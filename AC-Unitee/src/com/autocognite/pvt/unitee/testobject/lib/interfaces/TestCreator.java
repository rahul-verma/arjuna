package com.autocognite.pvt.unitee.testobject.lib.interfaces;

import java.util.List;

import com.autocognite.pvt.unitee.reporter.lib.IssueId;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestClassInstance;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestMethodInstance;

public interface TestCreator extends TestObject{

	List<JavaTestMethodInstance> getInstances();

	int getInstanceThreadCount();

	boolean shouldExecute(IssueId outId);

	boolean hasCompleted();

	String getName();

	JavaTestClassInstance getTestContainerInstance();

	void markTestMethodInstanceCompleted(TestCreatorInstance instance);

	void setUpMethod() throws Exception;

	void tearDownMethod() throws Exception;

	boolean shouldExecuteSetupMethodFixture();

	boolean wasSetUpMethodFixtureExecuted();

	boolean shouldExecuteTearDownMethodFixture();

}
