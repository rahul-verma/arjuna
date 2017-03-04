package com.autocognite.batteries.config;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;

import com.autocognite.batteries.databroker.DataReference;
import com.autocognite.batteries.databroker.ReadOnlyDataRecord;
import com.autocognite.batteries.util.ThreadBatteries;
import com.autocognite.batteries.value.StringKeyValueContainer;
import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.batteries.config.Configuration;
import com.autocognite.pvt.batteries.enums.BatteriesPropertyType;
import com.autocognite.pvt.batteries.lib.BatteriesSingleton;
import com.autocognite.pvt.batteries.lib.CentralConfiguration;

public class RunConfig {

	private static String getConfigName() {
		return ThreadBatteries.getCurrentThreadName();
	}

	public synchronized static boolean propExists(String path) {
		return CentralConfiguration.hasProperty(getConfigName(), path);
	}

	public synchronized static void registerThread(String parentThreadName, String threadName) throws Exception {
		CentralConfiguration.mergeConfiguration(parentThreadName, threadName);
	}

	public synchronized static void updateThreadConfig(String threadName, Configuration config) throws Exception {
		CentralConfiguration.updateThreadConfig(threadName, config);
	}

	public synchronized static StringKeyValueContainer cloneCentralUDVs() throws Exception {
		return CentralConfiguration.cloneCentralUDVs();
	}

	public synchronized static Value value(String propName) throws Exception {
		return CentralConfiguration.value(propName);
	}

	public synchronized static <T extends Enum<T>> Value value(T enumObject) throws Exception {
		return CentralConfiguration.value(enumObject);
	}

	public static <T extends Enum<T>> Value getCentralProperty(T enumObj) throws Exception {
		return CentralConfiguration.getCentralProperty(enumObj);
	}

	public static <T extends Enum<T>> String getPropPathForEnum(T propEnum) {
		return CentralConfiguration.getPropPathForEnum(propEnum);
	}

	public static String getCentralLogName() {
		return "autocognite";
	}

	public static Logger getCentralLogger() {
		return Logger.getLogger(getCentralLogName());
	}

	public static Level getDisplayLevel() throws Exception {
		return Level.toLevel(RunConfig.getCentralProperty(BatteriesPropertyType.LOGGING_CONSOLE_LEVEL).asString());
	}

	public static Level getLogLevel() throws Exception {
		return Level.toLevel(RunConfig.getCentralProperty(BatteriesPropertyType.LOGGING_FILE_LEVEL).asString());
	}

	public static String getLogDir() throws Exception {
		return RunConfig.getCentralProperty(BatteriesPropertyType.DIRECTORY_LOG).asString();
	}

	public static ReadOnlyDataRecord getDataRecord(String refFileName, String key) throws Exception {
		return BatteriesSingleton.INSTANCE.getDataRecord(refFileName, key);
	}

	public static String getConfiguredName(String sectionName, String internalName) throws Exception {
		return CentralConfiguration.getConfiguredName(sectionName, internalName);
	}

	public static String getProblemText(String problemCode, Object... args) throws Exception {
		return String.format(CentralConfiguration.getProblemText(problemCode), args);
	}

	public static String getComponentName(String name) throws Exception {
		return getConfiguredName("COMPONENT_NAMES", name);
	}

	public static String getInfoMessageText(String code, Object... args) throws Exception {
		return String.format(CentralConfiguration.getInfoMessageText(code), args);
	}

	public static Configuration getCentralConfig() {
		return CentralConfiguration.getCentralConfiguration();
	}

	public static void registerNewThread(String threadName) {
		CentralConfiguration.registerNewConfiguration(threadName);
	}

	public static DataReference getDataReference(String refName) throws Exception {
		return BatteriesSingleton.INSTANCE.getDataReference(refName);
	}
}
