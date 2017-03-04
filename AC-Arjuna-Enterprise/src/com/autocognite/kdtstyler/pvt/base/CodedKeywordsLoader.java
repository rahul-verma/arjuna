package com.autocognite.kdtstyler.pvt.base;

import java.io.IOException;
import java.util.HashMap;

public class CodedKeywordsLoader extends HeaderTextFileReader {
	
	public CodedKeywordsLoader(String filePath) throws IOException {
		super(filePath);
	}
	
	public void appendKeywords(HashMap<String, IKeyword> keywordMap, KeywordTrie trie) throws IOException {
		super.parse();
	
		IKeyword keyword = null;
		for (String key: processedMap.keySet()) {
			String[] packageParts = key.split("\\|");
			String language = "JAVA";
			String pkg = key;
			if (packageParts.length > 1) {
				language = packageParts[0].toUpperCase();
				pkg = packageParts[1];
			}
			//System.out.println(DSUtils.flatten(packageParts));
			for (String line: processedMap.get(key)) {
				keyword = new CodedKeyword();
				//System.out.println(line);
				line = line.replace("\t", " ");
				String[] parts = line.split(" = ");
				//System.out.println("sadasdads" + line);
				if (parts.length == 1) {
					String same = parts[0].trim(); 
					//System.out.println(same + " = " + same);
					keyword.set("KEYWORD", same);
					keyword.set("METHOD", same);
					keyword.set("PACKAGE", pkg);				
					keyword.set("LANGUAGE", language);
					keywordMap.put(same, keyword);
					trie.insert(same);
				} else {
					String left = parts[0].trim();
					String right = parts[1].trim();
					//System.out.println(left + " = " + right);
					keyword.set("KEYWORD", left);
					keyword.set("METHOD", right);
					keyword.set("PACKAGE", pkg);				
					keyword.set("LANGUAGE", language);
					keywordMap.put(left, keyword);
					trie.insert(left);
				}
			}
		}
	}
}
