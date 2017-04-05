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
package pvt.batteries.databroker;

import java.util.Iterator;
import java.util.Set;

import com.arjunapro.ddt.datarecord.DefaultDataRecord;
import com.arjunapro.ddt.exceptions.DataSourceFinishedException;
import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.ddt.interfaces.DataSource;
import com.arjunapro.sysauto.file.IniFileReader;

public class IniFileDataSource implements DataSource {
	IniFileReader reader = null;
	Set<String> sections = null;
	Iterator<String> iter = null;

	public IniFileDataSource(String path) throws Exception {
		reader = new IniFileReader(path);
		sections = this.reader.getAllSections();
		iter = sections.iterator();
	}

	@Override
	public synchronized DataRecord next() throws DataSourceFinishedException {
		if (iter.hasNext()) {
			return new DefaultDataRecord(this.reader.getSectionDataObjects((String) iter.next()));
		} else {
			throw new DataSourceFinishedException("Records Finished.");
		}
	}

}
