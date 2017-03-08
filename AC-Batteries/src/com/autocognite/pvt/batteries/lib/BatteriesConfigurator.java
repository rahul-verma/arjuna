package com.autocognite.pvt.batteries.lib;

import java.util.ArrayList;
import java.util.HashMap;

import com.autocognite.arjuna.enums.LoggingLevel;
import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.batteries.ds.Message;
import com.autocognite.pvt.batteries.ds.MessagesContainer;
import com.autocognite.pvt.batteries.ds.Name;
import com.autocognite.pvt.batteries.ds.NamesContainer;
import com.autocognite.pvt.batteries.enums.BatteriesPropertyType;
import com.autocognite.pvt.batteries.hocon.HoconReader;
import com.autocognite.pvt.batteries.hocon.HoconResourceReader;
import com.autocognite.pvt.batteries.integration.AbstractComponentConfigurator;
import com.autocognite.pvt.batteries.property.ConfigProperty;
import com.autocognite.pvt.batteries.property.ConfigPropertyBatteries;
import com.autocognite.pvt.batteries.property.ConfigPropertyBuilder;

public class BatteriesConfigurator extends AbstractComponentConfigurator {
	private ConfigPropertyBuilder<BatteriesPropertyType> builder = new ConfigPropertyBuilder<BatteriesPropertyType>();
	private HashMap<String, BatteriesPropertyType> pathToEnumMap = new HashMap<String, BatteriesPropertyType>();
	private HashMap<BatteriesPropertyType, String> enumToPathMap = new HashMap<BatteriesPropertyType, String>();

	public BatteriesConfigurator() {
		super("Batteries");
		for (BatteriesPropertyType e : BatteriesPropertyType.class.getEnumConstants()) {
			String path = ConfigPropertyBatteries.enumToPropPath(e);
			pathToEnumMap.put(path.toUpperCase(), e);
			enumToPathMap.put(e, path.toUpperCase());
		}
	}

	private BatteriesPropertyType codeForPath(String propPath) {
		return pathToEnumMap.get(propPath.toUpperCase());
	}

	protected void handleStringConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception {
		ConfigProperty prop = ConfigPropertyBatteries.createStringProperty(codeForPath(propPath), propPath, configValue,
				purpose, visible);
		registerProperty(prop);
	}

	protected void handleCoreDirPath(String propPath, Value configValue, String purpose, boolean visible) throws Exception {
		ConfigProperty prop = ConfigPropertyBatteries.createCoreDirPath(codeForPath(propPath), propPath,
				configValue, purpose, visible);
		registerProperty(prop);
	}
	
	protected void handleProjectDirPath(String propPath, Value configValue, String purpose, boolean visible) throws Exception {
		ConfigProperty prop = ConfigPropertyBatteries.createProjectDirPath(codeForPath(propPath), propPath,
				configValue, purpose, visible);
		registerProperty(prop);
	}

	protected void handleLogLevelConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception {
		ConfigProperty prop = ConfigPropertyBatteries.createEnumProperty(codeForPath(propPath), propPath,
				LoggingLevel.class, configValue, purpose, visible);
		registerProperty(prop);
	}

	protected void handleBooleanConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception {
		ConfigProperty prop = ConfigPropertyBatteries.createBooleanProperty(codeForPath(propPath), propPath,
				configValue, purpose, visible);
		registerProperty(prop);
	}

	@SuppressWarnings("unchecked")
	public void processConfigProperties(HashMap<String, Value> properties) throws Exception {
		HashMap<String, Value> tempMap = (HashMap<String, Value>) properties.clone();
		for (String propPath : tempMap.keySet()) {
			String ucPropPath = propPath.toUpperCase();
			Value cValue = tempMap.get(propPath);
			if (pathToEnumMap.containsKey(ucPropPath)) {
				switch (pathToEnumMap.get(ucPropPath)) {
				case CONFIG_FILE_NAME:
					handleStringConfig(propPath, cValue, "Central Configuration File", false);
					break;
				case DIRECTORY_PROJECT:
					handleCoreDirPath(propPath, cValue, "Configuration Directory", false);
					break;
				case DIRECTORY_CONFIG:
					handleCoreDirPath(propPath, cValue, "Configuration Directory", false);
					break;
				case DIRECTORY_DATA_REFERENCES:
					handleProjectDirPath(propPath, cValue, "Data References Directory", false);
					break;
				case DIRECTORY_DATA_ROOT:
					handleProjectDirPath(propPath, cValue, "Data Directory", false);
					break;
				case DIRECTORY_DATA_SOURCES:
					handleProjectDirPath(propPath, cValue, "Data Sources Directory", false);
					break;
				case DIRECTORY_LOG:
					handleProjectDirPath(propPath, cValue, "Log Directory", false);
					break;
				case DIRECTORY_SCREENSHOTS:
					handleProjectDirPath(propPath, cValue, "Screenshots Directory", false);
					break;
				case DIRECTORY_TEMP:
					handleProjectDirPath(propPath, cValue, "Temporary Directory", false);
					break;
				case DIRECTORY_TOOLS_ROOT:
					handleProjectDirPath(propPath, cValue, "Tools Directory", false);
					break;
				case LOGGING_CONSOLE_LEVEL:
					handleLogLevelConfig(propPath, cValue, "Minimum Logging Message Level for Console Display", true);
					break;
				case LOGGING_CONSOLE_ON:
					handleBooleanConfig(propPath, cValue, "Should display logging messages on console?", true);
					break;
				case LOGGING_FILE_LEVEL:
					handleLogLevelConfig(propPath, cValue, "Minimum Logging Message Level for File Log", true);
					break;
				case LOGGING_FILE_NAME:
					builder.overridable(false).visible(false);
					handleStringConfig(propPath, cValue, "AutoCognite Log file name", false);
					break;
				case LOGGING_FILE_ON:
					handleBooleanConfig(propPath, cValue, "Should log to file?", true);
					break;
				default:
					break;

				}

				properties.remove(propPath);
			}
		}

	}

	public void processDefaults() throws Exception {
		HoconReader reader = new HoconResourceReader(this.getClass().getResourceAsStream("/com/autocognite/pvt/text/batteries.conf"));
		super.processDefaults(reader);
	}

	@Override
	public void loadComponent() throws Exception {
		BatteriesSingleton.INSTANCE.loadDataReferences();
	}

	public ArrayList<MessagesContainer> getAllMessages() {
		ArrayList<MessagesContainer> containers = new ArrayList<MessagesContainer>();

		MessagesContainer infoMessages = new MessagesContainer("INFO_MESSAGES");
		infoMessages.add(new Message(Batteries.info.EXIT_ON_ERROR, "Critical Error. Exiting."));
		containers.add(infoMessages);

		return containers;
	}

	public ArrayList<NamesContainer> getAllNames() {
		ArrayList<NamesContainer> containers = new ArrayList<NamesContainer>();

		NamesContainer objectNames = new NamesContainer("COMPONENT_NAMES");

		objectNames.add(new Name("DATA_SOURCE", "Data Source"));

		containers.add(objectNames);

		return containers;
	}
}
