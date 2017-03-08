package com.autocognite.arjuna.interfaces;

import com.autocognite.arjuna.enums.TestObjectType;
import com.autocognite.pvt.arjuna.enums.TestObjectAttribute;
import com.autocognite.pvt.batteries.container.ReadOnlyContainer;

public interface TestObjectProperties extends 
					ReadOnlyContainer<TestObjectAttribute, Value>{
	
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
}
