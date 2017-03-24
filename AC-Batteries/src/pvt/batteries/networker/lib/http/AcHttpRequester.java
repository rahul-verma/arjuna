package pvt.batteries.networker.lib.http;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.HttpHeaders;
import org.apache.http.HttpHost;
import org.apache.http.NameValuePair;
import org.apache.http.StatusLine;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.config.RequestConfig.Builder;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpRequestBase;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.client.methods.RequestBuilder;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.config.SocketConfig;
import org.apache.http.entity.ContentType;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import pvt.batteries.networker.api.NetworkProtocol;
import pvt.batteries.networker.api.http.AcHttpContent;
import pvt.batteries.networker.lib.util.FormData;
import pvt.batteries.networker.lib.util.KeyValuePair;

public class AcHttpRequester {
	private CloseableHttpClient httpclient = null;
	private AcHttpRequestBuilder builder = null;
	
	public AcHttpRequester(CloseableHttpClient httpClient, List<Header> headers){
		this.httpclient = httpClient;
		this.builder = new AcHttpRequestBuilder(this.httpclient);
		this.builder.setDefaultHeaders(headers);
	}
	
	private void reset(){
		
	}
	
	public AcHttpRequester setUrl(String url){
		this.builder.setUrl(url);
		return this;
	}
	
	public AcHttpRequester setUrl(AcUrlBuilder urlBuilder) throws Exception{
		this.builder.setUrl(urlBuilder.getUrl().toString());
		return this;
	}
	
	public AcHttpRequester setHeader(String header, String value){
		builder.setHeader(header, value);
		return this;
	}
	
	public AcHttpRequester setHeaders(AcHttpHeaders headers) {
		while(headers.hasNext()){
			KeyValuePair header = headers.next();
			builder.setHeader(header.getName(), header.getValue());
		}
		return this;
	}
	
	private AcHttpResponse _send(AcHttpRequestBuilder builder, AcHttpMethod method) throws Exception{
		AcHttpResponse response = builder.setMethod(method).build().send();
		this.builder.reset();
		return response;		
	}
	
	public AcHttpResponse get() throws Exception {
		return this._send(this.builder, AcHttpMethod.GET);
	}
	
	public AcHttpResponse get(AcUrlBuilder urlBuilder) throws Exception {
		return this.get(urlBuilder.getUrl().toString());
	}
	
	public AcHttpResponse get(String url) throws Exception{
		return this._send(this.builder.setUrl(url), AcHttpMethod.GET);
	}
	
	public AcHttpResponse delete() throws Exception {
		return this._send(this.builder, AcHttpMethod.DELETE);
	}
	
	public AcHttpResponse delete(AcUrlBuilder urlBuilder) throws Exception {
		return this.delete(urlBuilder.getUrl().toString());
	}
	
	public AcHttpResponse delete(String url) throws Exception{
		return this._send(this.builder.setUrl(url), AcHttpMethod.DELETE);
	}
	
	public AcHttpResponse post(String content) throws Exception{
		return this.post(new AcRawHttpContent(content, ContentType.APPLICATION_FORM_URLENCODED));
	}
	
	public AcHttpResponse post(String content, ContentType type) throws Exception{
		return this.post(new AcRawHttpContent(content, type));
	}
	
	public AcHttpResponse post(HashMap<String, String> map) throws Exception{
		return this.post((new AcUrlEncodedContent()).setParams(map));
	}
	
	public AcHttpResponse post(FormData formData) throws Exception{
		return this.post((new AcUrlEncodedContent()).setParams(formData));
	}
	
	public AcHttpResponse post(AcHttpContent content) throws Exception{
		if (content != null){
			builder.setContentEntity(content);
		}
		return this._send(this.builder, AcHttpMethod.POST);
	}
	
	public AcHttpResponse put(String content) throws Exception{
		return this.put(new AcRawHttpContent(content, ContentType.APPLICATION_FORM_URLENCODED));
	}
	
	public AcHttpResponse put(String content, ContentType type) throws Exception{
		return this.put(new AcRawHttpContent(content, type));
	}
	
	public AcHttpResponse put(HashMap<String, String> map) throws Exception{
		return this.put((new AcUrlEncodedContent()).setParams(map));
	}
	
	public AcHttpResponse put(FormData formData) throws Exception{
		return this.put((new AcUrlEncodedContent()).setParams(formData));
	}
	
	public AcHttpResponse put(AcHttpContent content) throws Exception{
		if (content != null){
			builder.setContentEntity(content);
		}
		return this._send(this.builder, AcHttpMethod.PUT);
	}
	
	public AcHttpResponse patch(String content) throws Exception{
		return this.patch(new AcRawHttpContent(content, ContentType.APPLICATION_FORM_URLENCODED));
	}
	
	public AcHttpResponse patch(String content, ContentType type) throws Exception{
		return this.patch(new AcRawHttpContent(content, type));
	}
	
	public AcHttpResponse patch(HashMap<String, String> map) throws Exception{
		return this.patch((new AcUrlEncodedContent()).setParams(map));
	}
	
	public AcHttpResponse patch(FormData formData) throws Exception{
		return this.patch((new AcUrlEncodedContent()).setParams(formData));
	}
	
	public AcHttpResponse patch(AcHttpContent content) throws Exception{
		if (content != null){
			builder.setContentEntity(content);
		}
		return this._send(this.builder, AcHttpMethod.PATCH);
	}

}
