package pvt.batteries.value;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;

public class NullValue extends AbstractValue {

	public NullValue() {
		super(ValueType.NULL, null);
	}

	@Override
	public Value clone() {
		return this;
	}

	@Override
	public String asString() {
		return "null";
	}

	@Override
	public boolean isNull() {
		return true;
	}
}
