package com.autocognite.pvt.batteries.networker.lib.http;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.Header;
import org.apache.http.HttpHost;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.config.RequestConfig.Builder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicHeader;

import com.autocognite.pvt.batteries.networker.api.NetworkProtocol;
import com.autocognite.pvt.batteries.networker.lib.util.KeyValuePair;

public class AcHttpRequesterBuilder {
	private CloseableHttpClient httpClient = null;
	private RequestConfig config = null;
	private AcProxies proxies = new AcProxies();
	List<Header> headers = new ArrayList<Header>();
	Builder configBuilder = RequestConfig.custom();
	
	public AcHttpRequesterBuilder(){
		switchToDefaultConfig();		
	}
	
	public AcHttpRequesterBuilder setProxy(String proxyHost, int port, NetworkProtocol prot){
		if (proxies == null){
			proxies = new AcProxies();
		}
		proxies.add(proxyHost, port, prot);
		this.setProxy(this.proxies);
		return this;
	}
	
	public AcHttpRequesterBuilder setProxy(AcProxies proxies){
		this.proxies = proxies;
		for (HttpHost proxy: proxies.getProxies()){
			configBuilder.setProxy(proxy);
		}
		config = configBuilder.build();
		return this;		
	}
	
	public AcHttpRequesterBuilder switchOnProxy(){
		this.setProxy(this.proxies);
		return this;
	}
	
	public AcHttpRequesterBuilder switchToDefaultProxy(){
		this.proxies = new AcProxies();
		proxies.add("localhost", 9999, NetworkProtocol.HTTP);
		//proxies.add("localhost", 9999, NetworkProtocol.HTTPS); <--- Yeh fajlu hai. Causes hang with HttpClient.	
		this.setProxy(this.proxies);
		return this;
	}
	
	public AcHttpRequesterBuilder switchOffProxy(){
		configBuilder.setProxy(null);
		config = configBuilder.build();		
		return this;
	}
	
	public AcHttpRequesterBuilder switchToDefaultConfig(){
		this.config = RequestConfig.DEFAULT;
		return this;
	}
	
	public AcHttpRequester build(){
		httpClient = HttpClients.
				custom()
				.setDefaultRequestConfig(this.config)
				.build();
		return new AcHttpRequester(httpClient, headers);
	}

	public AcHttpRequesterBuilder setHeader(String header, String value) {
		headers.add(new BasicHeader(header, value));
		return this;
	}
	
	public AcHttpRequesterBuilder setHeaders(AcHttpHeaders headers) {
		while(headers.hasNext()){
			KeyValuePair header = headers.next();
			this.setHeader(header.getName(), header.getValue());
		}
		return this;
	}
}
