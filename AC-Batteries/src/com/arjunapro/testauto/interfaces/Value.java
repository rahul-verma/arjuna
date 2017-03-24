package com.arjunapro.testauto.interfaces;

import com.arjunapro.ddt.interfaces.DataWrapper;

public interface Value extends DataWrapper, Cloneable {

	Object object();

	Value clone();

}