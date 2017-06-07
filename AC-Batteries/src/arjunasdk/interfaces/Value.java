package arjunasdk.interfaces;

import arjunasdk.ddauto.interfaces.DataWrapper;

public interface Value extends DataWrapper, Cloneable {

	Object object();

	Value clone();

}