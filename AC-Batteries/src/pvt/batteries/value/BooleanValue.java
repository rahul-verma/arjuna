package pvt.batteries.value;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;

public class BooleanValue extends AbstractValue {

	public BooleanValue(boolean boolObject) {
		super(ValueType.BOOLEAN, boolObject);
	}

	@Override
	public Value clone() {
		return new BooleanValue(this.asBoolean());

	}

	@Override
	public boolean asBoolean() {
		return (boolean) this.object();
	}

}
