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
package com.autocognite.batteries.processhandler;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.autocognite.batteries.util.SystemBatteries;
import com.autocognite.pvt.batteries.lib.DelimitedDataParser;
import com.autocognite.pvt.batteries.lib.ThreadSafeStreamReader;

public class CommandExecutor {
	private String command = null;
	private List<String> args = null;
	private String stdout = null;
	private String stderr = null;
	private int returnCode = -1000;

	public CommandExecutor(String command, String[] args) {
		this.command = command;
		this.args = Arrays.asList(args);
	}

	public CommandExecutor(String command, List<String> args) {
		this.command = command;
		this.args = args;
	}

	public CommandExecutor(String command, String argString) {
		this.command = command;
		this.args = DelimitedDataParser.parse(argString);
	}

	public CommandExecutor(String commandString) {
		List<String> arr = DelimitedDataParser.parse(commandString);
		this.command = arr.get(0);
		this.args = arr.subList(1, arr.size());
	}

	private void addPrefix(List<String> commandList) {
		String[] windows = { "cmd.exe", "/C" };
		String[] empty = {};

		if (SystemBatteries.getOSName().contains("Windows")) {
			commandList.addAll(Arrays.asList(windows));
		}
	}

	private String[] getCommandArray() {
		List<String> commandList = new ArrayList<String>();
		addPrefix(commandList);
		commandList.add(this.command);
		commandList.addAll(this.args);
		return commandList.toArray(new String[commandList.size()]);
	}

	public String getStdoutText() {
		return this.stdout;
	}

	public String getStderrText() {
		return this.stderr;
	}

	public int getReturnCode() {
		return this.returnCode;
	}

	public void execute() throws IOException {
		try {
			Process proc = SystemBatteries.getRunTime().exec(getCommandArray());
			// any error message?
			ThreadSafeStreamReader errorGobbler = new ThreadSafeStreamReader(proc.getErrorStream(), "ERROR");

			// any output?
			ThreadSafeStreamReader outputGobbler = new ThreadSafeStreamReader(proc.getInputStream(), "OUTPUT");

			// kick them off
			errorGobbler.start();
			outputGobbler.start();

			// any error???
			proc.getOutputStream().close();
			int exitVal = proc.waitFor();
			this.stderr = errorGobbler.getOutput();
			this.stdout = outputGobbler.getOutput();
			this.returnCode = exitVal;
		} catch (Throwable t) {
			t.printStackTrace();
		}
	}
}
