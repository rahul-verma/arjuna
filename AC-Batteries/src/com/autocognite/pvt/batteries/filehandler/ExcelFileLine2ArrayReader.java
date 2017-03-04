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
package com.autocognite.pvt.batteries.filehandler;

import java.util.ArrayList;
import java.util.HashMap;

public class ExcelFileLine2ArrayReader extends ExcelFileReader {

	public ExcelFileLine2ArrayReader(String path) throws Exception {
		super(path);
	}

	public ArrayList<Object> next() throws Exception {
		if (this.getCurrentRowIndex() < this.getRowCount()) {
			ArrayList<Object> retArray = getRowAsArrayList(this.getCurrentRowIndex());
			this.setCurrentRowIndex(this.getCurrentRowIndex() + 1);
			HashMap<String, Object> zipped = zip(retArray);
			if (zipped.containsKey("EXCLUDE")) {
				String exclude = ((String) zipped.get("EXCLUDE")).toLowerCase().trim();
				if (exclude.equals("y") || exclude.equals("yes") || exclude.equals("true")) {
					retArray = this.next();
				}
				if (retArray != null) {
					retArray.remove(this.getHeaders().indexOf("EXCLUDE"));
				}
			}
			return retArray;
		} else {
			return null;
		}
	}
}
