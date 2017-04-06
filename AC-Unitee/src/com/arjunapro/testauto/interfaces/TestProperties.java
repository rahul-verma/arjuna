package com.arjunapro.testauto.interfaces;

import java.util.List;
import java.util.Map;

import com.arjunapro.testauto.enums.TestAttribute;

public interface TestProperties {
	
	String id() throws Exception;
	
	String name() throws Exception;
	
	String idea() throws Exception;
	
	int priority() throws Exception;

	Map<TestAttribute, Value> items() throws Exception;

	Map<String, String> strItems() throws Exception;

	Value value(TestAttribute key) throws Exception;

	String string(TestAttribute key) throws Exception;

	boolean hasKey(TestAttribute key) throws Exception;
	
	List<String> strings(List<TestAttribute> props)  throws Exception;

	Map<String, String> strItems(List<TestAttribute> props)  throws Exception;
}
