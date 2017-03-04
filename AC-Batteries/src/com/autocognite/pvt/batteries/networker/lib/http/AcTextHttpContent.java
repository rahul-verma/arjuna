package com.autocognite.pvt.batteries.networker.lib.http;

import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;

public class AcTextHttpContent extends AcRawHttpContent{
	
	public AcTextHttpContent(String text){
		super(text, ContentType.DEFAULT_TEXT);
	}
}
