package pvt.batteries.value;

import com.arjunapro.testauto.enums.ValueType;
import com.arjunapro.testauto.interfaces.Value;

public class NotSetValue extends AbstractValue {
	private static String val = "NOT_SET";

	public NotSetValue() {
		super(ValueType.NOT_SET, val);
	}

	@Override
	public Value clone() {
		return this;
	}

	@Override
	public String asString() {
		return val;
	}

	@Override
	public boolean isNull() {
		return true;
	}

}
