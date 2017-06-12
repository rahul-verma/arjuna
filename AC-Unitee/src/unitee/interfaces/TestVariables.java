package unitee.interfaces;

import java.util.Map;

import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.ddauto.interfaces.DataReference;
import arjunasdk.interfaces.StringKeyValueContainer;

public interface TestVariables {

	TestObjectProperties object() throws Exception;

	TestProperties test() throws Exception;

	StringKeyValueContainer attr() throws Exception;

	StringKeyValueContainer execVars() throws Exception;

	DataRecord record();

	DataReference refer(String refName) throws Exception;
	
	Map<String, DataReference> references();

}