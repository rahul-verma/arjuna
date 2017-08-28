package pvt.unitee.reporter.lib.test;

import java.util.HashMap;
import java.util.Map;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;
import pvt.batteries.container.EnumKeyValueContainer;
import pvt.batteries.value.EnumValue;
import pvt.batteries.value.IntValue;
import pvt.batteries.value.StringValue;
import pvt.unitee.enums.TestResultAttribute;
import pvt.unitee.enums.TestResultCode;
import pvt.unitee.enums.TestResultType;

public class TestResultProperties 
				extends EnumKeyValueContainer<TestResultAttribute>{

	private Throwable exc;

	public TestResultProperties(){
		Map<TestResultAttribute,Value> map = new HashMap<TestResultAttribute,Value>();
		map.put(TestResultAttribute.RESULT, notSetValue);
		map.put(TestResultAttribute.CODE, notSetValue);
		map.put(TestResultAttribute.DESC, notSetValue);
		map.put(TestResultAttribute.ISSUE_ID, naValue);
		super.add(map);
	}

	@Override
	public ValueType valueType(TestResultAttribute propType) {
		switch(propType){
			case CODE:
				return ValueType.ENUM;
			case DESC:
				return ValueType.STRING;
			case RESULT:
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
	public TestResultAttribute key(String strKey) {
		return TestResultAttribute.valueOf(strKey.toUpperCase());
	}
	
	@Override
	public Class<? extends Enum<?>> valueEnumType(String strKey) {
		TestResultAttribute key = key(strKey);
		if (valueType(key) != ValueType.ENUM){
			return null;
		} else {
			switch (key){
			case CODE:
				return TestResultCode.class;
			case RESULT:
				return TestResultType.class;		
			}
		}
		return null;
	}

	public TestResultType result() throws Exception{
		if (!this.value(TestResultAttribute.RESULT).isNull()){
			return this.value(TestResultAttribute.RESULT).asEnum(TestResultType.class);
		} else {
			return null;
		}
	}
	
	public void setResult(TestResultType type){
		this.add(TestResultAttribute.RESULT, new EnumValue<TestResultType>(type));
	}

	public void setResultCode(TestResultCode code) {
		this.add(TestResultAttribute.CODE, new EnumValue<TestResultCode>(code));
	}

	public void setDescription(String desc) {
		this.add(TestResultAttribute.DESC, new StringValue(desc));
	}
	
	public void setIssueId(int id) throws Exception {
		if (id == -1){
			// retain na value
		} else {
			this.add(TestResultAttribute.ISSUE_ID, new IntValue(id));
		}
	}

	public String desc() throws Exception {
		return this.value(TestResultAttribute.DESC).asString();
	}

	public Throwable exception() {
		return this.exc;
	}

	public int issueId() throws Exception {
		Value issue = this.value(TestResultAttribute.ISSUE_ID);
		if (issue.isNull()){
			return -1;
		} else {
			return this.value(TestResultAttribute.ISSUE_ID).asInt();
		}
	}

}
