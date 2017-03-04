package com.autocognite.arjuna.interfaces;

import java.util.Map;

import com.autocognite.batteries.databroker.DataReference;
import com.autocognite.batteries.databroker.ReadOnlyDataRecord;
import com.autocognite.batteries.value.StringKeyValueContainer;

public interface TestVariables {

	TestObjectProperties objectProps() throws Exception;

	TestProperties testProps() throws Exception;

	StringKeyValueContainer customProps() throws Exception;

	StringKeyValueContainer udv() throws Exception;

	ReadOnlyDataRecord dataRecord();

	DataReference dataRef(String refName) throws Exception;
	
	Map<String, DataReference> getAllDataReferences();

}