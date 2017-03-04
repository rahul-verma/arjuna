package com.autocognite.pvt.batteries.networker.api.http;

import org.apache.http.HttpEntity;

public interface AcHttpContent {
	public HttpEntity getContentEntity();
	public String getContent() throws Exception;
}
