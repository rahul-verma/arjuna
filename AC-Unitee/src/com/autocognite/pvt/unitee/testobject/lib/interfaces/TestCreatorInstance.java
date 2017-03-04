package com.autocognite.pvt.unitee.testobject.lib.interfaces;

import com.autocognite.pvt.arjuna.enums.FixtureResultType;

public interface TestCreatorInstance extends TestObject {

	Test next() throws Exception;

	int getTestThreadCount();

	TestCreator getParentTestCreator();

	TestContainerInstance getTestContainerInstance();

	int getInstanceNumber();

	void setUpMethodInstance() throws Exception;

	void tearDownMethodInstance() throws Exception;

	FixtureResultType getSetUpMethodFixtureResult();

	FixtureResultType getTearDownMethodFixtureResult();

	boolean wasSetUpMethodInstanceFixtureExecuted();

	boolean didSetUpMethodFixtureSucceed();

	boolean wasTearDownMethodFixtureExecuted();

	boolean didTearDownMethodFixtureSucceed();
	
	boolean shouldExecuteSetupMethodInstanceFixture();

	boolean shouldExecuteTearDownMethodInstanceFixture();

}
