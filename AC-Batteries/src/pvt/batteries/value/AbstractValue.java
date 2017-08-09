package pvt.batteries.value;

import java.util.List;

import arjunasdk.enums.ValueType;
import arjunasdk.exceptions.UnsupportedRepresentationException;
import arjunasdk.interfaces.Value;
import pvt.batteries.utils.StackBatteries;

public class AbstractValue implements Value {
	private Object object = null;
	private ValueType type = ValueType.NULL;

	public AbstractValue(ValueType type, Object object) {
		this.setValueType(type);
		this.setObject(object);
	}

	@Override
	public ValueType valueType() {
		return type;
	}

	private void setValueType(ValueType type) {
		this.type = type;
	}

	@Override
	public Object object() {
		return object;
	}

	protected void setObject(Object value) {
		this.object = value;
	}

	@Override
	public Value clone() {
		return null;
	}

	@Override
	public boolean isNull() {
		return this.object == null;
	}

	@Override
	public String asString() {
		return this.object().toString();
	}

	@Override
	public String toString() {
		return this.asString();
	}
	
	protected void throwUnsupportedException(ValueType targetType, String callingMethodName) throws Exception{
		throw new UnsupportedRepresentationException(this.valueType().toString(), callingMethodName, this.toString(), targetType.toString());
	}
	
	protected void throwUnsupportedForEnumException(ValueType targetType, String enumClassName, String callingMethodName) throws Exception{
		throw new UnsupportedRepresentationException(this.valueType().toString(), callingMethodName, this.toString(), targetType.toString() + " of enum type " + enumClassName);
	}
	
	protected void throwUnsupportedEnumForEnumException(String sourceEnumClassName, ValueType targetType, String enumClassName, String callingMethodName) throws Exception{
		throw new UnsupportedRepresentationException(this.valueType().toString() + "of enum type " + sourceEnumClassName, callingMethodName, this.toString(), targetType.toString() + " of enum type " + enumClassName);
	}
	
	@Override
	public boolean asBoolean() throws Exception {
		throwUnsupportedException(ValueType.BOOLEAN, "asBoolean");
		return false;
	}

	@Override
	public Number asNumber() throws Exception {
		throwUnsupportedException(ValueType.NUMBER, "asNumber");
		return null;
	}

	@Override
	public int asInt() throws Exception {
		throwUnsupportedException(ValueType.INTEGER, "asInt");
		return 0;
	}

	@Override
	public long asLong() throws Exception {
		throwUnsupportedException(ValueType.LONG, "asLong");
		return 0;
	}

	@Override
	public double asDouble() throws Exception {
		throwUnsupportedException(ValueType.DOUBLE, "asDouble");
		return 0.0;
	}

	@Override
	public float asFloat() throws Exception {
		throwUnsupportedException(ValueType.FLOAT, "asFloat");
		return 0.0f;
	}

	@Override
	public <T extends Enum<T>> T asEnum(Class<T> enumClass) throws Exception {
		throwUnsupportedException(ValueType.ENUM, "asEnum");
		return null;
	}

	@Override
	public <T extends Enum<T>> List<T> asEnumList(Class<T> klass) throws Exception {
		throwUnsupportedException(ValueType.ENUM_LIST, "asEnumList");
		return null;
	}

	@Override
	public List<Number> asNumberList() throws Exception {
		throwUnsupportedException(ValueType.NUMBER_LIST, "asNumberList");
		return null;
	}

	@Override
	public List<Integer> asIntList() throws Exception {
		throwUnsupportedException(ValueType.INT_LIST, "asIntList");
		return null;
	}

	@Override
	public List<String> asStringList() throws Exception {
		throwUnsupportedException(ValueType.STRING_LIST, "asStringList");
		return null;
	}

	public List<?> asList() throws Exception {
		throwUnsupportedException(ValueType.LIST, "asList");
		return null;
	}
}
