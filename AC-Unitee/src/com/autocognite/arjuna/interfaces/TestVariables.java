package com.autocognite.arjuna.interfaces;

import java.util.Map;

public interface TestVariables {

	TestObjectProperties object() throws Exception;

	TestProperties test() throws Exception;

	StringKeyValueContainer utp() throws Exception;

	StringKeyValueContainer utv() throws Exception;

	DataRecord record();

	DataReference refer(String refName) throws Exception;
	
	Map<String, DataReference> references();

}