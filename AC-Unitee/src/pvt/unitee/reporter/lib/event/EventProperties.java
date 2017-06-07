package pvt.unitee.reporter.lib.event;

import java.util.HashMap;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;
import pvt.batteries.container.EnumKeyValueContainer;
import pvt.batteries.value.BooleanValue;
import pvt.batteries.value.StringValue;
import pvt.unitee.enums.EventAttribute;

public class EventProperties 
				extends EnumKeyValueContainer<EventAttribute>{
	
	public EventProperties(){
		HashMap<EventAttribute,Value> map = new HashMap<EventAttribute,Value>();
		map.put(EventAttribute.TEXT, notSetValue);
		map.put(EventAttribute.COMPONENT, notSetValue);
		map.put(EventAttribute.SUCCESS, new BooleanValue(true));
		map.put(EventAttribute.REMARKS, naValue);
		map.put(EventAttribute.EXC_MSG, naValue);
		map.put(EventAttribute.EXC_TRACE, naValue);
		super.add(map);
	}

	@Override
	public ValueType valueType(EventAttribute propType) {
		switch(propType){
		case TEXT:
			return ValueType.STRING;
		case COMPONENT:
			return ValueType.STRING;
		case SUCCESS:
			return ValueType.BOOLEAN;
		case REMARKS:
			return ValueType.STRING;
		case EXC_MSG:
			return ValueType.STRING;
		case EXC_TRACE:
			return ValueType.STRING;
		}
		return null;
	}
	
	@Override
	public ValueType valueType(String strKey) {
		return this.valueType(key(strKey));
	}

	@Override
	public EventAttribute key(String strKey) {
		return EventAttribute.valueOf(strKey.toUpperCase());
	}
	
	@Override
	public Class<? extends Enum<?>> valueEnumType(String strKey) {
		return null;
	}

	public void setText(String text) {
		this.add(EventAttribute.TEXT, new StringValue(text));
	}

	public void setComponent(String component) {
		this.add(EventAttribute.COMPONENT, new StringValue(component));
	}
}
