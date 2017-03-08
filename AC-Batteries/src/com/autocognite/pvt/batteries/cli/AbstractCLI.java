/*******************************************************************************
 * Copyright 2015-16 AutoCognite Testing Research Pvt Ltd
 * 
 * Website: www.AutoCognite.com
 * Email: support [at] autocognite.com
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/
package com.autocognite.pvt.batteries.cli;

import java.util.Properties;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;

import com.autocognite.arjuna.console.Console;
import com.autocognite.arjuna.utils.SystemBatteries;

public abstract class AbstractCLI implements CLI {

	private CommandLine userOptions = null;
	private Options options = new Options();
	private HelpFormatter helper = new HelpFormatter();
	private String[] args = null;

	public AbstractCLI() throws Exception {
	}
	
	@Override
	public void setArgs(String[] cliArgs) throws Exception {
		this.args = cliArgs;
		this.initialize();
		CommandLineParser parser = new DefaultParser();
		try {
			this.userOptions = parser.parse(this.options, this.getArgs());
		} catch (Exception e) {
			Console.displayError("Error: Improper CLI usage.");
			Console.displayError(
					"Solution: Go through the exception details & the CLI usage details shown below. Change your CLI options accordingly.");
			Console.displayExceptionBlock(e);
			help();
			SystemBatteries.exit();
		}
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.configurator.lib.cli.CLI#getUniteeProperties()
	 */
	@Override
	public Properties getProperties() {
		// return
		// this.userOptions.getOptionProperties(options.getOption("P").getOpt());
		return null;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.configurator.lib.cli.CLI#getOption(java.lang.String)
	 */
	@Override
	public String getOption(String option) {
		String value = this.userOptions.getOptionValue(option.toLowerCase());
		return value;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.autocognite.configurator.lib.cli.CLI#hasOption(java.lang.String)
	 */
	@Override
	public boolean hasOption(String option) {
		boolean value = this.userOptions.hasOption(option.toLowerCase());
		return value;
	}

	@Override
	public String[] getArgs() {
		return args;
	}

	private void addOption(Option opt) {
		this.options.addOption(opt);
	}

	@Override
	public void addSingleArgSwitch(String shortName, String longName, String argName, String desc) throws Exception {
		addOption(Option.builder(shortName).longOpt(longName).desc(desc).hasArg().argName(argName.toUpperCase())
				.valueSeparator('=').build());
	}

	@Override
	public void addTrueSwitch(String shortName, String longName, String desc) throws Exception {
		addOption(new Option(shortName, longName, true, desc));
	}

	@Override
	public void addFalseSwitch(String shortName, String longName, String desc) throws Exception {
		addOption(new Option(shortName, longName, false, desc));
	}

	public void help(String prefix) throws Exception {
		this.helper.printHelp(prefix, this.options);
	}

	@Override
	public void initialize() throws Exception {
		// addOption(Option.builder("P").argName("property=value").hasArgs().numberOfArgs(2).valueSeparator('=').desc("Change
		// Unitee Property Values" ).build());
	}
}
