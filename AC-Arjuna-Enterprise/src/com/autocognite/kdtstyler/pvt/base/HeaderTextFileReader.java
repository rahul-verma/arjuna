package com.autocognite.kdtstyler.pvt.base;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import pvt.batteries.filehandler.FileLineReader;

public class HeaderTextFileReader {
	FileLineReader reader = null;
	ArrayList<String> allRawLines = new ArrayList<String>();
	HashMap<String, ArrayList<String>> processedMap = new HashMap<String, ArrayList<String>>();
	Pattern sectionHeader = Pattern.compile("(\\s*\\[\\s*(.*?)\\s*\\]\\s*)");

	public HeaderTextFileReader(String filePath) throws IOException {
		reader = new FileLineReader(filePath);
	}
	
	public void processHeader(String header) { }
	
	public void processLine(String line) { }
	
	protected void parse() throws IOException {
		allRawLines = reader.all();
		String currentHeader = null;
		String header = null;
		for (String line: allRawLines) {
			Matcher headerMatcher = sectionHeader.matcher(line);
			if (headerMatcher.find()) {
				header = headerMatcher.group(2);
				if (!header.equals(currentHeader)) {
					currentHeader = header;
					ArrayList<String> lines = new ArrayList<String>();
					processedMap.put(currentHeader, lines);
				}
			} else {
				line = line.trim();
				line = line.replace("\\t", " ");
				processedMap.get(currentHeader).add(line);
			}
		}

	}
}
