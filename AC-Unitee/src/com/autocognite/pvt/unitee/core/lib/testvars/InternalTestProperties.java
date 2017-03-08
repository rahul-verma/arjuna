package com.autocognite.pvt.unitee.core.lib.testvars;

import com.autocognite.arjuna.interfaces.TestProperties;
import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.pvt.arjuna.enums.TestAttribute;
import com.autocognite.pvt.batteries.container.ValueContainer;
import com.autocognite.pvt.batteries.value.ValueType;

public interface InternalTestProperties 
				extends TestProperties, ValueContainer<TestAttribute>{
	
	void setId(Value value) throws Exception;
	
	void setId(String name) throws Exception;
	
	void setName(Value value) throws Exception;
	
	void setName(String name) throws Exception;
	
	void setIdea(Value value) throws Exception;
	
	void setIdea(String name) throws Exception;
	
	void setPriority(Value value) throws Exception;
	
	void setPriority(int num) throws Exception;

	ValueType valueType(TestAttribute propType);

	ValueType valueType(String strKey);

	TestAttribute key(String strKey);

	Class valueEnumType(String strKey);

	void populateDefaults() throws Exception;

}
