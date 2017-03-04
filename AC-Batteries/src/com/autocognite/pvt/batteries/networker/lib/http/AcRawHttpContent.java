package com.autocognite.pvt.batteries.networker.lib.http;

import org.apache.http.HttpEntity;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.util.EntityUtils;

import com.autocognite.pvt.batteries.networker.api.http.AcHttpContent;

public class AcRawHttpContent implements AcHttpContent{
	private StringEntity myEntity = null;
	
	public AcRawHttpContent(String text, ContentType type){
		myEntity = new StringEntity(text, 
				   ContentType.create(type.getMimeType(), "UTF-8"));
	}
	
	public HttpEntity getContentEntity(){
		return myEntity;
	}
	
	public String getContent() throws Exception{
		return EntityUtils.toString(myEntity);
	}

}
