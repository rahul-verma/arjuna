package arjunasdk.config;

import org.apache.log4j.Logger;

import arjunasdk.interfaces.ReadOnlyStringKeyValueContainer;
import arjunasdk.interfaces.StringKeyValueContainer;
import arjunasdk.interfaces.Value;
import arjunasdk.sysauto.batteries.ThreadBatteries;
import pvt.batteries.config.Batteries;
import pvt.batteries.lib.CentralConfiguration;

public class RunConfig {

	private static String getConfigName() {
		return ThreadBatteries.getCurrentThreadName();
	}

	public synchronized static boolean exists(String path) throws Exception {
		return CentralConfiguration.hasProperty(getConfigName(), path);
	}

	public synchronized static Value value(String propName) throws Exception {
		return CentralConfiguration.value(propName);
	}

	public static Logger logger() {
		return Logger.getLogger(Batteries.getCentralLogName());
	}
	
	public static StringKeyValueContainer cloneUserConfig() throws Exception {
		return Batteries.cloneCentralUserConfig();
	}
	
	public static ReadOnlyStringKeyValueContainer userConfig() throws Exception {
		return Batteries.sessionUserConfig();
	}
}
