package pvt.batteries.hocon;

import com.typesafe.config.Config;
import com.typesafe.config.ConfigObject;

public class HoconConfigObjectReader extends AbstractHoconReader {
	private Config config = null;

	public HoconConfigObjectReader(ConfigObject confObj) {
		super();
		this.config = confObj.toConfig();
	}

	@Override
	public void loadConfig() throws Exception {
		this.setConfig(config);
	}
}
