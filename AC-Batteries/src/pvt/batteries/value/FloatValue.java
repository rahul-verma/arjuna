package pvt.batteries.value;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;

public class FloatValue extends NumberValue {

	public FloatValue(Float number) {
		super(ValueType.FLOAT, number);
	}

	@Override
	public Value clone() {
		return new FloatValue(this.getRawObject());
	}

	@SuppressWarnings({ "unchecked", "unused" })
	private float getRawObject() {
		return (Float) this.object();
	}

	@Override
	public float asFloat() {
		return (Float) this.object();
	}
}
