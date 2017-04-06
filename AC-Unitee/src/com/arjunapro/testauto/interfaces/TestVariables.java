package com.arjunapro.testauto.interfaces;

import java.util.Map;

import com.arjunapro.ddt.interfaces.DataRecord;

import pvt.arjunapro.ddt.interfaces.DataReference;

public interface TestVariables {

	TestObjectProperties object() throws Exception;

	TestProperties test() throws Exception;

	StringKeyValueContainer utp() throws Exception;

	StringKeyValueContainer utv() throws Exception;

	DataRecord record();

	DataReference refer(String refName) throws Exception;
	
	Map<String, DataReference> references();

}