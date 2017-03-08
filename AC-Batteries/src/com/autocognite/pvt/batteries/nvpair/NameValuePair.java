package com.autocognite.pvt.batteries.nvpair;

import com.autocognite.arjuna.enums.ValueType;
import com.autocognite.arjuna.interfaces.Value;

public interface NameValuePair extends Cloneable {
	String name() throws Exception;

	NameValuePair clone();

	Value value();

	ValueType valueType();
}