package pvt.batteries.value;

import com.arjunapro.testauto.enums.ValueType;
import com.arjunapro.testauto.interfaces.Value;

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
