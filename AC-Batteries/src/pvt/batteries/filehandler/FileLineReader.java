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

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

public class FileLineReader {
	Scanner reader = null;

	public FileLineReader(String filePath) throws IOException {
		File file = new File(filePath);
		reader = new Scanner(file);
	}

	String delimiter = null;

	public String next() {
		if (this.reader.hasNextLine()) {
			String line = this.reader.nextLine();
			if (line.trim().isEmpty() || line.trim().startsWith("#")) {
				return this.next();
			} else {
				return line;
			}
		} else {
			return null;
		}
	}

	public ArrayList<String> all() {
		try {
			ArrayList<String> al = new ArrayList<String>();
			String line = null;
			while ((line = (String) this.next()) != null) {
				al.add(line);
			}
			// DSHandler.print(al);
			return al;
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}

	public void close() {
		this.reader.close();
	}

}
