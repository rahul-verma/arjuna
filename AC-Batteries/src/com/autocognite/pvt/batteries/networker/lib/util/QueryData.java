package com.autocognite.pvt.batteries.networker.lib.util;

public class QueryData extends AbstractKVQueue{

	public void add(String name, String value){
		this.add(new QueryParam(name, value));
	}
}
