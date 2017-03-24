package pvt.batteries.networker.lib.http;

import java.util.HashMap;

import org.apache.http.Header;

public class AcHttpResponse {

	private int responseCode = -1;
	private String responseDesc = null;
	private HashMap<String, String> responseHeaders = new HashMap<String, String>();
	private String body = null;
	
	public AcHttpResponse(int code, String responseDesc, Header[] headers, String content){
		this.responseCode = code;
		this.responseDesc = responseDesc;
		for (Header header: headers){
			this.responseHeaders.put(header.getName(), header.getValue());
		}
		this.body = content;
	}

	public int getCode() {
		return responseCode;
	}
	
	public String getDesc() {
		return responseDesc;
	}
	
	public String getHeader(String header){
		return this.responseHeaders.get(header);
	}
	
	public HashMap<String, String> getHeaders(){
		return this.responseHeaders;
	}
	
	public String getContent(){
		return this.body;
	}
}
