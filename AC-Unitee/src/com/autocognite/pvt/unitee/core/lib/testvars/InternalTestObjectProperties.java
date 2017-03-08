package com.autocognite.pvt.unitee.core.lib.testvars;

import com.autocognite.arjuna.enums.ValueType;
import com.autocognite.arjuna.interfaces.DataRecord;
import com.autocognite.arjuna.interfaces.TestObjectProperties;
import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.internal.arjuna.enums.TestObjectAttribute;
import com.autocognite.internal.arjuna.enums.TestObjectType;
import com.autocognite.pvt.batteries.container.ReadOnlyContainer;
import com.autocognite.pvt.batteries.container.ValueContainer;
import com.autocognite.pvt.batteries.databroker.DefaultDataRecord;
import com.autocognite.pvt.batteries.value.IntValue;
import com.autocognite.pvt.batteries.value.StringValue;

public interface InternalTestObjectProperties 
				extends TestObjectProperties, ValueContainer<TestObjectAttribute>, ReadOnlyContainer<TestObjectAttribute, Value>{
	
	void setObjectId(String name) throws Exception;
	
	void setObjectType(Value value) throws Exception;

	void setObjectType(TestObjectType type) throws Exception;
	
	void setParentQualifiedName(String name) throws Exception;
	
	void setParentQualifiedName(Value value) throws Exception;
	
	void setPackage(String name) throws Exception;
	
	void setPackage(Value value) throws Exception;
	
	void setClass(String name) throws Exception;
	
	void setClassInstanceNumber(Value value) throws Exception;
	
	void setClassInstanceNumber(int num) throws Exception;
	
	void setMethod(String name) throws Exception;
	
	void setName(String name) throws Exception;
	
	void setMethodInstanceNumber(Value value) throws Exception;
	
	void setMethodInstanceNumber(int num) throws Exception;

	void setTestNumber(Value value) throws Exception;
	
	void setTestNumber(int num) throws Exception;
	
	void setSessionName(Value value) throws Exception;
	
	void setSessionName(String name) throws Exception;

	ValueType valueType(TestObjectAttribute propType);

	ValueType valueType(String strKey);

	TestObjectAttribute key(String strKey);

	Class valueEnumType(String strKey);

	void populateDefaults() throws Exception;

	void setGroupName(String groupName) throws Exception;

	void setThreadId(String id) throws Exception;
	
	void setDataRecord(DefaultDataRecord dataRecord) throws Exception;
	
	void setSessionNodeName(Value value) throws Exception;	
	void setSessionNodeName(String name) throws Exception;		
	void setSessionNodeId(Value value) throws Exception;	
	void setSessionNodeId(int id) throws Exception;		
	void setSessionSubNodeId(Value value) throws Exception;	
	void setSessionSubNodeId(int id) throws Exception;

	void setBeginTstamp() throws Exception;
	void setEndTstamp() throws Exception;	
}
