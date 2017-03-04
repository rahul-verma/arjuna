package com.autocognite.pvt.batteries.nvpair;

import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.batteries.value.ValueType;

public interface NameValuePair extends Cloneable {
	String name() throws Exception;

	NameValuePair clone();

	Value value();

	ValueType valueType();
}