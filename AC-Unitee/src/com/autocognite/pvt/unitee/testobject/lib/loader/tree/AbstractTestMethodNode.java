package com.autocognite.pvt.unitee.testobject.lib.loader.tree;

import java.util.ArrayList;
import java.util.List;

import com.autocognite.pvt.batteries.console.Console;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;

public class AbstractTestMethodNode implements TestNode{
	private JavaTestMethodDefinition methodDef = null;
	private String name = null;
	private List<TestNode> edges = new ArrayList<TestNode>();
	private boolean scheduled;

	public AbstractTestMethodNode(String name, JavaTestMethodDefinition methodDef){
		this.setName(name);
		this.setCreatorDefinition(methodDef);
	}

	public AbstractTestMethodNode(String name){
		this.setName(name);
	}

	public boolean isDummy(){
		return false;
	}

	public void addEdge(TestNode node){
		this.edges.add(node);
	}

	public List<TestNode> getEdges() {
		return edges;
	}

	public JavaTestMethodDefinition getCreatorDefinition() {
		return methodDef;
	}

	private void setCreatorDefinition(JavaTestMethodDefinition methodDef) {
		this.methodDef = methodDef;
	}

	public String getName() {
		return name;
	}

	private void setName(String name) {
		this.name = name;
	}
	
	public void enumerateEdges(){
		for (TestNode edge: this.edges){
			if (edge == null){
				Console.display("NULL");
			} else {
				Console.display(edge.getName());
			}
		}
	}
}
