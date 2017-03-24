package com.arjunapro.testauto.console;

import org.apache.log4j.Level;

import com.arjunapro.sysauto.batteries.SystemBatteries;
import com.arjunapro.testauto.config.RunConfig;

import pvt.batteries.config.Batteries;
import pvt.batteries.utils.ExceptionBatteries;

public class Console {
	private static boolean done = false;
	private static String separator = null;
	private static Level centralLogLevel = null;

	public synchronized static void init() {
		if (done)
			return;
		separator = SystemBatteries.getLineSeparator();
		done = true;
	}

	private synchronized static boolean logToCentralLog(String message) {
		if (centralLogLevel == null) {
			return true;
		} else if (centralLogLevel == Level.DEBUG) {
			RunConfig.logger().debug(message);
			return false;
		} else {
			RunConfig.logger().debug(message);
			return true;
		}
	}

	public synchronized static void display(String message) {
		boolean shouldPrint = logToCentralLog(message);
		if (shouldPrint) {
			System.out.println(message);
		}
	}

	public synchronized static void displayError(String message) {
		boolean shouldPrint = logToCentralLog(message);
		if (shouldPrint) {
			System.err.println(message);
		}
	}

	private synchronized static void errorForConsole(String message) {
		System.err.println(message);
	}

	public synchronized static void displayOnSameLine(String message) {
		boolean shouldPrint = logToCentralLog(message);
		if (shouldPrint) {
			System.out.print(message);
		}
	}

	public synchronized static void marker(int length) {
		String marker = new String(new char[length]).replace('\0', '-');
		display(marker);
	}

	public synchronized static void markerError(int length) {
		String marker = new String(new char[length]).replace('\0', '-');
		displayError(marker);
	}

	public synchronized static void markerOnSameLine(int length) {
		String marker = new String(new char[length]).replace('\0', '-');
		displayOnSameLine(marker);
	}

	public synchronized static void marker(int length, char symbol) {
		String marker = new String(new char[length]).replace('\0', symbol);
		display(marker);
	}

	public synchronized static void markerError(int length, char symbol) {
		String marker = new String(new char[length]).replace('\0', symbol);
		displayError(marker);
	}

	public synchronized static void displayKeyValue(String key, String value) {
		String message = String.format("%s %s", key, value);
		display(message);
	}

	public synchronized static void displayPaddedKeyValue(String key, String value) {
		String message = String.format("| %-20s| %s", key, value);
		display(message);
	}

	public synchronized static void displayPaddedKeyValue(String key, String value, int leftPadding) {
		String rightPad = String.format("%%%ds", leftPadding + 2);
		String cleanedValue = value.replace(separator, separator + "|" + String.format(rightPad, "|")); // .replace("\t",
																										// String.format(rightPad,
																										// ""));
		String fmt = String.format("| %%-%ds| %%s", leftPadding);
		String message = String.format(fmt, key, cleanedValue);
		display(message);
	}

	public synchronized static void displayPaddedKeyValueError(String key, String value, int leftPadding) {
		String rightPad = String.format("%%%ds", leftPadding + 2);
		String cleanedValue = value.replace(separator, separator + "|" + String.format(rightPad, "|")); // .replace("\t",
																										// String.format(rightPad,
																										// ""));
		String fmt = String.format("| %%-%ds| %%s", leftPadding);
		String message = String.format(fmt, key, cleanedValue);
		displayError(message);
	}

	public synchronized static void displayExceptionBlock(Throwable e) {
		Console.markerError(80);
		Console.displayPaddedKeyValueError("Exception Type", e.getClass().getSimpleName(), 30);
		if (e.getMessage() != null){
			Console.displayPaddedKeyValueError("Exception Message", e.getMessage(), 30);
		}
		Console.displayPaddedKeyValueExceptionTrace("Exception Trace", ExceptionBatteries.getStackTraceAsString(e), 30);
		Console.markerError(80);
	}

	public static void setCentralLogLevel(Level level) {
		centralLogLevel = level;
	}

	public synchronized static void displayPaddedKeyValueExceptionTrace(String key, String value, int leftPadding) {
		String rightPad = String.format("%%%ds", leftPadding + 2);
		String cleanedValue = value.replace(separator, "|").replace("\t", " "); // .replace("\t",
																				// String.format(rightPad,
																				// ""));
		String fmt = String.format("| %%-%ds| %%s", leftPadding);
		String message = String.format(fmt, key, cleanedValue);
		boolean shouldPrint = logToCentralLog(message);
		if (shouldPrint) {
			cleanedValue = value.replace(separator, separator + "|" + String.format(rightPad, "|")); // .replace("\t",
																										// String.format(rightPad,
																										// ""));
			message = String.format(fmt, key, cleanedValue);
			errorForConsole(message);
		}
	}

}
