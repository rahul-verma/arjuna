package pvt.batteries.lib;

import pvt.batteries.config.Configuration;
import pvt.batteries.value.DefaultStringKeyValueContainer;

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
