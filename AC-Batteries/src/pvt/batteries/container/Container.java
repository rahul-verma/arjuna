package pvt.batteries.container;

import java.util.List;
import java.util.Map;

public interface Container<T, V> {

	Map<T, V> items() throws Exception;

	Map<T, V> items(List<T> filterKeys) throws Exception;

	Map<String, String> strItems() throws Exception;

	Map<String, String> strItems(List<T> filterKeys) throws Exception;

	List<V> values() throws Exception;

	List<V> values(List<T> keys) throws Exception;

	List<String> strings() throws Exception;

	List<String> strings(List<T> keys) throws Exception;

	V value(T key) throws Exception;

	String string(T key) throws Exception;

	boolean hasKey(T key) throws Exception;

}