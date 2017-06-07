package pvt.batteries.hocon;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;

import pvt.arjunasdk.enums.HoconSyntaxType;

public class HoconResourceReader extends AbstractHoconReader {
	private InputStream fileStream = null;

	public HoconResourceReader(InputStream fileStream) {
		super();
		this.fileStream = fileStream;
	}

	public HoconResourceReader(InputStream fileStream, HoconSyntaxType parseSyntax) {
		super(parseSyntax);
		this.fileStream = fileStream;
	}

	@Override
	public void loadConfig() throws Exception {
		BufferedReader reader = new BufferedReader(new InputStreamReader(fileStream));
		Config conf = ConfigFactory.parseReader(reader, this.getParseOptions());
		Config loadedConf = ConfigFactory.load(conf, this.getResolveOptions());
		this.setConfig(loadedConf);
	}
}
