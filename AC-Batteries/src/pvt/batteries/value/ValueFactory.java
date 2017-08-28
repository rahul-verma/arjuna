package pvt.batteries.value;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;
import arjunasdk.sysauto.batteries.DataBatteries;

public class ValueFactory {
	private static NullValue nullValue = new NullValue();
	private static BooleanValue trueValue = new BooleanValue(true);
	private static BooleanValue falseValue = new BooleanValue(false);
	private static Set<String> trues = new HashSet<String>(Arrays.asList("on", "ON", "true", "TRUE", "yes", "YES"));
	private static Set<String> falses = new HashSet<String>(Arrays.asList("off", "OFF", "false", "FALSE", "no", "NO"));
	private static Set<ValueType> numbers = new HashSet<ValueType>(
			Arrays.asList(ValueType.NUMBER, ValueType.INTEGER, ValueType.LONG, ValueType.FLOAT, ValueType.DOUBLE));
	
	private static void throwIncomaptibleInputTypeException(ValueType sourceValueType, String actualValueStr, ValueType targetValueType) throws Exception{
		throw new IncompatibleInputForValueException(sourceValueType.toString(), actualValueStr, targetValueType.toString());
	}
	
	private static void throwIncomaptibleInputTypeExceptionForEnum(String targetEnumClass, ValueType sourceValueType, String actualValueStr, ValueType targetValueType) throws Exception{
		throw new IncompatibleInputForValueException(actualValueStr, sourceValueType.toString(), targetValueType.toString() + "of enum type " + targetEnumClass);
	}

	public static NullValue createNullValue() throws Exception {
		return nullValue;
	}

	public static BooleanValue createBooleanValue(boolean flag) throws Exception {
		if (flag) {
			return trueValue;
		} else {
			return falseValue;
		}
	}

	public static BooleanValue createBooleanValue(String boolStr) throws Exception {
		if (trues.contains(boolStr)) {
			return new BooleanValue(true);
		} else if (falses.contains(boolStr)) {
			return new BooleanValue(false);
		}
		throwIncomaptibleInputTypeException(ValueType.BOOLEAN, boolStr, ValueType.STRING);
		return null;
	}

	public static BooleanValue createBooleanValue(Value value) throws Exception {
		if ((value.valueType() == ValueType.BOOLEAN)) {
			return createBooleanValue(value.asBoolean());
		} else if (value.valueType() == ValueType.STRING) {
			return createBooleanValue(value.asString());
		} else {
			throwIncomaptibleInputTypeException(ValueType.BOOLEAN, value.asString(), value.valueType());
			return null;
		}
	}

	public static StringListValue createStringListValue(String value) throws Exception {
		List<String> tempList = DataBatteries.split(value, ",");
		return new StringListValue(tempList);
	}

	public static StringListValue createStringUCListValue(String value) throws Exception {
		List<String> tempList = DataBatteries.splitAndConvertToUpperCase(value);
		return new StringListValue(tempList);
	}

	public static IntValue createIntValue(int value) throws Exception {
		return new IntValue(value);
	}

	public static IntValue createIntValue(String value) throws Exception {
		try {
			return new IntValue(Integer.parseInt(value));
		} catch (Exception e) {
			throwIncomaptibleInputTypeException(ValueType.INTEGER, value, ValueType.STRING);
			return null;
		}
	}

	public static LongValue createLongValue(long value) throws Exception {
		return new LongValue(value);
	}

	public static LongValue createLongValue(String value) throws Exception {
		try {
			return new LongValue(Long.parseLong(value));
		} catch (Exception e) {
			throwIncomaptibleInputTypeException(ValueType.LONG, value, ValueType.STRING);
			return null;
		}
	}

	public static FloatValue createFloatValue(float value) throws Exception {
		return new FloatValue(value);
	}

	public static FloatValue createFloatValue(String value) throws Exception {
		try {
			return new FloatValue(Float.parseFloat(value));
		} catch (Exception e) {
			throwIncomaptibleInputTypeException(ValueType.FLOAT, value, ValueType.STRING);
			return null;
		}
	}

	public static NumberValue createDoubleValue(double value) throws Exception {
		return new DoubleValue(value);
	}

	public static DoubleValue createDoubleValue(String value) throws Exception {
		try {
			return new DoubleValue(Double.parseDouble(value));
		} catch (Exception e) {
			throwIncomaptibleInputTypeException(ValueType.DOUBLE, value, ValueType.STRING);
			return null;
		}
	}

	public static NumberValue createNumberValue(Number number) throws Exception {
		if (number instanceof Integer) {
			return createIntValue((Integer) number);
		} else if (number instanceof Long) {
			return createLongValue((Long) number);
		} else if (number instanceof Float) {
			return createFloatValue((Float) number);
		} else if (number instanceof Double) {
			return createDoubleValue((Double) number);
		} else {
			return new NumberValue(number);
		}
	}

