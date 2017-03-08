package com.autocognite.pvt.batteries.lib;

import com.autocognite.pvt.batteries.config.Configuration;
import com.autocognite.pvt.batteries.value.DefaultStringKeyValueContainer;

public class BaseConfiguration extends DefaultStringKeyValueContainer implements Configuration {

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
