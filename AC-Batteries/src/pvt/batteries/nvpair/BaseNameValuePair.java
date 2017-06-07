package pvt.batteries.nvpair;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;

public class BaseNameValuePair implements NameValuePair {
	private String name = null;
	private Value value = null;

	public BaseNameValuePair(String name, Value value) {
		this.setName(name);
		this.setValue(value);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.poc.nvp.NameValuePair#type()
	 */
	@Override
	public ValueType valueType() {
		return this.value.valueType();
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.poc.nvp.NameValuePair#name()
	 */
	@Override
	public String name() {
		return name;
	}

	private void setName(String name) {
		this.name = name;
	}

	@Override
	public Value value() {
		return value;
	}

	private void setValue(Value value) {
		this.value = value;
	}

	@Override
	public NameValuePair clone() {
		return null;
	}

}
