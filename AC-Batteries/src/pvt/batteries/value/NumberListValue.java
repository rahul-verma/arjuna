package pvt.batteries.value;

import java.util.List;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;

public class NumberListValue<T extends Number> extends AbstractValue {

	public NumberListValue(List<T> listObject) {
		super(ValueType.NUMBER_LIST, listObject);
	}

	@Override
	public Value clone() {
		return new NumberListValue<T>(getRawList());
	}

	@SuppressWarnings("unchecked")
	private List<T> getRawList() {
		return (List<T>) this.object();
	}

	@SuppressWarnings("unchecked")
	@Override
	public List<Number> asNumberList() {
		return (List<Number>) this.object();
	}

}
