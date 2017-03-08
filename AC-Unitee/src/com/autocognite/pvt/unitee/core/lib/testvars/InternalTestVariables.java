package com.autocognite.pvt.unitee.core.lib.testvars;

import java.util.Map;

import com.autocognite.arjuna.interfaces.DataRecord;
import com.autocognite.arjuna.interfaces.DataReference;
import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.pvt.batteries.value.DefaultStringKeyValueContainer;
import com.google.gson.JsonObject;

public interface InternalTestVariables extends TestVariables {

	InternalTestObjectProperties rawObjectProps() throws Exception;

	InternalTestProperties rawTestProps() throws Exception;

	DefaultStringKeyValueContainer rawCustomProps() throws Exception;

	DefaultStringKeyValueContainer rawUdv() throws Exception;
	
	void setObjectProps(InternalTestObjectProperties props) throws Exception;

	void setTestProps(InternalTestProperties props) throws Exception;

	void setCustomProps(DefaultStringKeyValueContainer props) throws Exception;

	void setUdv(DefaultStringKeyValueContainer props) throws Exception;

	void populateDefaults() throws Exception;

	JsonObject asJsonObject() throws Exception;

	void setDataRecord(DataRecord dataRecord);

	void addDataReference(String name, DataReference dataRef);

	void addDataReferences(Map<String, DataReference> dataRefs) throws Exception;

}