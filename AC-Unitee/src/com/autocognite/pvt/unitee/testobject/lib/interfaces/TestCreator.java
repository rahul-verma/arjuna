package com.autocognite.pvt.unitee.testobject.lib.interfaces;

import java.util.List;

import com.autocognite.pvt.unitee.reporter.lib.IssueId;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestClassFragment;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestClassInstance;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestMethodInstance;

public interface TestCreator extends TestObject{

	List<JavaTestMethodInstance> getInstances();

	int getInstanceThreadCount();

	boolean shouldExecute(IssueId outId);

	String getName();

	JavaTestClassFragment getTestContainerFragment();
}
