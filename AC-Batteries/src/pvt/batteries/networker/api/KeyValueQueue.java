package pvt.batteries.networker.api;

import pvt.batteries.networker.lib.util.KeyValuePair;

public interface KeyValueQueue {

	boolean hasNext();

	KeyValuePair next();

	void add(String name, String value);
}