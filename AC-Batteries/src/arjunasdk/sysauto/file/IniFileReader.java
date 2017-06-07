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
package arjunasdk.sysauto.file;

import java.io.File;
import java.util.HashMap;
import java.util.Set;

import org.ini4j.Profile.Section;
import org.ini4j.Wini;

public class IniFileReader {
	private Wini reader = null;

	public IniFileReader(String fileName) throws Exception {
		this.setReader(new Wini(new File(fileName)));
	}

	public IniFileReader(File file) throws Exception {
		this.setReader(new Wini(file));
	}

	public Wini getReader() {
		return reader;
	}

	public void setReader(Wini reader) {
		this.reader = reader;
	}

	public Set<String> getAllSections() {
		return this.reader.keySet();
	}

	public HashMap<String, Object> getSectionDataObjects(String section) {
		HashMap<String, Object> map = new HashMap<String, Object>();
		Section sec = this.reader.get(section);
		for (String key : sec.keySet()) {
			map.put(key, sec.get(key));
		}
		return map;
	}

	public HashMap<String, String> getSectionData(String section) {
		HashMap<String, String> map = new HashMap<String, String>();
		Section sec = this.reader.get(section);
		for (String key : sec.keySet()) {
			map.put(key, (String) sec.get(key));
		}
		return map;
	}
}
