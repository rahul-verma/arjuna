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
package com.autocognite.pvt.unitee.cli;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import com.autocognite.pvt.batteries.cli.AbstractCLI;
import com.autocognite.pvt.batteries.console.Console;
import com.autocognite.pvt.unitee.testobject.lib.loader.group.AbstractPickerConfig;

public class UniteeCLI extends AbstractCLI {
	
	public UniteeCLI() throws Exception {
	}

	@Override
	public void initialize() throws Exception {
		super.initialize();
		
		addFalseSwitch("h", "help", "Print help for Unitee's command line");
		addFalseSwitch("v", "version", "Print Unitee version and exit");

		addSingleArgSwitch("dl",
		"display-level",
		"(DEBUG/INFO/WARN/ERROR/FATAL)",
		"Min log message level for console display.");	

		addSingleArgSwitch("ll",
		"log-level",
		"(DEBUG/INFO/WARN/ERROR/FATAL)",
		"Min log message level for file logging.");
		
		addSingleArgSwitch("pn",
		"package-name",
		"name",
		"Package Name");

		addSingleArgSwitch("cn",
		"class-name",
		"name",
		"Class Name");
		
		addSingleArgSwitch("cp",
		"consider-packages",
		"comma separated patterns",
		"Consider only these test packages for execution");

		addSingleArgSwitch("cc",
		"consider-classes",
		"comma separated patterns",
		"Consider only these test classes for execution");

		addSingleArgSwitch("cm",
		"consider-methods",
		"comma separated patterns",
		"Consider only these test methods for execution");

		addSingleArgSwitch("ip",
		"ignore-packages",
		"comma separated patterns",
		"Ignore these test packages for execution");

		addSingleArgSwitch("ic",
		"ignore-classes",
		"comma separated patterns",
		"Ignore these test classes for execution");

		addSingleArgSwitch("im",
		"ignore-methods",
		"comma separated patterns",
		"Ignore these test methods for execution");

		addSingleArgSwitch("d",
		"test-dir",
		"local directory",
		"Full directory path of tests. Contains classes/JAR files.");

		addSingleArgSwitch("rgb",
		"report-generators-builtin",
		"ReportFormat Enum String(s)",
		"Comma Separated list of built-in reports to be generated. Options: CONSOLE, EXCEL");
		
		addSingleArgSwitch("rlb",
		"report-listeners-builtin",
		"ReportFormat Enum String(s)",
		"Comma Separated list of built-in report listeners. Options: CONSOLE, EXCEL");
		
		addSingleArgSwitch("rm",
		"report-mode",
		"Report Mode",
		"Provide one of these: MINIMAL, BASIC, ADVANCED, DEBUG");

		addSingleArgSwitch("rid",
		"run-id",
		"Name of current run",
		"A name to identify a run in Unitee.");	
//		
//		addSingleArgSwitch("s",
//		"session-name",
//		"Name of Session Template",
//		"Unitee Session template to be used for this run.");	
	}

	@Override
	public void help() throws Exception {
		BufferedReader txtReader = new BufferedReader(new InputStreamReader(UniteeCLI.class.getResourceAsStream("/com/autocognite/pvt/text/arjuna_cli.help")));
		String line = null;
		while ((line = txtReader.readLine()) != null) {
			Console.displayError(line);
		}
		txtReader.close();
//		super.help("unitee.sh OR unitee.bat\r\n\r\n");
	}
}
