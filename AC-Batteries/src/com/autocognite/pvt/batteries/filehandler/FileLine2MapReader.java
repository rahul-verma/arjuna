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

import com.autocognite.arjuna.utils.DataBatteries;

public class FileLine2MapReader {
	private String[] headers = null;
	private FileLine2ArrayReader reader = null;
	private String delimiter = null;

	public FileLine2MapReader(String filePath) throws Exception {
		reader = new FileLine2ArrayReader(filePath);
		this.setDelimiter(",");
		this.populateHeaders();
	}

	public FileLine2MapReader(String filePath, String delimiter) throws Exception {
		reader = new FileLine2ArrayReader(filePath, delimiter);
		this.populateHeaders();
	}

	protected void populateHeaders() throws Exception {
		String line = reader.nextRawLine();
		if ((line != null) && (line != "EMPTY_LINE")) {
			this.headers = reader.splitLine(line);
		} else {
			throw new Exception("Invalid input file data. Empty headers line.");
		}
	}

	public String[] getHeaders() {
		return this.headers;
	}

	protected HashMap<String, String> zip(String[] lineParts) throws Exception {
		if (lineParts.length != this.headers.length) {
			throw new Exception("Invalid input file data. Number of headers and data values do not match.\r\n"
					+ DataBatteries.flatten(this.headers) + "\r\n" + DataBatteries.flatten(lineParts) + "\r\n");
		} else {
			return DataBatteries.zip(this.headers, lineParts);
		}
	}

	public HashMap<String, String> next() throws Exception {
		String[] lineParts = reader.next();
		HashMap<String, String> zipped = null;
		if (lineParts == null) {
			return null;
		} else {
			zipped = this.zip(lineParts);
			if (zipped.containsKey("EXCLUDE")) {
				String exclude = zipped.get("EXCLUDE").toLowerCase().trim();
				if (exclude.equals("y") || exclude.equals("yes") || exclude.equals("true")) {
					zipped = this.next();
				}
				if (zipped != null) {
					zipped.remove("EXCLUDE");
				}

			}
			return zipped;
		}
	}

	public ArrayList<HashMap<String, String>> all() throws Exception {
		ArrayList<HashMap<String, String>> allLines = new ArrayList<HashMap<String, String>>();
		for (String[] line : reader.all()) {
			allLines.add(this.zip(line));
		}
		return allLines;
	}

	public String getDelimiter() {
		return delimiter;
	}

	public void setDelimiter(String delimiter) {
		this.delimiter = delimiter;
	}
}
