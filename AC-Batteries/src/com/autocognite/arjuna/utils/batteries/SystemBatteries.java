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
package com.autocognite.arjuna.utils.batteries;

import java.io.File;

import com.autocognite.arjuna.utils.console.Console;

public class SystemBatteries {

	public static void exit() {
		Console.displayError("Exiting...");
		System.exit(1);
	}

	public static Runtime getRunTime() {
		return Runtime.getRuntime();
	}

	public static String getOSName() {
		return System.getProperty("os.name");
	}

	public static String getLineSeparator() {
		return System.getProperty("line.separator");
	}

	public static String getPathSeparator() {
		return File.separator;
	}
}
