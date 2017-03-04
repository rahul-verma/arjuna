package com.autocognite.kdtstyler.pvt.base;

import java.io.IOException;

public class TextKDTReader extends HeaderTextFileReader {

	public TextKDTReader(String filePath) throws IOException {
		super(filePath);
	}
	
	public void processLine(String line) {
		
	}
	
	public void parse(Keywords keywords) throws IOException {
		super.parse();
		
		for (String key: processedMap.keySet()) {
			//System.out.println(key);
			String statement = null;
			for (String line: processedMap.get(key)) {
				System.out.println(line);
				//System.out.println(DSUtils.flatten(line.split("\\s+")));
				line = line.replace("\t", " ");
				line = line.replace("\\s+", " ");
				if (!line.startsWith("Is")) {
					
					
					// Find out whether it is an equation
					String[] lineParts = line.split(" ");
					if (lineParts.length > 1) {
						if (lineParts[1].equals(" = ")) {
							// Yes it is an equation
							System.out.println("Is an equation");
							statement = line.split(" = ")[1].trim();
						} else {
							statement = line;
						}
					} else {
						statement = line;
					}
				} else {
					statement = line;
				}
				if (statement == null) {
					System.out.println("Statement is null" + line);
				}
				
				String match = keywords.match(statement);
				System.out.println("MATCH:" + match);
				if (match.equals("")) {
					System.out.println("***PARSING ISSUE***: " + statement);
				}
			}
		}
	}
}
