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
package com.autocognite.batteries.databroker;

import org.apache.commons.io.FilenameUtils;

import com.autocognite.pvt.batteries.databroker.ExcelDataReference;

public class DataReferenceFactory {
	public static DataReference getReference(String fileFormat, String refFileDir, String refFileName, String key)
			throws Exception {
		return getReference(fileFormat, refFileDir + "/" + refFileName, key);
	}

	public static DataReference getReference(String path) throws Exception {
		return getReference(FilenameUtils.getExtension(path).toUpperCase(), path, null);
	}

	public static DataReference getReference(String fileFormat, String path, String key) throws Exception {
		switch (fileFormat.toUpperCase().trim()) {
		case "XLS":
			return new ExcelDataReference(path, key);
		default:
			throw new Exception("Unsupported file reference format: " + fileFormat);
		}
	}
}
