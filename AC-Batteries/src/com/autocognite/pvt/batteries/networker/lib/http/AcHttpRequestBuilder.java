package com.autocognite.pvt.batteries.networker.lib.http;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.client.methods.RequestBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.message.BasicHeader;

import com.autocognite.pvt.batteries.networker.api.http.AcHttpContent;

public class AcHttpRequestBuilder {
	private CloseableHttpClient httpClient = null;
	List<Header> headers = null;
	private AcHttpMethod method = null;
	private String url = null;
	private HttpEntity entity = null;
	private List<Header> defaultHeaders = null;
	
	public AcHttpRequestBuilder(CloseableHttpClient client){
		this.httpClient = client;
		this.reset();
	}
	
	public AcHttpRequestBuilder reset(){
		this.headers = new ArrayList<Header>();
		//this.url = null;
		this.method = AcHttpMethod.GET;
		this.entity = null;
		return this;
	}
	
	public AcHttpRequestBuilder setDefaultHeaders(List<Header> headers) {
		this.defaultHeaders = headers;
		return this;
	}
	
	public AcHttpRequestBuilder setHeader(String header, String value){
		headers.add(new BasicHeader(header, value));
		return this;
	}
	
	public AcHttpRequestBuilder setUrl(String url){
		this.url = url;
		return this;
	}
	
	public AcHttpRequestBuilder setMethod(AcHttpMethod method){
		this.method = method;
		return this;
	}
	
	
	public AcHttpRequestBuilder setContentEntity(AcHttpContent content){
		this.entity = content.getContentEntity();
		return this;
	}
	
	public AcHttpRequest build() throws Exception{
		if (url == null){
			throw new Exception("The url is null.");
		}
		RequestBuilder builder = null;
		switch (method){
		case GET: builder = RequestBuilder.get(); break;
		case POST: builder = RequestBuilder.post(); break;
		case PUT: builder = RequestBuilder.put(); break;
		case DELETE: builder = RequestBuilder.delete(); break;
		case PATCH: builder = RequestBuilder.patch(); break;
		default: throw new Exception(String.format("Method %s is not supported by AutoCognite-Networker.", method.toString()));
		}
		
		for(Header header: this.defaultHeaders){
			builder.setHeader(header);
		}
		
		for(Header header: headers){
			builder.setHeader(header);
		}
		
		if(this.entity != null){
			builder.setEntity(entity);
		}
		
		builder.setUri(url);
		
		return new AcHttpRequest(this.httpClient, builder.build());
		
	}

}
