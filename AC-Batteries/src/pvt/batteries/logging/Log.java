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
package pvt.batteries.logging;

import org.apache.log4j.ConsoleAppender;
import org.apache.log4j.FileAppender;
import org.apache.log4j.Level;
import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;
import org.apache.log4j.PatternLayout;

import arjunasdk.console.Console;

public class Log {
	private ConsoleAppender console = new ConsoleAppender(); // create appender
	private FileAppender fa = new FileAppender();

	private void setConsoleLogger(Level level, String logName) {
		// configure the appender
		// String PATTERN = "[%-5p]\t%l\t%m%n";
		String PATTERN = null;
		PATTERN = "(%F:%L)\t%m%n";
		// if (Unitee.isInternalBuild()){
		// PATTERN = "(%F:%L)\t%m%n";
		// //"[%-5p]\t%m%n";//"[%-5p]\t%d{yyyy-MM-dd|HH:mm:ss}\t(%F:%L)\t%m%n";//
		// } else {
		// PATTERN = "%m%n";
		// }
		console.setLayout(new PatternLayout(PATTERN));
		console.setThreshold(level);
		console.activateOptions();
		Logger.getLogger(logName).addAppender(console);
		Console.setCentralLogLevel(level);
	}

	private void setFileLogger(Level level, String logName, String path) {
		fa.setName("FileLogger-" + logName);
		fa.setFile(path + "/" + logName + ".log");
		// if (Unitee.isInternalBuild()){
		fa.setLayout(new PatternLayout("[%-5p]\t%d{yyyy-MM-dd|HH:mm:ss}\t(%F:%L)\t%m%n"));
		// } else {
		// fa.setLayout(new PatternLayout("[%-5p]\t%d{yyyy-MM-dd|HH:mm:ss}
		// %m%n"));
		// }
		fa.setThreshold(level);
		fa.setAppend(false);
		fa.activateOptions();
		Logger.getLogger(logName).addAppender(fa);
	}

	public void configure(Level consoleLevel, Level fileLevel, String logName, String logPath) {
		Logger.getLogger(logName);
		Logger.getLogger(logName).getLoggerRepository().resetConfiguration();
		this.setConsoleLogger(consoleLevel, logName);
		this.setFileLogger(fileLevel, logName, logPath);
	}

	public void changeLogLevel(String name, String level) {
		LogManager.getLogger(name).setLevel(Level.toLevel(level));
	}
}
