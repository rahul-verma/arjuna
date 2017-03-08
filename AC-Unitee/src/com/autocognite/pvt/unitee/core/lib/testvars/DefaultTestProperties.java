package com.autocognite.pvt.unitee.core.lib.testvars;

import com.autocognite.arjuna.enums.ValueType;
import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.internal.arjuna.enums.TestAttribute;
import com.autocognite.pvt.batteries.container.EnumKeyValueContainer;
import com.autocognite.pvt.batteries.value.IntValue;
import com.autocognite.pvt.batteries.value.StringValue;

public class DefaultTestProperties 
				extends EnumKeyValueContainer<TestAttribute>
				implements InternalTestProperties{

	public DefaultTestProperties(){

	}
	
	@Override
	public void populateDefaults() throws Exception{
		this.setId(notSetValue);
		this.setName(notSetValue);
		this.setIdea(notSetValue);
		this.setPriority(notSetValue);		
	}
	
	public String id() throws Exception{
		return this.value(TestAttribute.ID).asString();
	}
	
	public void setId(Value value) throws Exception{
		super.add(TestAttribute.ID, value);
	}
	
	public void setId(String name) throws Exception{
		this.setId(new StringValue(name));
	}
	
	public String name() throws Exception{
		return this.value(TestAttribute.NAME).asString();
	}
	
	public void setName(Value value) throws Exception{
		super.add(TestAttribute.NAME, value);
	}
	
	public void setName(String name) throws Exception{
		this.setName(new StringValue(name));
	}
	
	public String idea() throws Exception{
		return this.value(TestAttribute.IDEA).asString();
	}
	
	public void setIdea(Value value) throws Exception{
		super.add(TestAttribute.IDEA, value);
	}
	
	public void setIdea(String name) throws Exception{
		this.setIdea(new StringValue(name));
	}
	
	public int priority() throws Exception{
		return this.value(TestAttribute.PRIORITY).asInt();
	}
	
	public void setPriority(Value value) throws Exception{
		super.add(TestAttribute.PRIORITY, value);
	}
	
	public void setPriority(int num) throws Exception{
		this.setPriority(new IntValue(num));
	}

	@Override
	public ValueType valueType(TestAttribute propType) {
		switch (propType){
		case ID:
			return ValueType.STRING;
		case NAME:
			return ValueType.STRING;
		case IDEA:
			return ValueType.STRING;
		case PRIORITY:
			return ValueType.INTEGER;			
		}
		return null;
	}
	
	@Override
	public ValueType valueType(String strKey) {
		return this.valueType(key(strKey));
	}

	@Override
	public TestAttribute key(String strKey) {
		return TestAttribute.valueOf(strKey.toUpperCase());
	}
	
	@Override
	public Class<? extends Enum<?>> valueEnumType(String strKey) {
		return null;
	}
	
	public DefaultTestProperties clone(){
		DefaultTestProperties map = new DefaultTestProperties();
		try{
			map.cloneAdd(this.items());
		} catch (Exception e){
			e.printStackTrace();
		}
		return map;
	}

}
