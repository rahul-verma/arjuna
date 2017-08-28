package pvt.batteries.lib;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

import arjunasdk.enums.LoggingLevel;
import arjunasdk.interfaces.Value;
import pvt.arjunasdk.enums.BatteriesPropertyType;
import pvt.arjunasdk.property.ConfigProperty;
import pvt.arjunasdk.property.ConfigPropertyBatteries;
import pvt.arjunasdk.property.ConfigPropertyBuilder;
import pvt.batteries.config.Batteries;
import pvt.batteries.ds.Message;
import pvt.batteries.ds.MessagesContainer;
import pvt.batteries.ds.Name;
import pvt.batteries.ds.NamesContainer;
import pvt.batteries.hocon.HoconReader;
import pvt.batteries.hocon.HoconResourceReader;
import pvt.batteries.integration.AbstractComponentConfigurator;

public class BatteriesConfigurator extends AbstractComponentConfigurator {
	private ConfigPropertyBuilder<BatteriesPropertyType> builder = new ConfigPropertyBuilder<BatteriesPropertyType>();
	private Map<String, BatteriesPropertyType> pathToEnumMap = new HashMap<String, BatteriesPropertyType>();
	private Map<BatteriesPropertyType, String> enumToPathMap = new HashMap<BatteriesPropertyType, String>();

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
		try{
			ConfigProperty prop = ConfigPropertyBatteries.createEnumProperty(codeForPath(propPath), propPath,
					LoggingLevel.class, configValue, purpose, visible);
			registerProperty(prop);
		} catch (Exception e){
			throw new Exception("Error in processing Logging Level configuration: " + e.getMessage());
		}
	}

	protected void handleBooleanConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception {
		ConfigProperty prop = ConfigPropertyBatteries.createBooleanProperty(codeForPath(propPath), propPath,
				configValue, purpose, visible);
		registerProperty(prop);
	}

	@SuppressWarnings("unchecked")
	public void processConfigProperties(Map<String, Value> properties) throws Exception {
		Set<String> keys = properties.keySet();
		Iterator<String> iter = keys.iterator();
		List<String> handledProps = new ArrayList<String>();
		while(iter.hasNext()) {
			String propPath = iter.next();
			String ucPropPath = propPath.toUpperCase();
			Value cValue = properties.get(propPath);
			if (pathToEnumMap.containsKey(ucPropPath)) {
				switch (pathToEnumMap.get(ucPropPath)) {
				case CONFIG_CENTRAL_FILE_NAME:
					handleStringConfig(propPath, cValue, "Central Configuration File", false);
					break;
				case DIRECTORY_PROJECT_ROOT:
					handleCoreDirPath(propPath, cValue, "Configuration Directory", false);
					break;
				case DIRECTORY_CONFIG:
					handleCoreDirPath(propPath, cValue, "Configuration Directory", false);
					break;
				case DIRECTORY_PROJECT_DATA_REFERENCES:
					handleProjectDirPath(propPath, cValue, "Data References Directory", false);
					break;
				case DIRECTORY_PROJECT_DATA_ROOT:
					handleProjectDirPath(propPath, cValue, "Data Directory", false);
					break;
				case DIRECTORY_PROJECT_DATA_SOURCES:
					handleProjectDirPath(propPath, cValue, "Data Sources Directory", false);
					break;
				case DIRECTORY_PROJECT_LOG:
					handleProjectDirPath(propPath, cValue, "Log Directory", false);
					break;
				case DIRECTORY_PROJECT_SCREENSHOTS:
					handleProjectDirPath(propPath, cValue, "Screenshots Directory", false);
					break;
				case DIRECTORY_PROJECT_TEMP:
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
				case LOGGING_NAME:
					builder.overridable(false).visible(false);
					handleStringConfig(propPath, cValue, "AutoCognite Log file name", false);
					break;
				case LOGGING_FILE_ON:
					handleBooleanConfig(propPath, cValue, "Should log to file?", true);
					break;
				default:
					break;

				}

				handledProps.add(propPath);
			}
		}

		for(String prop: handledProps){
			properties.remove(prop);
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

	public List<MessagesContainer> getAllMessages() {
		List<MessagesContainer> containers = new ArrayList<MessagesContainer>();

		MessagesContainer infoMessages = new MessagesContainer("INFO_MESSAGES");
		infoMessages.add(new Message(Batteries.info.EXIT_ON_ERROR, "Critical Error. Exiting."));
		containers.add(infoMessages);

		return containers;
	}

	public List<NamesContainer> getAllNames() {
		List<NamesContainer> containers = new ArrayList<NamesContainer>();

		NamesContainer objectNames = new NamesContainer("COMPONENT_NAMES");

		objectNames.add(new Name("DATA_SOURCE", "Data Source"));

		containers.add(objectNames);

		return containers;
	}
}
