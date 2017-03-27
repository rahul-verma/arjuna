package pvt.batteries.networker.lib.http;


import java.util.HashMap;

import org.apache.http.Consts;
import org.apache.http.HttpEntity;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.util.EntityUtils;

import pvt.batteries.networker.api.KeyValueQueue;
import pvt.batteries.networker.api.http.AcHttpContent;
import pvt.batteries.networker.lib.util.FormData;
import pvt.batteries.networker.lib.util.NameValuePairBuilder;

public class AcUrlEncodedContent implements AcHttpContent{
	private UrlEncodedFormEntity myEntity = null;
	private NameValuePairBuilder nvpBuilder = null;
	
	public AcUrlEncodedContent(){
		this.nvpBuilder = new NameValuePairBuilder();
	}
	
	public AcUrlEncodedContent updateParam(String param, String value){
		this.nvpBuilder.updateParam(param, value);
		return this;
	}
	
	public AcUrlEncodedContent addParam(String param, String value){
		this.nvpBuilder.addParam(param, value);
		return this;
	}
	
	public AcUrlEncodedContent addParams(HashMap<String, String> map){
		this.nvpBuilder.addParams(map);
		return this;
	}
	
	public AcUrlEncodedContent updateParams(HashMap<String, String> map){
		this.nvpBuilder.updateParams(map);
		return this;
	}
	
	public AcUrlEncodedContent setParams(HashMap<String, String> map){
		this.nvpBuilder.initParams();
		return addParams(map);
	}
	
	public AcUrlEncodedContent addParams(FormData map){
		this.nvpBuilder.addParams(map);
		return this;
	}
	
	public AcUrlEncodedContent updateParams(FormData map){
		this.nvpBuilder.updateParams(map);
		return this;
	}
	
	public AcUrlEncodedContent setParams(FormData map){
		this.nvpBuilder.initParams();
		return addParams(map);
	}

	public AcUrlEncodedContent reset(){
		this.myEntity = null;
		this.nvpBuilder.initParams();
		return this;
	}
	
	@Override
	public HttpEntity getContentEntity() {
		this.myEntity = new UrlEncodedFormEntity(this.nvpBuilder.getParamsList(), Consts.UTF_8);
		return this.myEntity;
	}

	@Override
	public String getContent() throws Exception {
		if (this.myEntity == null){
			this.myEntity = new UrlEncodedFormEntity(this.nvpBuilder.getParamsList(), Consts.UTF_8);
		}
		return EntityUtils.toString(myEntity);
	}

}
