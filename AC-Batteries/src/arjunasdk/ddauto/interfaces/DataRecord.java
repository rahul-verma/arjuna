package arjunasdk.ddauto.interfaces;

import arjunasdk.interfaces.ReadOnlyStringKeyValueContainer;
import arjunasdk.interfaces.Value;

public interface DataRecord extends ReadOnlyStringKeyValueContainer {

	Value valueAt(int index) throws Exception;

	String stringAt(int index) throws Exception;

	Object objectAt(int index) throws Exception;

}
