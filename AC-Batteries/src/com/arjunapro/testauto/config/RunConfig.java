package com.arjunapro.testauto.config;

import org.apache.log4j.Logger;

import com.arjunapro.sysauto.batteries.ThreadBatteries;
import com.arjunapro.testauto.interfaces.ReadOnlyStringKeyValueContainer;
import com.arjunapro.testauto.interfaces.StringKeyValueContainer;
import com.arjunapro.testauto.interfaces.Value;

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
