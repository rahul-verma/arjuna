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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.testauto.interfaces.Value;

import pvt.batteries.container.ReadOnlyContainer;
import pvt.batteries.value.AnyRefValue;
import pvt.batteries.value.DefaultStringKeyValueContainer;

public class DefaultDataRecord extends DefaultStringKeyValueContainer implements ReadOnlyContainer<String, Value>, DataRecord {
	HashMap<Integer, String> indexToKeyMap = new HashMap<Integer, String>();
	private int counter = 0;

	public void add(String name, Object obj) {
		String internalName = name;
		if (name == null) {
			internalName = String.format("GK_%d", counter);
		}
		super.add(internalName.toUpperCase(), new AnyRefValue(obj));
		this.indexToKeyMap.put(counter, internalName.toUpperCase());
		counter += 1;
	}

	public DefaultDataRecord() {

	}

	public DefaultDataRecord(List<String> names, ArrayList<Object> values) {
		for (int i = 0; i < names.size(); i++) {
			this.add(names.get(i), values.get(i));
		}
	}

	public DefaultDataRecord(String[] names, Object[] values) {
		for (int i = 0; i < names.length; i++) {
			this.add(names[i], values[i]);
		}
	}

	public DefaultDataRecord(HashMap<String, Object> nvMap) {
		for (String name : nvMap.keySet()) {
			this.add(name, nvMap.get(name));
		}
	}

	public DefaultDataRecord(Object[] record) {
		for (Object obj : record) {
			this.add(null, obj);
		}
	}

	public DefaultDataRecord(String[] headers, List<Object> objList) {
		for (int i = 0; i < headers.length; i++) {
			this.add(headers[i], objList.get(i));
		}
	}

	public boolean hasIndex(int index) {
		return indexToKeyMap.containsKey(index);
	}

	private void checkIndex(int index) throws Exception {
		if (!this.hasIndex(index)) {
			throw new Exception(String.format("Index Error: Max data record index: %d", this.counter));
		}
	}

	@Override
	public Value valueAt(int index) throws Exception {
		checkIndex(index);
		return this.value(indexToKeyMap.get(index));
	}

	@Override
	public String stringAt(int index) throws Exception {
		checkIndex(index);
		return this.value(indexToKeyMap.get(index)).asString();
	}

	@Override
	public Object objectAt(int index) throws Exception {
		checkIndex(index);
		return this.value(indexToKeyMap.get(index)).object();
	}
}
