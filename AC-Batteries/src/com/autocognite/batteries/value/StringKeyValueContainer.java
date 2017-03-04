package com.autocognite.batteries.value;

import com.autocognite.pvt.batteries.container.BaseValueContainer;
import com.autocognite.pvt.batteries.value.ValueType;

public class StringKeyValueContainer extends BaseValueContainer<String> {

	@Override
	public ValueType valueType(String strKey) {
		return ValueType.STRING;
	}

	@Override
	public Class valueEnumType(String strKey) {
		return null;
	}

	@Override
	public String key(String strKey) {
		return strKey.toUpperCase();
	}

	public String formatKey(String k) {
		return key(k);
	}
	//
	// public void add(String propName, String propValue) {
	// this.add(this.key(propName), new StringValue(propValue));
	// }

	public StringKeyValueContainer clone() {
		StringKeyValueContainer map = new StringKeyValueContainer();
		try {
			map.cloneAdd(this.items());
		} catch (Exception e) {
			e.printStackTrace();
		}
		return map;
	}

}
