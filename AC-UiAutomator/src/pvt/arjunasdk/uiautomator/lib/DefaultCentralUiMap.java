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
package pvt.arjunasdk.uiautomator.lib;

import java.util.HashMap;

import arjunasdk.uiauto.interfaces.PageMapper;
import pvt.arjunasdk.uiauto.api.CentralPageMap;

public class DefaultCentralUiMap implements CentralPageMap {

	private HashMap<String, HashMap<String, HashMap<String,String>>> rawMap =  new HashMap<String, HashMap<String, HashMap<String,String>>>();
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.map.ICentralUiMap#isRawMapPresent(java.lang.String)
	 */
	@Override
	public boolean isRawMapPresent(String uiFullName){
		return rawMap.containsKey(uiFullName);
	}
	
	@Override
	public HashMap<String, HashMap<String,String>> populateRawPageMap(String uiFullName, PageMapper mapper) throws Exception{
		if(!rawMap.containsKey(uiFullName)){
			HashMap<String, HashMap<String,String>> pMap = mapper.getPageMap();
			rawMap.put(uiFullName, pMap);
		}
		return rawMap.get(uiFullName);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.map.ICentralUiMap#getRawMap(java.lang.String)
	 */
	@Override
	public HashMap<String, HashMap<String,String>> getRawMap(String uiFullName) throws Exception{
		return rawMap.get(uiFullName);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.map.ICentralUiMap#getRawMap()
	 */
	@Override
	public HashMap<String, HashMap<String, HashMap<String,String>>> getRawMap() {
		return this.rawMap;
	}
	
}
