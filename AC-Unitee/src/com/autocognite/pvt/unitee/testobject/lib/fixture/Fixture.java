package com.autocognite.pvt.unitee.testobject.lib.fixture;

import java.lang.reflect.Method;

import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.arjuna.enums.TestResultCode;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerFragment;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestObject;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestClassFragment;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestClassInstance;
import com.autocognite.pvt.unitee.testobject.lib.loader.MethodSignatureType;

public interface Fixture extends Cloneable{

	String getName();

	public Fixture clone() throws CloneNotSupportedException;

	void setTestContainerInstance(TestContainerInstance testContainerInstance);

	boolean execute() throws Exception;

	TestObject getTestObject();

	void setTestObject(TestObject testObject);
	
	boolean wasExecuted();
	
	boolean wasSuccessful();

	FixtureResultType getResultType();

	String getFixtureClassName();

	int getIssueId();

	void setTestContainerFragment(TestContainerFragment javaTestClassFragment);
	
	TestResultCode getTestResultCodeForFixtureError();

	Method getMethod();

	void setSignatureType(MethodSignatureType type);

}
