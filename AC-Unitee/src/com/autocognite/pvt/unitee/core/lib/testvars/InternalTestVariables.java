package com.autocognite.pvt.unitee.core.lib.testvars;

import java.util.Map;

import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.batteries.databroker.DataReference;
import com.autocognite.batteries.databroker.ReadOnlyDataRecord;
import com.autocognite.batteries.value.StringKeyValueContainer;
import com.google.gson.JsonObject;

public interface InternalTestVariables extends TestVariables {

	InternalTestObjectProperties rawObjectProps() throws Exception;

	InternalTestProperties rawTestProps() throws Exception;

	StringKeyValueContainer rawCustomProps() throws Exception;

	StringKeyValueContainer rawUdv() throws Exception;
	
	void setObjectProps(InternalTestObjectProperties props) throws Exception;

	void setTestProps(InternalTestProperties props) throws Exception;

	void setCustomProps(StringKeyValueContainer props) throws Exception;

	void setUdv(StringKeyValueContainer props) throws Exception;

	void populateDefaults() throws Exception;

	JsonObject asJsonObject() throws Exception;

	void setDataRecord(ReadOnlyDataRecord dataRecord);

	void addDataReference(String name, DataReference dataRef);

	void addDataReferences(Map<String, DataReference> dataRefs) throws Exception;

}