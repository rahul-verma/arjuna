package com.arjunapro.testauto.interfaces;

import java.util.List;

public interface StringKeyValueContainer extends ReadOnlyStringKeyValueContainer{

	void add(String k, Value v);

	void add(String k, Number v);

	void add(String k, String v);

	void add(String k, boolean v);

	void addObject(String k, Object v);

	<T extends Enum<T>> void add(String k, T v);

	<T extends Enum<T>> void addEnumList(String k, List<T> values);

	<T extends Number> void addNumberList(String k, List<T> values);

	void addStringList(String k, List<String> values);
}
