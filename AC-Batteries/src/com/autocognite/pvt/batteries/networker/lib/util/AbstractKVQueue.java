package com.autocognite.pvt.batteries.networker.lib.util;

import java.util.ArrayList;
import java.util.Iterator;

import com.autocognite.pvt.batteries.networker.api.KeyValueQueue;

public abstract class AbstractKVQueue implements KeyValueQueue {

	private ArrayList<KeyValuePair> queue = new ArrayList<KeyValuePair>();
	Iterator iter  = null;
	
	/* (non-Javadoc)
	 * @see com.autocognite.networker.lib.util.KVQueue#hasNext()
	 */
	@Override
	public boolean hasNext(){
		if (iter == null){
			iter = queue.iterator();
		}
		return iter.hasNext();
	}
	
	protected void add(KeyValuePair pair){
		queue.add(pair);
	}
	
	abstract public void add(String name, String value);
	
	/* (non-Javadoc)
	 * @see com.autocognite.networker.lib.util.KVQueue#next()
	 */
	@Override
	public KeyValuePair next(){
		return (KeyValuePair) iter.next();
	}
}
