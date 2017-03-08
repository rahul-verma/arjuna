package com.autocognite.pvt.batteries.value;

import com.autocognite.arjuna.interfaces.StringKeyValueContainer;
import com.autocognite.pvt.batteries.container.BaseValueContainer;

public class DefaultStringKeyValueContainer extends BaseValueContainer<String> implements StringKeyValueContainer{

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

	public DefaultStringKeyValueContainer clone() {
		DefaultStringKeyValueContainer map = new DefaultStringKeyValueContainer();
		try {
			map.cloneAdd(this.items());
		} catch (Exception e) {
			e.printStackTrace();
		}
		return map;
	}

}
