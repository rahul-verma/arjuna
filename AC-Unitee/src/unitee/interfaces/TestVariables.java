package unitee.interfaces;

import java.util.Map;

import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.interfaces.StringKeyValueContainer;
import pvt.arjunasdk.ddt.interfaces.DataReference;

public interface TestVariables {

	TestObjectProperties object() throws Exception;

	TestProperties test() throws Exception;

	StringKeyValueContainer utp() throws Exception;

	StringKeyValueContainer utv() throws Exception;

	DataRecord record();

	DataReference refer(String refName) throws Exception;
	
	Map<String, DataReference> references();

}