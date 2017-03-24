package com.arjunapro.testauto.interfaces;

import java.util.Map;

import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.ddt.interfaces.DataReference;
import com.arjunapro.testauto.interfaces.StringKeyValueContainer;

public interface TestVariables {

	TestObjectProperties object() throws Exception;

	TestProperties test() throws Exception;

	StringKeyValueContainer utp() throws Exception;

	StringKeyValueContainer utv() throws Exception;

	DataRecord record();

	DataReference refer(String refName) throws Exception;
	
	Map<String, DataReference> references();

}