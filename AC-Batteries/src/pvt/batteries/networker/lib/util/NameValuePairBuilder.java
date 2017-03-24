package pvt.batteries.networker.lib.util;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;

import pvt.batteries.networker.api.KeyValueQueue;
import pvt.batteries.networker.lib.http.AcUrlEncodedContent;

public class NameValuePairBuilder {
	HashMap<String, Integer> paramMap = null;
	List<NameValuePair> formparams = null;
	
	public NameValuePairBuilder(){
		this.initParams();
	}
	
	public void initParams(){
		paramMap = new HashMap<String, Integer>();
		formparams = new ArrayList<NameValuePair>();		
	}
	
	public void updateParam(String param, String value){
		// Updates the last occurence or adds a new key if not present
		if (paramMap.containsKey(param)){
			formparams.set(paramMap.get(param), new BasicNameValuePair(param, value));
		} else {
			this.addParam(param, value);
		}
	}
	
	public void addParam(String param, String value){
		formparams.add(new BasicNameValuePair(param, value));
		paramMap.put(param, formparams.size()-1);
	}
	
	public void addParams(HashMap<String, String> map){
		for (String k: map.keySet()){
			addParam(k, map.get(k));
		}
	}
	
	public void updateParams(HashMap<String, String> map){
		for (String k: map.keySet()){
			updateParam(k, map.get(k));
		}
	}
	
	public void setParams(HashMap<String, String> map){
		this.initParams();
		addParams(map);
	}
	
	public void addParams(KeyValueQueue map){
		KeyValuePair item = null;
		while(map.hasNext()){
			item = map.next();
			addParam(item.getName(), item.getValue());
		}
	}
	
	public void updateParams(KeyValueQueue map){
		KeyValuePair item = null;
		while(map.hasNext()){
			item = map.next();
			updateParam(item.getName(), item.getValue());
		}
	}
	
	public void setParams(KeyValueQueue map){
		this.initParams();
		addParams(map);
	}

	public void reset(){
		this.paramMap =  new HashMap<String, Integer>(); 
		this.formparams = new ArrayList<NameValuePair>();
	}
	
	public List<NameValuePair> getParamsList(){
		return this.formparams;
	}

}
