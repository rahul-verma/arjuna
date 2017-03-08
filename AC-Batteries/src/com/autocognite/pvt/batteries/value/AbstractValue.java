package com.autocognite.pvt.batteries.value;

import com.autocognite.arjuna.interfaces.Value;

public class AbstractValue extends AbstractDataWrapper implements Value {
	private Object object = null;
	private ValueType type = ValueType.NULL;

	public AbstractValue(ValueType type, Object object) {
		this.setValueType(type);
		this.setObject(object);
	}

	@Override
	public ValueType valueType() {
		return type;
	}

	private void setValueType(ValueType type) {
		this.type = type;
	}

	@Override
	public Object object() {
		return object;
	}

	protected void setObject(Object value) {
		this.object = value;
	}

	@Override
	public Value clone() {
		return null;
	}

	@Override
	public boolean isNull() {
		return this.object == null;
	}

	@Override
	public String asString() {
		return this.object().toString();
	}

	@Override
	public String toString() {
		return this.asString();
	}

}
