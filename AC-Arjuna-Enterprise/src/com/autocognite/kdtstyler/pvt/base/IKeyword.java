package com.autocognite.kdtstyler.pvt.base;

import java.util.HashMap;

public interface IKeyword {	
	Object execute();
	void setProperties(HashMap<String, String> props);
	HashMap<String, String> getProperties();
	String get(String prop);
	void set(String prop, String value);
	KeywordType getType();
}
