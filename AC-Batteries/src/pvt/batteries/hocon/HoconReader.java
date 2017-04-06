package pvt.batteries.hocon;

import java.util.HashMap;
import java.util.Map.Entry;
import java.util.Set;

import com.arjunapro.testauto.interfaces.Value;
import com.typesafe.config.Config;
import com.typesafe.config.ConfigValue;

public interface HoconReader {

	void setConfig(Config loadedConf);

	void process() throws Exception;

	Config getConfig();

	HashMap<String, Value> getProperties();
	
	 void loadConfig() throws Exception;
	 
	 Set<Entry<String, ConfigValue>> getSystemPropSet();
	 Set<String> getSystemKeys();

}