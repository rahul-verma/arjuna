package com.autocognite.pvt.batteries.networker.api;

import com.autocognite.pvt.batteries.networker.lib.util.KeyValuePair;

public interface KeyValueQueue {

	boolean hasNext();

	KeyValuePair next();

	void add(String name, String value);
}