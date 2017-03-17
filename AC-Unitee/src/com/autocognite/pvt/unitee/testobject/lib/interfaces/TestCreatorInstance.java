package com.autocognite.pvt.unitee.testobject.lib.interfaces;

import com.autocognite.pvt.arjuna.enums.FixtureResultType;

public interface TestCreatorInstance extends TestObject {

	Test next() throws Exception;

	int getTestThreadCount();

	TestCreator getParentTestCreator();

	TestContainerFragment getTestContainerFragment();

	int getInstanceNumber();

}
