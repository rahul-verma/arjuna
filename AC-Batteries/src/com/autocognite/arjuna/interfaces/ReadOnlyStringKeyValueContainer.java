package com.autocognite.arjuna.interfaces;

import java.util.List;
import java.util.Map;

public interface ReadOnlyStringKeyValueContainer{
	
	Map<String, Value> items() throws Exception;

	Map<String, Value> items(List<String> filterKeys) throws Exception;

	Map<String, String> strItems() throws Exception;

	Map<String, String> strItems(List<String> filterKeys) throws Exception;

	List<Value> values() throws Exception;

	List<Value> values(List<String> keys) throws Exception;

	List<String> strings() throws Exception;

	List<String> strings(List<String> keys) throws Exception;

	Value value(String key) throws Exception;

	String string(String key) throws Exception;

	boolean hasKey(String key);
}
