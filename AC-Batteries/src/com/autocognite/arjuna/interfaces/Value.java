package com.autocognite.arjuna.interfaces;

public interface Value extends DataWrapper, Cloneable {

	Object object();

	Value clone();

}