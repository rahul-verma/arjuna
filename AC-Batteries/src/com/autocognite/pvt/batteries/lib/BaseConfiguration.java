package com.autocognite.pvt.batteries.lib;

import com.autocognite.batteries.value.StringKeyValueContainer;
import com.autocognite.pvt.batteries.config.Configuration;

public class BaseConfiguration extends StringKeyValueContainer implements Configuration {

	public BaseConfiguration clone() {
		BaseConfiguration map = new BaseConfiguration();
		try {
			map.cloneAdd(this.items());
		} catch (Exception e) {
			e.printStackTrace();
		}
		return map;
	}
}
