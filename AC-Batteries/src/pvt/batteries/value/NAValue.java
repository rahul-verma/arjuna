package pvt.batteries.value;

import com.arjunapro.testauto.enums.ValueType;
import com.arjunapro.testauto.interfaces.Value;

public class NAValue extends AbstractValue {
	private static String val = "NA";

	public NAValue() {
		super(ValueType.NA, val);
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
