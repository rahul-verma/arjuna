package pvt.batteries.value;

import com.arjunapro.testauto.enums.ValueType;
import com.arjunapro.testauto.interfaces.StringKeyValueContainer;

import pvt.batteries.container.BaseValueContainer;
import pvt.batteries.container.ValueContainer;

public class DefaultStringKeyValueContainer extends BaseValueContainer<String> implements ValueContainer<String>, StringKeyValueContainer{

	@Override
	public ValueType valueType(String strKey) {
		return ValueType.STRING;
	}

	@Override
	public Class valueEnumType(String strKey) {
		return null;
	}

	@Override
	public String key(String strKey) {
		return strKey.toUpperCase();
	}

	public String formatKey(String k) {
		return key(k);
	}
	//
	// public void add(String propName, String propValue) {
	// this.add(this.key(propName), new StringValue(propValue));
	// }

	public DefaultStringKeyValueContainer clone() {
		DefaultStringKeyValueContainer map = new DefaultStringKeyValueContainer();
		try {
			map.cloneAdd(this.items());
		} catch (Exception e) {
			e.printStackTrace();
		}
		return map;
	}

}
