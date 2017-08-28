package pvt.batteries.hocon;

import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import com.typesafe.config.Config;
import com.typesafe.config.ConfigValue;

import arjunasdk.interfaces.Value;

public interface HoconReader {

	void setConfig(Config loadedConf);

	void process() throws Exception;

	Config getConfig();

	Map<String, Value> getProperties();
	
	 void loadConfig() throws Exception;
	 
	 Set<Entry<String, ConfigValue>> getSystemPropSet();
	 Set<String> getSystemKeys();

}