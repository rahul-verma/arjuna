package pvt.batteries.container;

import java.util.List;
import java.util.Map;

import com.arjunapro.testauto.enums.ValueType;
import com.arjunapro.testauto.interfaces.StringKeyValueContainer;
import com.arjunapro.testauto.interfaces.Value;

import pvt.batteries.value.AnyRefValue;
import pvt.batteries.value.BooleanValue;
import pvt.batteries.value.EnumListValue;
import pvt.batteries.value.EnumValue;
import pvt.batteries.value.NAValue;
import pvt.batteries.value.NotSetValue;
import pvt.batteries.value.NumberListValue;
import pvt.batteries.value.NumberValue;
import pvt.batteries.value.StringListValue;
import pvt.batteries.value.StringValue;

public abstract class BaseValueContainer<T> extends BaseContainer<T, Value> implements ValueContainer<T> {
	public static NotSetValue notSetValue = new NotSetValue();
	public static NAValue naValue = new NAValue();

	@Override
	protected Value getValueForNonExistentKey() {
		return notSetValue;
	}

	@Override
	protected String getStrValueForNonExistentKey() {
		return notSetValue.asString();
	}

	public void addAsStringValue(Map<T, String> map) {
		for (T k : map.keySet()) {
			this.addAsStringValue(formatKey(k), map.get(k));
		}
	}

	public void addAsStringValue(T k, String str) {
		this.add(formatKey(k), new StringValue(str));
	}

	@Override
	public void cloneAdd(Map<T, Value> map) {
		for (T key : map.keySet()) {
			super.add(formatKey(key), map.get(key).clone());
		}
	}

	@Override
	public void cloneAdd(Container<T, Value> container) throws Exception {
		Map<T, Value> map = container.items();
		this.cloneAdd(map);
	}

	@Override
	public void cloneAdd(T k, Value v) {
		super.add(formatKey(k), v.clone());
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.batteries.config.Configuration#add(java.lang.String,
	 * java.lang.Number)
	 */
	@Override
	public void add(T k, Number value) {
		this.add(this.formatKey(k), new NumberValue(value));
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.batteries.config.Configuration#add(java.lang.String,
	 * java.lang.String)
	 */
	@Override
	public void add(T k, String value) {
		this.add(this.formatKey(k), new StringValue(value));
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.batteries.config.Configuration#add(java.lang.String,
	 * boolean)
	 */
	@Override
	public void add(T k, boolean value) {
		this.add(this.formatKey(k), new BooleanValue(value));
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.batteries.config.Configuration#putObject(java.lang.
	 * String, java.lang.Object)
	 */
	@Override
	public void addObject(T k, Object value) {
		this.add(this.formatKey(k), new AnyRefValue(value));
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * com.autocognite.batteries.config.Configuration#putEnum(java.lang.String,
	 * T)
	 */
	@Override
	public <T1 extends Enum<T1>> void add(T k, T1 value) {
		this.add(this.formatKey(k), new EnumValue<T1>(value));
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * com.autocognite.batteries.config.Configuration#putEnumList(java.lang.
	 * String, java.util.List)
	 */
	@Override
	public <T1 extends Enum<T1>> void addEnumList(T k, List<T1> values) {
		this.add(this.formatKey(k), new EnumListValue<T1>(values));
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * com.autocognite.batteries.config.Configuration#putNumberList(java.lang.
	 * String, java.util.List)
	 */
	@Override
	public <T1 extends Number> void addNumberList(T k, List<T1> values) {
		this.add(this.formatKey(k), new NumberListValue<T1>(values));
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * com.autocognite.batteries.config.Configuration#putStringList(java.lang.
	 * String, java.util.List)
	 */
	@Override
	public void addStringList(T k, List<String> values) {
		this.add(this.formatKey(k), new StringListValue(values));
	}

	public abstract ValueType valueType(String strKey);

	public abstract Class valueEnumType(String strKey);

	public abstract T key(String strKey);
}
