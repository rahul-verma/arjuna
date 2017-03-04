package com.autocognite.pvt.unitee.reporter.lib.issue;

import java.util.HashMap;

import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.arjuna.enums.IssueAttribute;
import com.autocognite.pvt.arjuna.enums.IssueSubType;
import com.autocognite.pvt.arjuna.enums.IssueType;
import com.autocognite.pvt.batteries.container.EnumKeyValueContainer;
import com.autocognite.pvt.batteries.value.StringValue;
import com.autocognite.pvt.batteries.value.ValueType;

public class IssueProperties 
				extends EnumKeyValueContainer<IssueAttribute>{

	public IssueProperties(){
		HashMap<IssueAttribute,Value> map = new HashMap<IssueAttribute,Value>();
		map.put(IssueAttribute.TYPE, notSetValue);
		map.put(IssueAttribute.SUB_TYPE, notSetValue);
		map.put(IssueAttribute.ENAME, naValue);
		map.put(IssueAttribute.EMSG, naValue);
		map.put(IssueAttribute.ETRACE, naValue);
		map.put(IssueAttribute.STEP_NUM, naValue);
		map.put(IssueAttribute.FNAME, naValue);
		super.add(map);
	}

	@Override
	public ValueType valueType(IssueAttribute propType) {
		switch(propType){
		case ENAME:
			return ValueType.STRING;
		case EMSG:
			return ValueType.STRING;
		case TYPE:
			return ValueType.ENUM;
		case SUB_TYPE:
			return ValueType.ENUM;
		case ETRACE:
			return ValueType.STRING;
		case STEP_NUM:
			return ValueType.INTEGER;
		case FNAME:
			return ValueType.STRING;
		case ID:
			return ValueType.INTEGER;
		}	
		
		return null;
	}
	
	@Override
	public ValueType valueType(String strKey) {
		return this.valueType(key(strKey));
	}

	@Override
	public IssueAttribute key(String strKey) {
		return IssueAttribute.valueOf(strKey.toUpperCase());
	}
	
	@Override
	public Class<? extends Enum<?>> valueEnumType(String strKey) {
		IssueAttribute key = key(strKey);
		if (valueType(key) != ValueType.ENUM){
			return null;
		} else {
			switch (key){
			case TYPE:
				return IssueType.class;
			case SUB_TYPE:
				return IssueSubType.class;	
			}
		}
		return null;
	}
	
	public void setExcName(String ename) {
		this.add(IssueAttribute.ENAME, new StringValue(ename));
	}
	
	public String ename() throws Exception {
		return this.value(IssueAttribute.ENAME).asString();
	}

	public int id() throws Exception {
		Value issue = this.value(IssueAttribute.ID);
		if (issue.isNull()){
			return -1;
		} else {
			return this.value(IssueAttribute.ID).asInt();
		}
	}
}
