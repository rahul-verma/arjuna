/*******************************************************************************
 * Copyright 2015-16 AutoCognite Testing Research Pvt Ltd
 * 
 * Website: www.AutoCognite.com
 * Email: support [at] autocognite.com
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/
package com.autocognite.pvt.batteries.databroker;

import java.util.ArrayList;
import java.util.HashMap;

import com.autocognite.arjuna.interfaces.DataReference;
import com.autocognite.arjuna.utils.datarecord.DefaultDataRecord;
import com.autocognite.arjuna.interfaces.DataRecord;
import com.autocognite.pvt.batteries.filehandler.ExcelFileLine2ArrayReader;

public class ExcelDataReference implements DataReference {
	private HashMap<String, DataRecord> map = new HashMap<String, DataRecord>();
	private ExcelFileLine2ArrayReader reader = null;
	private String keyColumn = null;
	private int keyIndex = -1;
	private ArrayList<String> headers = null;
	private Object path;

	public ExcelDataReference(String path, String keyColumn) throws Exception {
		this.path = path;
		this.keyColumn = keyColumn;
		if (path.toLowerCase().endsWith("xls")) {
			reader = new ExcelFileLine2ArrayReader(path);
			this.headers = reader.getHeaders();
		} else {
			throw new Exception("Unsupported file format for Excel reading.");
		}
		if (keyColumn == null) {
			this.keyIndex = 0;
		} else {
			this.keyIndex = this.headers.indexOf(keyColumn);
			if (this.keyIndex == -1) {
				throw new Exception(String.format(
						"The supplied key column [%s] does not exist in the Excel file at path '%s'", keyColumn, path));
			}
		}

		populate();
	}

	private void populate() throws Exception {
		if (this.keyColumn == null) {
			this.keyColumn = reader.getHeaders().get(0);
		}

		ArrayList<Object> dataRecord = reader.next();
		String keyColumnValue = null;
		while (dataRecord != null) {
			keyColumnValue = (String) dataRecord.get(this.keyIndex);
			DataRecord data = new DefaultDataRecord(this.headers, dataRecord);
			map.put(keyColumnValue.toUpperCase(), data);
			dataRecord = reader.next();
		}
		reader.close();
	}

	public synchronized DataRecord record(String key) throws Exception {
		if (map.containsKey(key.toUpperCase())) {
			return map.get(key.toUpperCase());
		} else {
			throw new Exception(String.format("Excel Data reference at %s does not contain %s key.", this.path, key));
		}

	}

}