	public static NumberValue createNumberValue(String numStr) throws Exception {
		try {
			return createIntValue(numStr);
		} catch (IncompatibleInputForValueException e) {
			try {
				return createLongValue(numStr);
			} catch (IncompatibleInputForValueException f) {
				try {
					return createFloatValue(numStr);
				} catch (IncompatibleInputForValueException g) {
					try {
						return createDoubleValue(numStr);
					} catch (IncompatibleInputForValueException h) {
						throwIncomaptibleInputTypeException(ValueType.NUMBER, numStr, ValueType.STRING);
						return null;
					}
				}
			}
		}
	}

	public static NumberValue createNumberValueFrom(Value value) throws Exception {
		if ((value.valueType() == ValueType.NUMBER) || (numbers.contains(value.valueType()))) {
			return createNumberValue(value.asNumber());
		} else if (value.valueType() == ValueType.STRING) {
			return createNumberValue(value.asString());
		}
		
		throwIncomaptibleInputTypeException(ValueType.NUMBER, value.asString(), value.valueType());
		return null;
	}

	public static StringValue createStringValue(String value) throws Exception {
		return new StringValue(value);
	}

	public static StringValue createStringValueFrom(Value value) throws Exception {
		return new StringValue(value.asString());
	}

	public static StringListValue createStringListValueFrom(Value value) throws Exception {
		if (value.isNull()) {
			throwIncomaptibleInputTypeException(ValueType.STRING_LIST, value.asString(), value.valueType());
			return null;
		}

		if ((value.valueType() == ValueType.STRING_LIST)) {
			return new StringListValue(value.asStringList());
		}

		if (value.valueType() == ValueType.ANYREF_LIST) {
			List<String> tempList = new ArrayList<String>();
			for (Object o : value.asList()) {
				tempList.add(o.toString());
			}
			return new StringListValue(tempList);
		}

		if (value.valueType() == ValueType.STRING) {
			return new StringListValue(Arrays.asList(value.asString()));
		}

		throwIncomaptibleInputTypeException(ValueType.STRING_LIST, value.asString(), value.valueType());
		return null;
	}

	public static <T extends Enum<T>> EnumValue<T> creatEnumValue(Class<T> enumClass, String value) throws Exception {
		try {
			StringValue v = new StringValue(value);
			T obj = v.asEnum(enumClass);
			return new EnumValue<T>(obj);
		} catch (Exception e) {
			throwIncomaptibleInputTypeExceptionForEnum(enumClass.getSimpleName(), ValueType.ENUM, value, ValueType.STRING);
			return null;
		}
	}

	public static <T extends Enum<T>> EnumValue<T> creatEnumValue(Class<T> enumClass, Value value)
			throws Exception {
		if (value.isNull()) {
			throwIncomaptibleInputTypeExceptionForEnum(enumClass.getSimpleName(), ValueType.ENUM, value.asString(), value.valueType());
			return null;
		}

		if ((value.valueType() == ValueType.STRING)) {
			return new EnumValue<T>(value.asEnum(enumClass));
		}

		if (value.valueType() == ValueType.ENUM) {
			return new EnumValue<T>(value.asEnum(enumClass));
		}

		throwIncomaptibleInputTypeExceptionForEnum(enumClass.getSimpleName(), ValueType.ENUM, value.asString(), value.valueType());
		return null;
	}

	public static <T extends Enum<T>> EnumListValue<T> creatEnumListValue(Class<T> enumClass, List<String> value)
			throws Exception {
		try {
			StringListValue sv = new StringListValue(value);
			List<T> obj = sv.asEnumList(enumClass);
			return new EnumListValue<T>(obj);
		} catch (Exception e) {
			throwIncomaptibleInputTypeExceptionForEnum(enumClass.getSimpleName(), ValueType.ENUM_LIST, value.toString(), ValueType.LIST);
			return null;
		}
	}

	public static <T extends Enum<T>> EnumListValue<T> createEnumListValue(Class<T> enumKlass, Value value)
			throws Exception {
		if ((value.valueType() == ValueType.ENUM_LIST)) {
			return new EnumListValue<T>(value.asEnumList(enumKlass));
		}

		if (value.valueType() == ValueType.STRING_LIST) {
			return creatEnumListValue(enumKlass, value.asStringList());
		}

		if (value.valueType() == ValueType.ANYREF_LIST) {
			return new EnumListValue<T>(value.asEnumList(enumKlass));
		}

		if (value.valueType() == ValueType.STRING) {
			return creatEnumListValue(enumKlass, Arrays.asList(value.asString()));
		}
		
		throwIncomaptibleInputTypeExceptionForEnum(enumKlass.getSimpleName(), ValueType.ENUM_LIST, value.asString(), value.valueType());
		return null;
	}

}
