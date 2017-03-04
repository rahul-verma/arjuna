package com.autocognite.pvt.unitee.testobject.lib.loader.tree;

public class NonTestNode extends AbstractTestMethodNode{

	public NonTestNode(String name) {
		super(name);
	}

	public boolean isDummy(){
		return true;
	}
}
