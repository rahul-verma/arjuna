package pvt.batteries.hocon;

import java.io.File;

import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;

import pvt.arjunasdk.enums.HoconSyntaxType;

public class HoconFileReader extends AbstractHoconReader {
	private String confPath = null;

	public HoconFileReader(String path) {
		super();
		this.confPath = path;
	}

	public HoconFileReader(String path, HoconSyntaxType parseSyntax) {
		super(parseSyntax);
		this.confPath = path;
	}

	@Override
	public void loadConfig() throws Exception {
		Config conf = ConfigFactory.parseFile(new File(this.confPath), this.getParseOptions());
		Config loadedConf = ConfigFactory.load(conf, this.getResolveOptions());
		this.setConfig(loadedConf);
	}
}
