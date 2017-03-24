package pvt.batteries.networker.lib.http;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.HttpHeaders;
import org.apache.http.StatusLine;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.client.methods.RequestBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.message.BasicHeader;
import org.apache.http.util.EntityUtils;

public class AcHttpRequest {
	private CloseableHttpClient httpClient = null;
	private HttpUriRequest request = null;
	
	public AcHttpRequest(CloseableHttpClient httpClient, HttpUriRequest request) throws Exception{
		this.httpClient = httpClient;
		this.request = request;
	}

	public AcHttpResponse send() throws Exception {
		CloseableHttpResponse response = httpClient.execute(request);
		return this.createResponseObject(response);
	}
	
	private AcHttpResponse createResponseObject(CloseableHttpResponse response) throws Exception{
		AcHttpResponse resp = null;
		try{
		    HttpEntity entity = response.getEntity();
		    StatusLine status = response.getStatusLine();
		    resp = new AcHttpResponse(
		    		status.getStatusCode(),
		    		status.getReasonPhrase(),
		    		response.getAllHeaders(),
		    		EntityUtils.toString(entity));	
		    EntityUtils.consume(entity);
		} finally {
			response.close();
		}
	    return resp;
	}
	
}
