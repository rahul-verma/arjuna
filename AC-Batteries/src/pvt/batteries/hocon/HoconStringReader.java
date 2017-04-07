package pvt.batteries.hocon;

import java.io.Reader;
import java.io.StringReader;

import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;

import pvt.arjunapro.enums.HoconSyntaxType;

public class HoconStringReader extends AbstractHoconReader {
	private String confString = null;

	public HoconStringReader(String confString) throws Exception {
		super();
		this.confString = confString;
	}

	public HoconStringReader(String confString, HoconSyntaxType parseSyntax) {
		super(parseSyntax);
		this.confString = confString;
	}

	@Override
	public void loadConfig() throws Exception {
		Reader reader = new StringReader(confString.replace("\\\\\\\\", "fourslash").replace("\\\\", "twoslash")
				.replace("\\", "\\\\")
				.replace("twoslash", "\\\\")
				.replace("fourslash", "\\\\\\\\"));
		Config loadedConf = ConfigFactory.load(ConfigFactory.parseReader(reader, this.getParseOptions()),
				this.getResolveOptions());
		this.setConfig(loadedConf);
	}
}
