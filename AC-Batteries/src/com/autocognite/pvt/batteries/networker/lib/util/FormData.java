package com.autocognite.pvt.batteries.networker.lib.util;

import java.util.ArrayList;
import java.util.Iterator;

public class FormData extends AbstractKVQueue{
	
	public void add(String name, String value){
		this.add(new FormParam(name, value));
	}

}
