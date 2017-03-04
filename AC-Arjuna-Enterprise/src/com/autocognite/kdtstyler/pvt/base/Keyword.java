package com.autocognite.kdtstyler.pvt.base;

import java.util.HashMap;

public class Keyword implements IKeyword {
	KeywordType myType = null;
	HashMap<String, String> props = new HashMap<String, String>();
	
	public Object execute() {
		return null;
	}

	public void setProperties(HashMap<String, String> props) {
		this.props = props;
	}

	public HashMap<String, String> getProperties() {
		return this.props;	
	}

	public KeywordType getType() {
		return myType;
	}

	public String get(String prop) {
		return props.get(prop);
	}

	public void set(String prop, String value) {
		props.put(prop, value);
	}
}
