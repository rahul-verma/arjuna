package com.autocognite.arjuna.config;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.interfaces.ReadOnlyStringKeyValueContainer;
import com.autocognite.arjuna.interfaces.StringKeyValueContainer;
import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.arjuna.utils.ThreadBatteries;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.batteries.lib.CentralConfiguration;

public class RunConfig {

	private static String getConfigName() {
		return ThreadBatteries.getCurrentThreadName();
	}

	public synchronized static boolean exists(String path) {
		return CentralConfiguration.hasProperty(getConfigName(), path);
	}

	public synchronized static Value value(String propName) throws Exception {
		return CentralConfiguration.value(propName);
	}

	public static Logger getCentralLogger() {
		return Logger.getLogger(Batteries.getCentralLogName());
	}
	
	public static StringKeyValueContainer cloneSessionUserConfig() throws Exception {
		return Batteries.cloneCentralUserConfig();
	}
	
	public static ReadOnlyStringKeyValueContainer sessionUserConfig() throws Exception {
		return Batteries.sessionUserConfig();
	}
}
