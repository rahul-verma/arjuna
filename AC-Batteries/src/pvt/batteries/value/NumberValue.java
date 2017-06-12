package pvt.batteries.value;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;

public class NumberValue extends AbstractValue {

	public NumberValue(Number numberObject) {
		super(ValueType.NUMBER, numberObject);
	}

	protected NumberValue(ValueType type, Number numberObject) {
		super(type, numberObject);
	}

	@Override
	public Value clone() {
		return new NumberValue(getRawObject());
	}

	@SuppressWarnings({ "unchecked", "unused" })
	private Number getRawObject() {
		return (Number) this.object();
	}

	@Override
	public Number asNumber() {
		return (Number) this.object();
	}
	
	@Override
	public int asInt() throws Exception {
		try{
			return this.asNumber().intValue();
		} catch (Exception e){
			throw new Exception(String.format(">>%s<< can not be represented as an integer.", this.asString()));
		}
	}

	@Override
	public long asLong() throws Exception {
		try{
			return this.asNumber().longValue();
		} catch (Exception e){
			throw new Exception(String.format(">>%s<< can not be represented as a long int.", this.asString()));
		}
	}

	@Override
	public double asDouble() throws Exception {
		try{
			return this.asNumber().doubleValue();
		} catch (Exception e){
			throw new Exception(String.format(">>%s<< can not be represented as a double.", this.asString()));
		}
	}

	@Override
	public float asFloat() throws Exception {
		try{
			return this.asNumber().floatValue();
		} catch (Exception e){
			throw new Exception(String.format(">>%s<< can not be represented as a float.", this.asString()));
		}
	}
}
