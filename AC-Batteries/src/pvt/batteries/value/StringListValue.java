package pvt.batteries.value;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

import com.arjunapro.testauto.enums.ValueType;
import com.arjunapro.testauto.interfaces.Value;

public class StringListValue extends AbstractValue {

	public StringListValue(List<String> listObject) {
		super(ValueType.STRING_LIST, listObject);
	}

	@Override
	public Value clone() {
		return new StringListValue(this.asStringList());
	}

	@SuppressWarnings("unchecked")
	@Override
	public List<String> asStringList() {
		return (List<String>) this.object();
	}

	public void process(Object formatterObject, Method formatter) throws Exception {
		List<String> sList = this.asStringList();
		for (int i = 0; i < sList.size(); i++) {
			sList.set(i, (String) formatter.invoke(formatterObject, sList.get(i)));
		}
	}

	@Override
	public <T2 extends Enum<T2>> List<T2> asEnumList(Class<T2> enumClass) throws Exception {
		List<T2> tempList = new ArrayList<T2>();
		try {
			for (String s : this.asStringList()) {
				tempList.add(Enum.valueOf(enumClass, s.toUpperCase()));
			}
			return tempList;
		} catch (Exception e) {
			throw new UnsupportedRepresentationException(StringListValue.class.getSimpleName(), "asEnumList()",
					this.toString(), enumClass.getSimpleName());
		}
	}

}
