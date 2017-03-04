package com.autocognite.pvt.batteries.value;

import com.autocognite.batteries.value.Value;

public class IntValue extends NumberValue {

	public IntValue(Integer number) {
		super(ValueType.INTEGER, number);
	}

	@Override
	public Value clone() {
		return new IntValue(this.getRawObject());
	}

	@SuppressWarnings({ "unchecked", "unused" })
	private int getRawObject() {
		return (Integer) this.object();
	}

	@Override
	public int asInt() {
		return (Integer) this.object();
	}
}
