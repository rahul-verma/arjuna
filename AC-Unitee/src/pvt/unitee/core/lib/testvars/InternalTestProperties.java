package pvt.unitee.core.lib.testvars;

import com.arjunapro.testauto.enums.TestAttribute;
import com.arjunapro.testauto.enums.ValueType;
import com.arjunapro.testauto.interfaces.TestProperties;
import com.arjunapro.testauto.interfaces.Value;

import pvt.batteries.container.ReadOnlyContainer;
import pvt.batteries.container.ValueContainer;

public interface InternalTestProperties 
				extends TestProperties, ReadOnlyContainer<TestAttribute, Value>, ValueContainer<TestAttribute>{
	
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
