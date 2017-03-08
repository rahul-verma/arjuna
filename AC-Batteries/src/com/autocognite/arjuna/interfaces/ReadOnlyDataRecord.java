package com.autocognite.arjuna.interfaces;

import com.autocognite.pvt.batteries.container.ReadOnlyContainer;

public interface ReadOnlyDataRecord extends ReadOnlyContainer<String, Value> {

	Value valueAt(int index) throws Exception;

	String stringAt(int index) throws Exception;

	Object objectAt(int index) throws Exception;

}
