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
package pvt.batteries.discoverer;

import java.util.HashMap;
import java.util.Map;

public class DiscoveredFile {
	private Map<DiscoveredFileAttribute, String> props = new HashMap<DiscoveredFileAttribute, String>();
	Class<?> klass = null;

	public String getAttribute(DiscoveredFileAttribute attr) {
		return this.props.get(attr);
	}

	public String setAttribute(DiscoveredFileAttribute attr, String value) {
		return this.props.put(attr, value);
	}

}
