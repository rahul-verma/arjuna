package pvt.batteries.lib;

import com.arjunapro.testauto.console.Console;

import pvt.batteries.config.Configuration;
import pvt.batteries.value.DefaultStringKeyValueContainer;

public class BaseConfiguration extends DefaultStringKeyValueContainer implements Configuration {

	public BaseConfiguration clone() {
		BaseConfiguration map = new BaseConfiguration();
		try {
			map.cloneAdd(this.items());
		} catch (Exception e) {
			Console.displayExceptionBlock(e);
		}
		return map;
	}
}
