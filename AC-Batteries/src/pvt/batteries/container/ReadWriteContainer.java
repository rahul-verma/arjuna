package pvt.batteries.container;

import java.util.List;
import java.util.Map;

public interface ReadWriteContainer<T, V> extends ReadOnlyContainer<T, V> {

	void add(Map<T, V> map);

	void add(T k, V v);

	void add(T k, Number v);

	void add(T k, String v);

	void add(T k, boolean v);

	void addObject(T k, Object v);

	<T1 extends Enum<T1>> void add(T k, T1 v);

	<T1 extends Enum<T1>> void addEnumList(T k, List<T1> values);

	<T1 extends Number> void addNumberList(T k, List<T1> values);

	void addStringList(T k, List<String> values);
}
