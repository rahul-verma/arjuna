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

import java.util.List;

import pvt.arjunasdk.enums.FilterType;

public class StringFilterFactory {
	public static StringFilter getFilter(final String type, final String mode, final List<String> list) {
		FilterType fMode = FilterType.valueOf(mode.toUpperCase());
		String fType = type.toUpperCase();
		StringFilter f = null;
		switch (fType) {
		case "PREFIX":
			f = new PrefixFilter();
			break;
		case "SUFFIX":
			f = new SuffixFilter();
			break;
		case "EXACT":
			f = new ExactStringFilter();
			break;
		default:
			break;
		}
		if (f != null) {
			f.setMode(fMode);
			f.setFilterStrings(list);
		}
		return f;
	}

}

class PrefixFilter extends StringFilter {
	public boolean executeRelation(final String actual, final String expected) {
		return actual.startsWith(expected);
	}
}

class SuffixFilter extends StringFilter {
	public boolean executeRelation(final String actual, String expected) {
		return actual.endsWith(expected);
	}
}

class ExactStringFilter extends StringFilter {
	public boolean executeRelation(final String actual, final String expected) {
		return actual.equals(expected);
	}
}
