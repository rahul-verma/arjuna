package com.autocognite.arjuna.interfaces;

import java.util.List;
import java.util.Map;

import com.autocognite.internal.arjuna.enums.TestObjectAttribute;
import com.autocognite.internal.arjuna.enums.TestObjectType;
import com.autocognite.pvt.batteries.container.ReadOnlyContainer;

public interface TestObjectProperties {
	
	String objectId() throws Exception;
	
	TestObjectType objectType() throws Exception;
	
	String parentQualifiedName() throws Exception;
	
	String pkg() throws Exception;
	
	String klass() throws Exception;

	int classInstanceNumber() throws Exception;
	
	String method() throws Exception;
	
	String name() throws Exception;
	
	int methodInstanceNumber() throws Exception;

	int testNumber() throws Exception;
	
	String sessionName() throws Exception;

	String qualifiedName() throws Exception;
	
	String sessionNodeName() throws Exception;	

	int sessionNodeId() throws Exception;	

	int sessionSubNodeId() throws Exception;

	String group() throws Exception;
	
	Map<TestObjectAttribute, Value> items() throws Exception;

	Map<String, String> strItems() throws Exception;

	Value value(TestObjectAttribute key) throws Exception;

	String string(TestObjectAttribute key) throws Exception;

	boolean hasKey(TestObjectAttribute key);
	
	List<String> strings(List<TestObjectAttribute> props)  throws Exception;

	Map<String, String> strItems(List<TestObjectAttribute> props)  throws Exception;
}
