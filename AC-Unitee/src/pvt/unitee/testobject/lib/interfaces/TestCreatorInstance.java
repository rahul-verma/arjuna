package pvt.unitee.testobject.lib.interfaces;

import pvt.arjunapro.enums.FixtureResultType;

public interface TestCreatorInstance extends TestObject {

	Test next() throws Exception;

	int getTestThreadCount();

	TestCreator getParentTestCreator();

	TestContainerFragment getTestContainerFragment();

	int getInstanceNumber();

}
