package pvt.batteries.lib;

import java.util.HashMap;
import java.util.Map;

import arjunasdk.interfaces.ReadOnlyStringKeyValueContainer;
import arjunasdk.interfaces.Value;
import pvt.batteries.config.Configuration;
import pvt.batteries.value.DefaultStringKeyValueContainer;

public class CentralConfiguration {
	private static Map<String, String> propEnumToPropPathMap = new HashMap<String, String>();
	private static BaseConfiguration centralConfig = null;
	private static Map<String, BaseConfiguration> threadMap = new HashMap<String, BaseConfiguration>();
	private static StringsManager stringsManager = null;
	private static DefaultStringKeyValueContainer execVarMap = null;
	private static DefaultStringKeyValueContainer userOptionMap = null;

	public synchronized static Value getCentralProperty(String propPath) throws Exception {
		return centralConfig.value(propPath);
	}

	public synchronized static <T extends Enum<T>> Value getCentralProperty(T propEnum) throws Exception {
		return centralConfig.value(getPropPathForEnum(propEnum));
	}

	public synchronized static boolean hasConfiguration(String configName) {
		return threadMap.containsKey(configName.toUpperCase());
	}

	public synchronized static boolean hasProperty(String configName, String path) throws Exception {
		return hasConfiguration(configName) && (threadMap.get(configName).hasKey(path.toUpperCase()));
	}

	public synchronized static void mergeConfiguration(String sourceConfigName, String targetConfigName)
			throws Exception {
		if (hasConfiguration(sourceConfigName)) {
			if (hasConfiguration(targetConfigName)) {
				threadMap.put(targetConfigName.toUpperCase(), threadMap.get(sourceConfigName.toUpperCase()).clone());
			} else {
				registerNewConfiguration(targetConfigName.toUpperCase());
				threadMap.put(targetConfigName.toUpperCase(), threadMap.get(sourceConfigName.toUpperCase()).clone());
			}
		} else {
			throw new Exception(String.format("No source configuration found for name: %s", sourceConfigName));
		}
	}

	public synchronized static void registerNewConfiguration(String configName) {
		threadMap.put(configName.toUpperCase(), new BaseConfiguration());
	}

	public static void updateThreadConfig(String configName, Configuration config) throws Exception {
		threadMap.get(configName).cloneAdd(config);
	}

	public static void setCentralProperties(BaseConfiguration configuration) {
		CentralConfiguration.centralConfig = configuration;
	}

	public static Value value(String propName) throws Exception {
		String ucPropName = propName.toUpperCase();
		if (threadMap.containsKey(Thread.currentThread().getName())
				&& threadMap.get(Thread.currentThread().getName()).hasKey(ucPropName)) {
			return threadMap.get(Thread.currentThread().getName()).value(ucPropName);
		} else if (centralConfig.hasKey(ucPropName)) {
			return centralConfig.value(ucPropName);
		} else {
			throw new Exception(String.format("No property configred for name: %s", propName));
		}
	}

	public static void setPropEnumToPropPathNameMap(Map<String, String> propEnumToPropPathMap2) {
		propEnumToPropPathMap = propEnumToPropPathMap2;
	}

	public static <T extends Enum<T>> String getPropPathForEnum(T propEnum) {
		String key = String.format("%s.%s", propEnum.getClass().getSimpleName().toUpperCase(),
				propEnum.toString().toUpperCase());
		return propEnumToPropPathMap.get(key);
	}

	public static <T extends Enum<T>> Value value(T enumObject) throws Exception {
		return value(getPropPathForEnum(enumObject));
	}

	public static String getConfiguredName(String sectionName, String internalName) throws Exception {
		return stringsManager.getConfiguredName(sectionName, internalName);
	}

	public static void setStringsManager(StringsManager mgr) {
		stringsManager = mgr;
	}

	public static String getProblemText(String problemCode) throws Exception {
		return stringsManager.getProblemText(problemCode);
	}

	public static String getInfoMessageText(String code) throws Exception {
		return stringsManager.getInfoMessageText(code);
	}

	public static Configuration getCentralConfiguration() {
		return CentralConfiguration.centralConfig;
	}

	public static void setCentralexecVarMap(DefaultStringKeyValueContainer execVarMap) {
		CentralConfiguration.execVarMap = execVarMap;
	}

	public static void setCentralUserOptionMap(DefaultStringKeyValueContainer userOptionMap) throws Exception {
		CentralConfiguration.userOptionMap = userOptionMap;
	}
	
	public static DefaultStringKeyValueContainer cloneCentralExecVars() throws Exception {
		DefaultStringKeyValueContainer container = new DefaultStringKeyValueContainer();
		container.cloneAdd(CentralConfiguration.execVarMap.items());
		return container;
	}
	
	public static DefaultStringKeyValueContainer cloneUserOptions() throws Exception {
		DefaultStringKeyValueContainer container = new DefaultStringKeyValueContainer();
		container.cloneAdd(CentralConfiguration.userOptionMap.items());
		return container;
	}
	
	public static ReadOnlyStringKeyValueContainer userOptions() throws Exception {
		return CentralConfiguration.userOptionMap;
	}
}
