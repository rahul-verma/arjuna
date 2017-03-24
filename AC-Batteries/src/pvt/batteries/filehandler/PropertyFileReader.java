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
package pvt.batteries.filehandler;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class PropertyFileReader {
	FileLineReader reader = null;
	String[] excludePrefixes = {};

	public PropertyFileReader(String filePath) throws IOException {
		reader = new FileLineReader(filePath);
	}

	public PropertyFileReader(String filePath, String[] excludePrefixes) throws IOException {
		reader = new FileLineReader(filePath);
		this.excludePrefixes = excludePrefixes;
	}

	public HashMap<String, String> getAllProperties() {
		HashMap<String, String> retMap = new HashMap<String, String>();
		ArrayList<String> lines = reader.all();
		for (String line : lines) {
			String[] lineParts = line.split("=", 2);
			if (lineParts.length == 2) {
				String left = lineParts[0].trim();
				boolean include = true;
				for (String exPrefix : excludePrefixes) {
					if (left.startsWith(exPrefix)) {
						include = false;
						break;
					}
				}
				if (include) {
					retMap.put(lineParts[0].trim(), lineParts[1].trim());
				}
			}
		}
		return retMap;
	}

	public void close() {
		this.reader.close();
	}
}
