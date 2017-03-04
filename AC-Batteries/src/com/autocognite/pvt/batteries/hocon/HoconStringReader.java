package com.autocognite.pvt.batteries.hocon;

import java.io.Reader;
import java.io.StringReader;

import com.autocognite.pvt.batteries.enums.HoconSyntaxType;
import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;

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
		Reader reader = new StringReader(confString);
		Config loadedConf = ConfigFactory.load(ConfigFactory.parseReader(reader, this.getParseOptions()),
				this.getResolveOptions());
		this.setConfig(loadedConf);
	}
}
