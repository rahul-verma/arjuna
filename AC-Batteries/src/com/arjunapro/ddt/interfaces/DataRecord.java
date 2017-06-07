package com.arjunapro.ddt.interfaces;

import com.arjunapro.testauto.interfaces.ReadOnlyStringKeyValueContainer;
import com.arjunapro.testauto.interfaces.Value;

public interface DataRecord extends ReadOnlyStringKeyValueContainer {

	Value valueAt(int index) throws Exception;

	String stringAt(int index) throws Exception;

	Object objectAt(int index) throws Exception;

}
