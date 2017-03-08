package com.autocognite.pvt.batteries.value;

import java.util.ArrayList;
import java.util.List;

import com.autocognite.arjuna.interfaces.Value;

public class AnyRefListValue extends AbstractValue {

	public AnyRefListValue(List<?> listObject) {
		super(ValueType.ANYREF_LIST, listObject);
	}

	@Override
	public Value clone() {
		return new AnyRefListValue(this.asList());
	}

	@SuppressWarnings("unchecked")
	@Override
	public List<?> asList() {
		return (List<?>) this.object();
	}

	@Override
	public <T2 extends Enum<T2>> List<T2> asEnumList(Class<T2> enumClass) throws Exception {
		List<T2> tempList = new ArrayList<T2>();
		try {
			for (Object o : this.asList()) {

				try {
					tempList.add((T2) o);
				} catch (Exception e) {
					StringValue v = new StringValue((String) o);
					tempList.add(v.asEnum(enumClass));
				}
			}
			return tempList;
		} catch (Exception e) {
			e.printStackTrace();
			throw new UnsupportedRepresentationException(AnyRefListValue.class.getSimpleName(), "asEnumList()",
					this.toString(), enumClass.getSimpleName());
		}
	}

}
