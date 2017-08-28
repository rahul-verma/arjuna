package pvt.batteries.container;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public abstract class BaseContainer<T, V> implements ReadOnlyContainer<T, V>, ReadWriteContainer<T, V> {

	private Map<T, V> map = null;
	private List<T> keys = null;

	protected abstract V getValueForNonExistentKey(T key) throws Exception;

	protected abstract String getStrValueForNonExistentKey(T key) throws Exception;

	public abstract void cloneAdd(Map<T, V> map);

	public abstract void cloneAdd(T k, V v);

	public abstract T formatKey(T k);

	private void addFormattedKeyToKeyList(T key) {
		if (!map.containsKey(key)) {
			keys.add(key);
		}
	}

	private void addAllKeysToKeyList(List<T> keys) {
		for (T key : keys) {
			this.addFormattedKeyToKeyList(formatKey(key));
		}
	}

	private void addAllKeysToKeyList(Set<T> keys) {
		for (T key : keys) {
			this.addFormattedKeyToKeyList(formatKey(key));
		}
	}

	public BaseContainer(Map<T, V> map) {
		this.addAllKeysToKeyList(this.map.keySet());
		this.map = map;
	}

	public BaseContainer() {
		this.map = new HashMap<T, V>();
		this.keys = new ArrayList<T>();
	}

	public void add(Map<T, V> map) {
		for (T key : map.keySet()) {
			this.addFormattedKeyToKeyList(formatKey(key));
			this.map.put(formatKey(key), map.get(key));
		}
	}

	public void add(Container<T, V> container) throws Exception {
		this.add(container.items());
	}

	public void add(T k, V v) {
		this.addFormattedKeyToKeyList(formatKey(k));
		this.map.put(formatKey(k), v);
	}

	public boolean hasKey(T k) throws Exception{
		return this.map.containsKey(formatKey(k));
	}

	@Override
	public V value(T key) throws Exception {
		T fKey = formatKey(key);
		if (this.map.containsKey(fKey)) {
			return this.map.get(fKey);
		} else {
			return getValueForNonExistentKey(key);
		}
	}

	@Override
	public String string(T key) throws Exception {
		T fKey = formatKey(key);
		if (this.map.containsKey(fKey)) {
			return this.map.get(fKey).toString();
		} else {
			return getStrValueForNonExistentKey(key);
		}
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.result.Container#items()
	 */
	@Override
	public Map<T, V> items() throws Exception {
		return this.map;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.result.Container#items(java.util.List)
	 */
	@Override
	public Map<T, V> items(List<T> filterKeys) throws Exception {
		Map<T, V> retMap = new HashMap<T, V>();
		for (T key : keys) {
			retMap.put(key, value(key));
		}

		return retMap;
	}

	private Map<String, String> _strItems(List<T> keys) throws Exception {
		Map<String, String> retMap = new HashMap<String, String>();
		for (T key : keys) {
			retMap.put(key.toString(), string(key));
		}

		return retMap;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.result.Container#strItems()
	 */
	@Override
	public Map<String, String> strItems() throws Exception {
		return this._strItems(this.keys);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.result.Container#strItems(java.util.List)
	 */
	@Override
	public Map<String, String> strItems(List<T> filterKeys) throws Exception {
		return this._strItems(filterKeys);
	}

	private List<V> _values(List<T> keys) throws Exception {
		List<V> retList = new ArrayList<V>();
		for (T key : keys) {
			retList.add(value(key));
		}

		return retList;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.result.Container#values()
	 */
	@Override
	public List<V> values() throws Exception {
		return _values(this.keys);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.result.Container#values(java.util.List)
	 */
	@Override
	public List<V> values(List<T> keys) throws Exception {
		return _values(keys);
	}

	private List<String> _strValues(List<T> keys) throws Exception {
		List<String> retList = new ArrayList<String>();
		for (T key : keys) {
			retList.add(string(key));
		}

		return retList;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.result.Container#strings()
	 */
	@Override
	public List<String> strings() throws Exception {
		return _strValues(this.keys);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.result.Container#strings(java.util.List)
	 */
	@Override
	public List<String> strings(List<T> keys) throws Exception {
		return _strValues(keys);
	}

}
