package pvt.batteries.networker.lib.http;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.message.BasicNameValuePair;

import pvt.batteries.networker.api.KeyValueQueue;
import pvt.batteries.networker.api.http.AcUrl;
import pvt.batteries.networker.lib.util.NameValuePairBuilder;
import pvt.batteries.networker.lib.util.QueryData;

public class AcUrlBuilder {
	private URIBuilder uri = null;
	private NameValuePairBuilder nvpBuilder = null;
	boolean relative = false;
	
	public AcUrlBuilder(){
		this.uri = new URIBuilder();
		this.nvpBuilder = new NameValuePairBuilder();
		this.initialize();
	}
	
	private void initialize(){
		this.setProtocol("http");
		this.setHost(null);
		this.setPath("");	
	}

	public AcUrlBuilder setRelativeMode(boolean mode){
		this.relative = mode;
		return this;
	}
	
	public AcUrlBuilder setProtocol(String prot){
		this.uri.setScheme(prot);
		return this;
	}
	
	public AcUrlBuilder setHost(String host){
		this.uri.setHost(host);
		return this;
	}	
	
	public AcUrlBuilder setPath(String path){
		this.uri.setPath(path);
		return this;
	}	
	
	public AcUrlBuilder resetParams(){
		this.nvpBuilder.initParams();
		uri.clearParameters();
		return this;
	}
	
	public AcUrlBuilder reset(){
		this.initialize();
		this.resetParams();
		return this;
	}
	
	public AcUrlBuilder updateParam(String param, String value){
		this.nvpBuilder.updateParam(param, value);
		return this;
	}
	
	public AcUrlBuilder addParam(String param, String value){
		this.nvpBuilder.addParam(param, value);
		return this;
	}
	
	public AcUrlBuilder addParams(HashMap<String, String> map){
		this.nvpBuilder.addParams(map);
		return this;
	}
	
	public AcUrlBuilder updateParams(HashMap<String, String> map){
		this.nvpBuilder.updateParams(map);
		return this;
	}
	
	public AcUrlBuilder setParams(HashMap<String, String> map){
		this.nvpBuilder.initParams();
		return addParams(map);
	}
	
	public AcUrlBuilder addParams(QueryData map){
		this.nvpBuilder.addParams(map);
		return this;
	}
	
	public AcUrlBuilder updateParams(QueryData map){
		this.nvpBuilder.updateParams(map);
		return this;
	}
	
	public AcUrlBuilder setParams(QueryData map){
		this.nvpBuilder.initParams();
		return addParams(map);
	}
	public AcUrl getUrl() throws Exception{
		return this._getUrl(uri.getHost(), this.relative);
	}
	
	public AcUrl getRelativeUrl() throws Exception{
		return this._getUrl(uri.getHost(), true);
	}
	
	private AcUrl _getUrl(String host, boolean shouldBeRelative) throws Exception{
		List<NameValuePair> params = this.nvpBuilder.getParamsList();
		if (params.size() != 0){
			uri.setParameters(params);
		}

		if (host == null){
			if (shouldBeRelative){
				uri.setHost("temp");
				String u = uri.build().toString();
				AcDefaultUrl url = new AcDefaultUrl(u.substring(u.indexOf("temp") + 4));
				uri.setHost(null);
				return url;
			} else {
					throw new Exception("Host was found to be null. You can create a URL without host name.");
			}
		} else {
			if (shouldBeRelative){
				String host1 = uri.getHost();
				String u = uri.build().toString();
				return new AcDefaultUrl(u.substring(u.indexOf(host1) + host1.length()));
			} else {
				return new AcDefaultUrl(uri.build());
			}
		}
		
	}
}
