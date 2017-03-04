package com.autocognite.pvt.unitee.testobject.lib.loader.tree;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class DependencyTree {
	List<String> allNodesQueue = new ArrayList<String>();
	Set<String> methodDependencies = new HashSet<String>();
	Map<String, TestMethodNode> allNodesMap = null;
	
	public DependencyTree(List<String> methodNames, Map<String, TestMethodNode> nodesMap){
		allNodesQueue.addAll(methodNames);
		methodDependencies.addAll(methodNames);
		this.allNodesMap = nodesMap;
	}
	
	public boolean doesMethodDepExist(String name) {
		return this.methodDependencies.contains(name);
	}

	public int getNodeCount() {
		return this.allNodesQueue.size();
	}

	public boolean isEmpty() {
		return this.allNodesQueue.size() == 0;
	}
	
	public Iterator<String> iterator(){
		return this.allNodesQueue.iterator();
	}

	public void removeMethodDependency(String name) {
		this.methodDependencies.remove(name);
	}

	public void removeFromQueue(ArrayList<String> names) {
		this.allNodesQueue.removeAll(names);
	}

	public TestMethodNode getNode(String name) {
		return this.allNodesMap.get(name);
	}

}
