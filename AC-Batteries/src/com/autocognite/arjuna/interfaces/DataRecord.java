package com.autocognite.arjuna.interfaces;

public interface DataRecord extends ReadOnlyStringKeyValueContainer {

	Value valueAt(int index) throws Exception;

	String stringAt(int index) throws Exception;

	Object objectAt(int index) throws Exception;

}
