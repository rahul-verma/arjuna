package com.autocognite.pvt.batteries.property;

import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.pvt.batteries.enums.ConfigPropertyLevel;
import com.autocognite.pvt.batteries.value.ValueType;

public class ConfigPropertyBuilder<T extends Enum<T>> {
	private String definer = "UserDefined";
	private String propCodeName = null;
	private String propPath = null;
	private ConfigPropertyLevel propLevel = ConfigPropertyLevel.CENTRAL;
	private String readableName = null;
	private boolean propUserOverride = true;
	private boolean propVisible = true;
	private Value propValue = null;
	private ValueType expectedValueType = ValueType.STRING;

	private void reset() {
		definer = "UserDefined";
		propCodeName = null;
		propPath = null;
		propLevel = ConfigPropertyLevel.CENTRAL;
		readableName = null;
		propUserOverride = true;
		propVisible = true;
		propValue = null;
		expectedValueType = ValueType.STRING;
	}

	public ConfigPropertyBuilder<T> codeName(T enumCode) {
		definer = enumCode.getClass().getSimpleName();
		propCodeName = enumCode.toString();
		return this;
	}

	public ConfigPropertyBuilder<T> path(String path) {
		propPath = path;
		if (readableName == null) {
			this.readableName = path.toUpperCase();
		}
		return this;
	}

	public ConfigPropertyBuilder<T> level(ConfigPropertyLevel level) {
		propLevel = level;
		return this;
	}

	public ConfigPropertyBuilder<T> text(String text) {
		this.readableName = text;
		return this;
	}

	public ConfigPropertyBuilder<T> overridable(boolean flag) {
		this.propUserOverride = flag;
		return this;
	}

	public ConfigPropertyBuilder<T> visible(boolean flag) {
		this.propVisible = flag;
		return this;
	}

	public ConfigPropertyBuilder<T> value(Value val) {
		this.propValue = val;
		return this;
	}

	public ConfigPropertyBuilder<T> expectedValueType(ValueType vType) {
		this.expectedValueType = vType;
		return this;
	}

	public ConfigProperty build() {
		ConfigProperty prop = new ConfigProperty(this.definer, this.propCodeName, this.propPath, this.expectedValueType,
				this.propValue, this.propLevel, this.readableName, this.propUserOverride, this.propVisible);
		this.reset();
		return prop;
	}
}
