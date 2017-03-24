package pvt.batteries.nvpair;

import com.arjunapro.testauto.enums.ValueType;
import com.arjunapro.testauto.interfaces.Value;

public interface NameValuePair extends Cloneable {
	String name() throws Exception;

	NameValuePair clone();

	Value value();

	ValueType valueType();
}