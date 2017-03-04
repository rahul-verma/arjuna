package com.autocognite.pvt.batteries.container;

import com.autocognite.pvt.batteries.value.ValueType;

public abstract class EnumKeyValueContainer<T extends Enum<T>> extends BaseValueContainer<T> {

	public abstract ValueType valueType(T propType);

	public abstract ValueType valueType(String strKey);

	public abstract Class valueEnumType(String strKey);

	public T formatKey(T k) {
		return k;
	}
}
