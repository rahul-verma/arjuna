package com.autocognite.kdtstyler.pvt.base;

import java.util.HashMap;

public class TrieNode {
	private HashMap<Character, TrieNode> children = null;
	private boolean hasCompleted;
	private char value;
	
    public TrieNode(char ch)  {
        value = ch;
        this.children = new HashMap<Character, TrieNode>();
        hasCompleted = false;
    }
    
    public HashMap<Character, TrieNode> getChildren() {
    	return children; 
    }
    
    public char getValue() {
    	return value;
    }
    
    public void end(boolean val) {
    	hasCompleted = val;
    }
    
    public boolean hasEnded() {
    	return hasCompleted;
    } 
}
