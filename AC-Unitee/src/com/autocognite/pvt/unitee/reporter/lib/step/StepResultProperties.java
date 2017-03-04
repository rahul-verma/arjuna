package com.autocognite.pvt.unitee.reporter.lib.step;

import java.util.HashMap;

import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.arjuna.enums.StepResultAttribute;
import com.autocognite.pvt.arjuna.enums.StepResultType;
import com.autocognite.pvt.batteries.container.EnumKeyValueContainer;
import com.autocognite.pvt.batteries.value.IntValue;
import com.autocognite.pvt.batteries.value.ValueType;

public class StepResultProperties 
				extends EnumKeyValueContainer<StepResultAttribute>{
	
	private Throwable exc;

	public StepResultProperties(){
		HashMap<StepResultAttribute,Value> map = new HashMap<StepResultAttribute,Value>();
		map.put(StepResultAttribute.RESULT, notSetValue);
		map.put(StepResultAttribute.NUM, new IntValue(1));
		map.put(StepResultAttribute.PURPOSE, notSetValue);
		map.put(StepResultAttribute.ISSUE_ID, naValue);
		map.put(StepResultAttribute.SCR, naValue);
		map.put(StepResultAttribute.CTEXT, naValue);
		map.put(StepResultAttribute.CBENCH, naValue);
		map.put(StepResultAttribute.COBSERVE, naValue);
		super.add(map);
	}

	@Override
	public ValueType valueType(StepResultAttribute propType) {
		switch(propType){
		case RESULT:
			return ValueType.ENUM;
		case SCR:
			return ValueType.STRING_LIST;
		case CBENCH:
			return ValueType.STRING;
		case COBSERVE:
			return ValueType.STRING;
		case CTEXT:
			return ValueType.STRING;
		case NUM:
			return ValueType.INTEGER;
		case PURPOSE:
			return ValueType.STRING;
		case ISSUE_ID:
			return ValueType.INTEGER;
		}
		return null;
	}
	
	@Override
	public ValueType valueType(String strKey) {
		return this.valueType(key(strKey));
	}

	@Override
	public StepResultAttribute key(String strKey) {
		return StepResultAttribute.valueOf(strKey.toUpperCase());
	}
	
	@Override
	public Class<? extends Enum<?>> valueEnumType(String strKey) {
		StepResultAttribute key = key(strKey);
		if (valueType(key) != ValueType.ENUM){
			return null;
		} else {
			switch (key){
			case RESULT:
				return StepResultType.class;		
			}
		}
		return null;
	}
	
	public StepResultType result() throws Exception{
		return this.value(StepResultAttribute.RESULT).asEnum(StepResultType.class);
	}

	public void setStepNum(int i) {
		this.add(StepResultAttribute.NUM, new IntValue(i));
	}

	public Throwable exception() throws Exception{
		return this.exc;
	}
	
	public void setException(Throwable e) throws Exception{
		this.exc = e;
	}

	public int stepId() throws Exception {
		return this.value(StepResultAttribute.NUM).asInt();
	}

	public void setIssueId(int issueId) {
		this.add(StepResultAttribute.ISSUE_ID, new IntValue(issueId));
	}

	public int issueId() throws Exception {
		Value issue = this.value(StepResultAttribute.ISSUE_ID);
		if (issue.isNull()){
			return -1;
		} else {
			return this.value(StepResultAttribute.ISSUE_ID).asInt();
		}
	}
}
