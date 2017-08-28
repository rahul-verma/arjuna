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
package pvt.batteries.datafilter;

import java.util.ArrayList;
import java.util.List;

public abstract class StringFilter extends Filter {
	private List<String> filterStrings = new ArrayList<String>();

	public abstract boolean executeRelation(String actual, String expected);

	public boolean selected(final Object string) {
		if ((filterStrings.size() == 0) || (filterStrings == null)) {
			return true;
		}
		boolean bFound = false;
		for (String matchString : filterStrings) {
			if (executeRelation((String) string, matchString)) {
				bFound = true;
				break;
			}
		}
		return this.shouldSelect(bFound);
	}

	public void addFilterString(final String string) {
		if (string != null) {
			filterStrings.add(string.trim());
		}
	}

	public void addFilterStrings(final String strings, final String delimiter) {
		if (strings != null) {
			String[] parts = strings.split(delimiter);
			for (String part : parts) {
				addFilterString(part);
			}
		}
	}

	public void addFilterStrings(final String[] strings) {
		if (strings != null) {
			for (String string : strings) {
				addFilterString(string);
			}
		}
	}

	public void addFilterStrings(final List<String> strings) {
		if (strings != null) {
			for (String string : strings) {
				addFilterString(string);
			}
		}
	}

	public void setFilterStrings(final List<String> list) {
		if (list != null) {
			filterStrings = list;
		}
	}

	public void setFilterStrings(final String[] strings) {
		if (strings != null) {
			addFilterStrings(strings);
		}
	}
}
