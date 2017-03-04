package com.autocognite.pvt.batteries.networker.lib.http;

import java.net.URI;

import com.autocognite.pvt.batteries.networker.api.http.AcUrl;

public class AcDefaultUrl implements AcUrl {
	private String url = null;
	
	public AcDefaultUrl(String url){
		this.url = url;
	}
	
	public AcDefaultUrl(URI uri) {
		this.url = uri.toString();
	}

	public String toString(){
		return this.url;
	}

}
