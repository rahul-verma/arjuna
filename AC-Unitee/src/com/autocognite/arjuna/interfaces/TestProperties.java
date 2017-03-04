package com.autocognite.arjuna.interfaces;

import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.arjuna.enums.TestAttribute;
import com.autocognite.pvt.batteries.container.ReadOnlyContainer;

public interface TestProperties extends 
					ReadOnlyContainer<TestAttribute, Value>{
	
	String id() throws Exception;
	
	String name() throws Exception;
	
	String idea() throws Exception;
	
	int priority() throws Exception;
}
