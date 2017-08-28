package pvt.unitee.reporter.lib.fixture;

import java.util.HashMap;
import java.util.Map;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;
import pvt.batteries.container.EnumKeyValueContainer;
import pvt.batteries.value.StringValue;
import pvt.unitee.enums.FixtureResultPropertyType;
import pvt.unitee.enums.FixtureResultType;
import pvt.unitee.enums.TestClassFixtureType;

public class FixtureResultProperties 
				extends EnumKeyValueContainer<FixtureResultPropertyType>{

	public FixtureResultProperties(){
		Map<FixtureResultPropertyType,Value> map = new HashMap<FixtureResultPropertyType,Value>();
		map.put(FixtureResultPropertyType.RESULT, notSetValue);
		map.put(FixtureResultPropertyType.FIXTURE_TYPE, notSetValue);
		map.put(FixtureResultPropertyType.FIXTURE_METHOD, notSetValue);
		map.put(FixtureResultPropertyType.EXEC_POINT, notSetValue);
		map.put(FixtureResultPropertyType.ISSUE_ID, naValue);
		super.add(map);
	}

	@Override
	public ValueType valueType(FixtureResultPropertyType propType) {
		switch(propType){
		case EXEC_POINT:
			return ValueType.STRING;
		case FIXTURE_METHOD:
			return ValueType.STRING;
		case RESULT:
			return ValueType.ENUM;
		case FIXTURE_TYPE:
			return ValueType.ENUM;
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
	public FixtureResultPropertyType key(String strKey) {
		return FixtureResultPropertyType.valueOf(strKey.toUpperCase());
	}
	
	@Override
	public Class<? extends Enum<?>> valueEnumType(String strKey) {
		FixtureResultPropertyType key = key(strKey);
		if (valueType(key) != ValueType.ENUM){
			return null;
		} else {
			switch (key){
			case FIXTURE_TYPE:
				return TestClassFixtureType.class;
			case RESULT:
				return FixtureResultType.class;	
			}
		}
		return null;
	}

	public void setExecPoint(String execDesc) {
		this.add(FixtureResultPropertyType.EXEC_POINT, new StringValue(execDesc));
	}

	public void setFixtureMethod(String name) {
		this.add(FixtureResultPropertyType.FIXTURE_METHOD, new StringValue(name));
	}
	
	public int issueId() throws Exception {
		Value issue = this.value(FixtureResultPropertyType.ISSUE_ID);
		if (issue.isNull()){
			return -1;
		} else {
			return this.value(FixtureResultPropertyType.ISSUE_ID).asInt();
		}
	}
}
