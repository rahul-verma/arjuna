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

import pvt.arjunasdk.enums.FilterType;

public abstract class Filter implements IFilter {
	private FilterType type = null;

	public Filter() {
		this.type = FilterType.INCLUDE;
	}

	public final void setExclusionMode() {
		this.type = FilterType.EXCLUDE;
	}

	public final void setInclusionMode() {
		this.type = FilterType.INCLUDE;
	}

	public final void setMode(FilterType mode) {
		this.type = mode;
	}

	public final FilterType getFilterType() {
		return this.type;
	}

	protected final boolean shouldSelect(boolean match) {
		if (match) {
			if (type == FilterType.INCLUDE) {
				return true;
			} else if (type == FilterType.EXCLUDE) {
				return false;
			}
		} else {
			if (type == FilterType.INCLUDE) {
				return false;
			} else if (type == FilterType.EXCLUDE) {
				return true;
			}
		}

		return false;
	}
}
