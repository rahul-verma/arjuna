package com.autocognite.pvt.batteries.lib;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.autocognite.arjuna.enums.ValueType;
import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.arjuna.utils.FileSystemBatteries;
import com.autocognite.pvt.batteries.config.Configuration;
import com.autocognite.pvt.batteries.console.Console;
import com.autocognite.pvt.batteries.ds.MessagesContainer;
import com.autocognite.pvt.batteries.ds.NamesContainer;
import com.autocognite.pvt.batteries.integration.ComponentConfigurator;
import com.autocognite.pvt.batteries.property.ConfigProperty;
import com.autocognite.pvt.batteries.value.DefaultStringKeyValueContainer;

public class ComponentIntegrator {
	private String refDir = null;
	private String projDir = null;
	private List<ComponentConfigurator> configurators = new ArrayList<ComponentConfigurator>();
	private HashMap<String, ComponentConfigurator> configuratorMap = new HashMap<String, ComponentConfigurator>();
	private HashMap<String, String> propEnumToPropPathMap = new HashMap<String, String>();
	private HashMap<String, String> propNameToComponentMap = new HashMap<String, String>();
	private HashMap<String, ValueType> propNameExpectedTypeMap = new HashMap<String, ValueType>();
	private HashMap<String, ConfigProperty> fworkProperties = new HashMap<String, ConfigProperty>();
	private Set<String> overrideableProperties = new HashSet<String>();
	private Set<String> visiableProperties = new HashSet<String>();
	private HashMap<String, String> readableNames = new HashMap<String, String>();
	private StringsManager stringsManager = new StringsManager();
	private DefaultStringKeyValueContainer udvMap = new DefaultStringKeyValueContainer();

	public void init() {
		setRefDir(FileSystemBatteries.getJarFilePathForObject(this));
	}

	public void init(String refDir) {
		this.refDir = refDir;
	}
	
	public String getProjectDir() {
		return this.projDir;
	}
	
	public void setProjectDir(String dir) {
		this.projDir = dir;
	}

	public void addConfigurator(ComponentConfigurator configurator) {
		configurators.add(configurator);
		configuratorMap.put(configurator.getComponentName().toUpperCase(), configurator);
	}

	public void processDefaults() throws Exception {
		// Configuration config = new Configuration();
		// UserDefinedConfig userConfig = new UserDefinedConfig();
		for (ComponentConfigurator configurator : configurators) {
			configurator.processDefaults();
		}
	}

	private <T extends Enum<T>> String getKeyNameForEnumConstant(T enumConst) {
		return String.format("%s.%s", enumConst.getClass().getSimpleName(), enumConst.toString());

	}

	public void registerProperty(String componentName, ConfigProperty property) throws Exception {
		String ucComponentName = componentName.toUpperCase();
		if (!this.configuratorMap.containsKey(ucComponentName)) {
			throw new Exception(String.format("No configurator found for component: %s", componentName));
		}
		if (property.value() == null) {
			throw new Exception(String.format("%s supplied null value for %s", componentName, property.path()));
		}
		String propName = property.path();
		propNameToComponentMap.put(propName, componentName);
		propEnumToPropPathMap
				.put(String.format("%s.%s", property.definer().toUpperCase(), property.code().toUpperCase()), propName);
		fworkProperties.put(propName, property);
		propNameExpectedTypeMap.put(propName, property.expectedValueType());
		readableNames.put(propName, property.text());

		if (property.overridable()) {
			overrideableProperties.add(propName);
		}

		if (property.visible()) {
			visiableProperties.add(propName);
		}
	}

	public void enumerate() throws Exception {
		List<String> keys = new ArrayList<String>();
		keys.addAll(fworkProperties.keySet());
		Collections.sort(keys);
		Console.marker(100);
		String header = " Central Properties Table ";
		int markLength = ((100 - header.length()) / 2);
		Console.markerOnSameLine(markLength);
		Console.displayOnSameLine(header);
		Console.marker(markLength);
		Console.marker(100);
		for (String key : keys) {
			if (fworkProperties.get(key).visible()){
				Console.display(String.format("| %-60s| %s", fworkProperties.get(key).text(), fworkProperties.get(key).value().asString()));
				Console.display(String.format("| %-60s| %s", "(" + key + ")", ""));
				Console.marker(100);
			}
		}
		Console.marker(100);
	}

	public String getBaseDir() {
		return refDir;
	}

	public void setRefDir(String refDir) {
		this.refDir = refDir;
	}

	public void processConfigProperties(HashMap<String, Value> properties) throws Exception {
		for (ComponentConfigurator configurator : configurators) {
			configurator.processConfigProperties(properties);
		}
	}

	public void processCentralUDVProperties(Map<String, Value> properties) {
		this.udvMap.add(properties);
	}

	public Configuration freezeCentralConfig() throws Exception {
		BaseConfiguration configuration = new BaseConfiguration();
		CentralConfiguration.setPropEnumToPropPathNameMap(this.propEnumToPropPathMap);
		CentralConfiguration.setStringsManager(this.stringsManager);
		for (String key : fworkProperties.keySet()) {
			configuration.add(key, fworkProperties.get(key).value());
		}
		CentralConfiguration.setCentralUDVMap(this.udvMap);
		CentralConfiguration.setCentralProperties(configuration);
		for (ComponentConfigurator configurator : configurators) {
			configurator.loadComponent();
		}
		return configuration;
	}

	public void populateMessages(ArrayList<MessagesContainer> messages) {
		this.stringsManager.populateMessages(messages);
	}

	public void populateNames(ArrayList<NamesContainer> names) {
		this.stringsManager.populateNames(names);
	}

	public <T extends Enum<T>> String getPropPathForEnum(T propEnum) {
		String key = String.format("%s.%s", propEnum.getClass().getSimpleName().toUpperCase(),
				propEnum.toString().toUpperCase());
		return propEnumToPropPathMap.get(key);
	}

	public <T extends Enum<T>> Value value(T enumObject) throws Exception {
		return fworkProperties.get(getPropPathForEnum(enumObject)).value();
	}

	public <T extends Enum<T>> ValueType valueType(T enumObject) throws Exception {
		return fworkProperties.get(getPropPathForEnum(enumObject)).valueType();
	}

	public <T extends Enum<T>> ValueType expectedValueType(T enumObject) throws Exception {
		return propNameExpectedTypeMap.get(getPropPathForEnum(enumObject));
	}

	public ValueType expectedValueType(String propPath) throws Exception {
		return propNameExpectedTypeMap.get(propPath);
	}

}
