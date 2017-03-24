package pvt.batteries.value;

import com.arjunapro.testauto.enums.ValueType;
import com.arjunapro.testauto.interfaces.Value;

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
