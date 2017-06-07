package pvt.batteries.nvpair;

import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;

public interface NameValuePair extends Cloneable {
	String name() throws Exception;

	NameValuePair clone();

	Value value();

	ValueType valueType();
}