package com.autocognite.batteries.value;

public interface Value extends DataWrapper, Cloneable {

	Object object();

	Value clone();

}