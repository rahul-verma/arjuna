package com.autocognite.pvt.batteries.property;

import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.batteries.enums.ConfigPropertyLevel;
import com.autocognite.pvt.batteries.value.ValueType;

public class ConfigProperty implements Cloneable {
	private ConfigPropertyMetaData metaData = null;
	private Value propValue = null;

	public ConfigProperty(String definer, String codeName, String path, ValueType expectedValueType, Value value,
			ConfigPropertyLevel level, String text, boolean override, boolean visible) {
		this.setValue(value);
		this.setMetaData(
				new ConfigPropertyMetaData(definer, codeName, path, expectedValueType, level, text, override, visible));
	}

	private ConfigProperty(ConfigPropertyMetaData metaData, Value value) {
		this.setMetaData(metaData);
		this.setValue(value);
	}

	public ConfigProperty clone() {
		return new ConfigProperty(this.getMetaData(), this.value().clone());
	}

	public String definer() {
		return getMetaData().definer();
	}

	public String code() {
		return getMetaData().code();
	}

	public ConfigPropertyLevel level() {
		return getMetaData().level();
	}

	public String path() {
		return getMetaData().path();
	}

	public String text() {
		return getMetaData().text();
	}

	public boolean overridable() {
		return getMetaData().overridable();
	}

	public boolean visible() {
		return getMetaData().visible();
	}

	public ValueType valueType() {
		return propValue.valueType();
	}

	public Value value() {
		return propValue;
	}

	public ValueType expectedValueType() {
		return metaData.expectedValueType();
	}

	public void setValue(Value value) {
		this.propValue = value;
	}

	private ConfigPropertyMetaData getMetaData() {
		return metaData;
	}

	private void setMetaData(ConfigPropertyMetaData metaData) {
		this.metaData = metaData;
	}
}

class ConfigPropertyMetaData {
	private String definer = "UserDefined";
	private String propCodeName = null;
	private String propPath = null;
	private ConfigPropertyLevel propLevel = ConfigPropertyLevel.CENTRAL;
	private String readableName = null;
	private boolean propUserOverride = true;
	private boolean propVisible = true;
	private ValueType expectedType = ValueType.STRING;

	public ConfigPropertyMetaData(String definer, String codeName, String path, ValueType expectedValueType,
			ConfigPropertyLevel level, String text, boolean override, boolean visible) {
		this.setDefiner(definer);
		this.setCodeName(codeName);
		this.setPath(path);
		this.setExpectedValueType(expectedValueType);
		this.setLevel(level);
		this.setText(text);
		this.setOverride(override);
		this.setVisible(visible);
	}

	private void setExpectedValueType(ValueType vType) {
		this.expectedType = vType;
	}

	public String definer() {
		return definer;
	}

	private void setDefiner(String definer) {
		this.definer = definer;
	}

	public String code() {
		return propCodeName;
	}

	public ValueType expectedValueType() {
		return this.expectedType;
	}

	private void setCodeName(String codeName) {
		this.propCodeName = codeName;
	}

	public ConfigPropertyLevel level() {
		return propLevel;
	}

	private void setLevel(ConfigPropertyLevel propLevel) {
		this.propLevel = propLevel;
	}

	public String path() {
		return propPath;
	}

	private void setPath(String propPath) {
		this.propPath = propPath;
	}

	public String text() {
		return readableName;
	}

	private void setText(String readableName) {
		this.readableName = readableName;
	}

	public boolean overridable() {
		return propUserOverride;
	}

	private void setOverride(boolean propUserOverride) {
		this.propUserOverride = propUserOverride;
	}

	public boolean visible() {
		return propVisible;
	}

	private void setVisible(boolean propVisible) {
		this.propVisible = propVisible;
	}

}
