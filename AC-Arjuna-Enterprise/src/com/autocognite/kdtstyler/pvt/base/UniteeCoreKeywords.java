package com.autocognite.kdtstyler.pvt.base;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class UniteeCoreKeywords {
	HashMap<String, IKeyword> keywords = new HashMap<String, IKeyword>();
	KeywordTrie trie = new KeywordTrie();
	
	public void init() throws IOException {
		ArrayList<String> internalKeywords = new ArrayList<String>();
		internalKeywords.add("Is");
		internalKeywords.add("Set");
		CodedKeyword keyword = null;
		for (String kword: internalKeywords) {
			keyword = new CodedKeyword();
			keyword.set("KEYWORD", kword);
			keyword.set("METHOD", kword);
			keyword.set("PACKAGE", "in.unitee.internal.kdt.Keywords");				
			keyword.set("LANGUAGE", "JAVA");
			keywords.put(kword, keyword);
			trie.insert(kword);
		}
	}
}
