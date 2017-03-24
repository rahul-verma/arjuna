package pvt.batteries.networker.lib.http;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.http.HttpHost;

import pvt.batteries.networker.api.NetworkProtocol;
import pvt.batteries.networker.lib.util.StringIntPair;

public class AcProxies {
	HashMap<NetworkProtocol, Integer> paramMap = null;
	List<HttpHost> proxies = null;
	
	public AcProxies(){
		this.initParams();
	}
	
	private void initParams(){
		paramMap = new HashMap<NetworkProtocol, Integer>();
		proxies = new ArrayList<HttpHost>();
	}
	
	public void add(String hostName, int port, NetworkProtocol prot){
		// Updates the last occurence or adds a new key if not present
		HttpHost host = new HttpHost(hostName, port, prot.toString());
		if (paramMap.containsKey(prot)){
			proxies.set(paramMap.get(prot), host);
		} else {
			proxies.add(host);
			paramMap.put(prot, proxies.size() - 1);
		}
	}
	
	public List<HttpHost> getProxies(){
		return this.proxies;
	}
}
