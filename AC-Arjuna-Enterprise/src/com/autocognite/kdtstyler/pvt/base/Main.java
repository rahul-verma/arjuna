package com.autocognite.kdtstyler.pvt.base;

import java.util.ArrayList;

public class Main {
	public static void main(String args[]) throws Exception {
		Keywords keywords = new Keywords();
		keywords.init();
		
		ArrayList<String> files = new ArrayList<String>();
		String basePath = "/Users/rahul/Documents/_unitee/keyword_workbench/simple/";
		files.add(basePath + "SimpleTestCase.kdt");
		files.add(basePath + "SimpleTestCaseWithParams.kdt");
		files.add(basePath + "TestCaseWithFixtures.kdt");
		files.add(basePath + "TestCaseWithFixturesDDT.WithCustomDS.kdt");
		files.add(basePath + "TestCaseWithFixturesDDT.kdt");
		files.add(basePath + "TestCaseWithFixturesDDTSecondaryKeywords.kdt");
		files.add(basePath + "TestCaseWithFixturesDDTTertiaryKeywords.kdt");

		for (String file: files) {
			System.out.println(file);
			System.out.println("---------------------------------------------");
			TextKDTReader reader = new TextKDTReader(file);
			reader.parse(keywords);
			System.out.println("---------------------------------------------");
		}
		

	}
}
