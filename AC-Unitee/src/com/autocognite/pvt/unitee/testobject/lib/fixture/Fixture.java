package com.autocognite.pvt.unitee.testobject.lib.fixture;

import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestObject;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestClassInstance;

public interface Fixture extends Cloneable{

	String getName();

	public Fixture clone() throws CloneNotSupportedException;

	void setTestContainerInstance(JavaTestClassInstance classInstance);

	boolean execute() throws Exception;

	TestObject getTestObject();

	void setTestObject(TestObject testObject);
	
	boolean wasExecuted();
	
	boolean wasSuccessful();

	FixtureResultType getResultType();

	String getFixtureClassName();

	int getIssueId();

}
