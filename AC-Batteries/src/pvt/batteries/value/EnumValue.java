package pvt.batteries.value;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;

public class EnumValue<T extends Enum<T>> extends AbstractValue {
	Class<T> actualEnumClass = null;

	public EnumValue(T enumObject) {
		super(ValueType.ENUM, enumObject);
		this.actualEnumClass = (Class<T>) enumObject.getClass();
	}

	private EnumValue(Class<T> klass, Object obj) {
		super(ValueType.ENUM, obj);
		this.actualEnumClass = klass;
	}

	@Override
	public Value clone() {
		return new EnumValue<T>(actualEnumClass, this.object());
	}

	@Override
	public <T2 extends Enum<T2>> T2 asEnum(Class<T2> enumClass) throws Exception {
		if (actualEnumClass == enumClass) {
			return (T2) this.object();
		} else {
			this.throwUnsupportedEnumForEnumException(actualEnumClass.getSimpleName(), ValueType.ENUM, enumClass.getSimpleName(), "asEnum");
			return null;
		}
	}
}
