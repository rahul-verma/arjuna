package pvt.unitee.reporter.lib.ignored;

import java.util.HashMap;
import java.util.Map;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;
import pvt.batteries.container.EnumKeyValueContainer;
import pvt.batteries.value.EnumValue;
import pvt.batteries.value.StringValue;
import pvt.unitee.enums.IgnoredTestAttribute;
import pvt.unitee.enums.IgnoredTestReason;
import pvt.unitee.enums.IgnoredTestStatus;

public class IgnoredTestProperties 
extends EnumKeyValueContainer<IgnoredTestAttribute>{

	private Throwable exc;

	public IgnoredTestProperties(){
		Map<IgnoredTestAttribute,Value> map = new HashMap<IgnoredTestAttribute,Value>();
		map.put(IgnoredTestAttribute.STATUS, notSetValue);
		map.put(IgnoredTestAttribute.REASON, notSetValue);
		map.put(IgnoredTestAttribute.DESC, notSetValue);
		super.add(map);
	}

	@Override
	public ValueType valueType(IgnoredTestAttribute propType) {
		switch(propType){
		case REASON:
			return ValueType.ENUM;
		case DESC:
			return ValueType.STRING;
		case STATUS:
			return ValueType.ENUM;
		}
		return null;
	}

	@Override
	public ValueType valueType(String strKey) {
		return this.valueType(key(strKey));
	}

	@Override
	public IgnoredTestAttribute key(String strKey) {
		return IgnoredTestAttribute.valueOf(strKey.toUpperCase());
	}

	@Override
	public Class<? extends Enum<?>> valueEnumType(String strKey) {
		IgnoredTestAttribute key = key(strKey);
		if (valueType(key) != ValueType.ENUM){
			return null;
		} else {
			switch (key){
			case REASON:
				return IgnoredTestReason.class;
			case STATUS:
				return IgnoredTestStatus.class;		
			}
		}
		return null;
	}

	public IgnoredTestStatus status() throws Exception{
		if (!this.value(IgnoredTestAttribute.STATUS).isNull()){
			return this.value(IgnoredTestAttribute.STATUS).asEnum(IgnoredTestStatus.class);
		} else {
			return null;
		}
	}

	public void setStatus(IgnoredTestStatus type){
		this.add(IgnoredTestAttribute.STATUS, new EnumValue<IgnoredTestStatus>(type));
	}

	public void setReason(IgnoredTestReason code) {
		this.add(IgnoredTestAttribute.REASON, new EnumValue<IgnoredTestReason>(code));
	}

	public void setDescription(String desc) {
		this.add(IgnoredTestAttribute.DESC, new StringValue(desc));
	}

	public String desc() throws Exception {
		return this.value(IgnoredTestAttribute.DESC).asString();
	}

	public Throwable exception() {
		return this.exc;
	}

}
