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
package com.arjunapro.ddt.datarecord;

import java.util.HashMap;
import java.util.List;

import com.arjunapro.ddt.exceptions.MapDataRecordLookUpException;
import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.testauto.interfaces.Value;

import pvt.batteries.ddt.datarecord.BaseDataRecord;
import pvt.batteries.value.AnyRefValue;

public class MapDataRecord extends BaseDataRecord implements DataRecord {

	protected void add(String name, Object obj) {
		super.add(name.toUpperCase(), new AnyRefValue(obj));
	}
	
	public MapDataRecord() {

	}
	
	public MapDataRecord(List<String> names, List<Object> values){
		for (int i = 0; i < names.size(); i++) {
			this.addWithKey(names.get(i), values.get(i));
		}		
	}
	
	public MapDataRecord(String[] headers, List<Object> objList) {
		for (int i = 0; i < headers.length; i++) {
			this.addWithKey(headers[i], objList.get(i));
		}
	}

	public MapDataRecord(String[] names, Object[] values){
		for (int i = 0; i < names.length; i++) {
			this.addWithKey(names[i], values[i]);
		}	
	}
	
	public MapDataRecord(HashMap<String, Object> nvMap){
		for (String name : nvMap.keySet()) {
			this.addWithKey(name, nvMap.get(name));
		}
	}	
	
	@Override
	protected Value getValueForNonExistentKey(String key) throws Exception {
		throw new MapDataRecordLookUpException(key);
	}

	@Override
	protected String getStrValueForNonExistentKey(String key) throws Exception {
		throw new MapDataRecordLookUpException(key);
	}
	
	public boolean hasIndex(int index) throws Exception {
		throw new Exception("strings() method is not supported for Map Data Record.");
	}

	@Override
	public Value valueAt(int index) throws Exception {
		throw new Exception("valueAt() method is not supported for Map Data Record. Use value(keyName) instead");
	}

	@Override
	public String stringAt(int index) throws Exception {
		throw new Exception("stringAt() method is not supported for Map Data Record. Use string(keyName) instead");
	}

	@Override
	public Object objectAt(int index) throws Exception {
		throw new Exception("objectAt() method is not supported for Map Data Record. Use object(keyName) instead");
	}
}
