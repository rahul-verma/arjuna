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
package com.autocognite.batteries.util;

import com.autocognite.batteries.processhandler.CommandExecutor;
import com.sun.jna.platform.win32.Advapi32Util;
import com.sun.jna.platform.win32.WinReg.HKEY;

public class WindowsBatteries {

	public static boolean isRegistryKeyPresent(HKEY hKey, String keyPath) {
		return Advapi32Util.registryKeyExists(hKey, keyPath);
	}

	public static void killProcess(String processName) throws Exception {
		CommandExecutor executor = new CommandExecutor("taskkill /F /IM " + processName);
		executor.execute();
		if (executor.getReturnCode() != 0) {
			throw new Exception("Not able to kill process: " + processName);
		}
	}

	public static void startService(String serviceName) throws Exception {
		CommandExecutor executor = new CommandExecutor(String.format("sc start \"%s\"", serviceName));
		executor.execute();
		if ((executor.getReturnCode() != 0) || (!isServiceRunning(serviceName))) {
			throw new Exception("Unable to start service: " + serviceName);
		}
	}

	public static void stopService(String serviceName) throws Exception {
		CommandExecutor executor = new CommandExecutor(String.format("sc stop \"%s\"", serviceName));
		executor.execute();
		if ((executor.getReturnCode() != 0) || (isServiceRunning(serviceName))) {
			throw new Exception("Unable to stop service: " + serviceName);
		}
	}

	public static boolean isServiceRunning(String serviceName) throws Exception {
		CommandExecutor executor = new CommandExecutor(String.format("sc query \"%s\"", serviceName));
		executor.execute();
		if (executor.getReturnCode() != 0) {
			throw new Exception("Unable to check status of service: " + serviceName);
		} else {
			if (executor.getStdoutText().contains("RUNNING")) {
				return true;
			}
		}
		return false;
	}
}
