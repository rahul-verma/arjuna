package com.autocognite.kdtstyler.pvt.base;

import java.io.IOException;
import java.util.ArrayList;

public class Keywords extends UniteeCoreKeywords {
	
	public void init() throws IOException {
		super.init();
		ArrayList<String> files = new ArrayList<String>();
		String basePath = "/Users/rahul/Documents/_unitee/keyword_workbench/keywords/coded/";
		files.add(basePath + "keywords.txt");
		CodedKeywordsLoader loader = null;

		for (String file: files) {
			
			loader = new CodedKeywordsLoader(file);
			loader.appendKeywords(keywords, trie);
		}
		
		IKeyword keyword = null;
		for (String keywordName: keywords.keySet()) {
			keyword = keywords.get(keywordName);
			System.out.println("----------------------------------------------------------------------------");
			System.out.println("Keyword: " + keywordName);
			System.out.println("Package: " + keyword.get("PACKAGE"));
			System.out.println("Method: " + keyword.get("METHOD"));
			System.out.println("Language: " + keyword.get("LANGUAGE"));
			System.out.println("----------------------------------------------------------------------------");
		}
	}
	
	public String match(String statement) {
		return trie.getKeyword(statement);
	}
}
