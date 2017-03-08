package com.autocognite.pvt.batteries.value;

import java.lang.reflect.Method;

import com.autocognite.arjuna.enums.ValueType;
import com.autocognite.arjuna.interfaces.Value;

public class StringValue extends AbstractValue {

	public StringValue(String strObject) {
		super(ValueType.STRING, strObject);
	}

	@Override
	public Value clone() {
		return new StringValue(this.asString());
	}

	@Override
	public String asString() {
		if (this.object() != null) {
			return this.object().toString();
		} else {
			return "null";
		}
	}

	public void process(Object formatterObject, Method formatter) throws Exception {
		this.setObject((String) formatter.invoke(formatterObject, this.asString()));
	}

	@Override
	public <T2 extends Enum<T2>> T2 asEnum(Class<T2> enumClass) throws Exception {
		try {
			return Enum.valueOf(enumClass, this.asString().toUpperCase());
		} catch (Exception e) {
			throw new UnsupportedRepresentationException(StringValue.class.getSimpleName(), "asEnum()", this.toString(),
					enumClass.getSimpleName());
		}
	}
}
