package pvt.batteries.value;

import com.arjunapro.testauto.enums.ValueType;
import com.arjunapro.testauto.interfaces.Value;

public class LongValue extends NumberValue {

	public LongValue(long number) {
		super(ValueType.LONG, number);
	}

	@Override
	public Value clone() {
		return new LongValue(this.getRawObject());
	}

	@SuppressWarnings({ "unchecked", "unused" })
	private long getRawObject() {
		return (Long) this.object();
	}

	@Override
	public long asLong() {
		return (Long) this.object();
	}
}
