/*******************************************************************************
 * Copyright 2015-16 AutoCognite Testing Research Pvt Ltd
 * 
 * Website: www.AutoCognite.com
 * Email: support [at] autocognite.com
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/
package pvt.batteries.config;

import java.util.Map;

import org.apache.log4j.Level;

import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.ddauto.interfaces.DataReference;
import arjunasdk.interfaces.ReadOnlyStringKeyValueContainer;
import arjunasdk.interfaces.Value;
import pvt.arjunasdk.enums.BatteriesPropertyType;
import pvt.batteries.integration.ComponentConfigurator;
import pvt.batteries.lib.BatteriesConfigurator;
import pvt.batteries.lib.BatteriesSingleton;
import pvt.batteries.lib.CentralConfiguration;
import pvt.batteries.lib.ComponentIntegrator;
import pvt.batteries.value.DefaultStringKeyValueContainer;

public class Batteries {
	public static boolean logFileDiscoveryInfo = false;
	private static ComponentIntegrator integrator = new ComponentIntegrator();

	public static void addConfigurator(ComponentConfigurator configurator) {
		configurator.setIntegrator(integrator);
		configurator.setBaseDir(integrator.getBaseDir());
		integrator.addConfigurator(configurator);
	}

	public static void init() throws Exception {
		integrator.init();
		Batteries.addConfigurator(new BatteriesConfigurator());
	}

	public static void init(String baseDir) throws Exception {
		integrator.init(baseDir);
		Batteries.addConfigurator(new BatteriesConfigurator());
	}

	public static String getBaseDir() {
		return integrator.getBaseDir();
	}
	
	public static String getProjectDir() {
		return integrator.getProjectDir();
	}

	public static void processArjunaDefaults() throws Exception {
		integrator.processDefaults();
	}

	public static void processArjunaOptions(Map<String, Value> properties) throws Exception {
		integrator.processConfigProperties(properties);
	}

	public static void processCentralExecVars(Map<String, Value> properties) {
		integrator.processCentralExecVars(properties);
	}
	
	public static void processCentralUserOptions(Map<String, Value> properties) {
		integrator.processCentralUserOptions(properties);
	}

	public static void freezeCentralConfig() throws Exception {
		Configuration configuration = integrator.freezeCentralConfig();
	}

	public static class info {
		public static final String EXIT_ON_ERROR = "message.exit.on.error";
	}
	
	public synchronized static DefaultStringKeyValueContainer cloneCentralExecVars() throws Exception {
		return CentralConfiguration.cloneCentralExecVars();
	}
	
	public synchronized static DefaultStringKeyValueContainer cloneCentralUserOptions() throws Exception {
		return CentralConfiguration.cloneUserOptions();
	}
	
	public synchronized static ReadOnlyStringKeyValueContainer sessionUserOptions() throws Exception {
		return CentralConfiguration.userOptions();
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
		return "arjuna";
	}

	public static Level getDisplayLevel() throws Exception {
		return Level.toLevel(Batteries.getCentralProperty(BatteriesPropertyType.LOGGING_CONSOLE_LEVEL).asString());
	}

	public static Level getLogLevel() throws Exception {
		return Level.toLevel(Batteries.getCentralProperty(BatteriesPropertyType.LOGGING_FILE_LEVEL).asString());
	}

	public static String getLogDir() throws Exception {
		return Batteries.getCentralProperty(BatteriesPropertyType.DIRECTORY_PROJECT_LOG).asString();
	}
	
	public static DataRecord getDataRecord(String refFileName, String key) throws Exception {
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
	
	public synchronized static void registerThread(String parentThreadName, String threadName) throws Exception {
		CentralConfiguration.mergeConfiguration(parentThreadName, threadName);
	}

	public synchronized static void updateThreadConfig(String threadName, Configuration config) throws Exception {
		CentralConfiguration.updateThreadConfig(threadName, config);
	}
}
