package com.autocognite.pvt.unitee.testobject.lib.interfaces;

import java.util.List;

import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestMethod;
import com.autocognite.pvt.unitee.testobject.lib.loader.DataMethodsHandler;

public interface TestContainerInstance extends TestObject {

	int getInstanceNumber();
	
	void loadTestCreators() throws Exception;

	TestContainer getContainer();

	List<JavaTestMethod> getTestCreators();

	boolean wasSetUpClassInstanceFixtureExecuted();

	boolean didSetUpClassFixtureSucceed();

	boolean hasCompleted();

	int getCreatorThreadCount();

	Class<?> getUserTestContainer();

	DataMethodsHandler getDataMethodsHandler();

	Object getUserTestContainerObject();

	TestFixtures getTestFixtures();

	boolean wasTearDownClassFixtureExecuted();

	boolean didTearDownClassFixtureSucceed();

	FixtureResultType getSetUpClassFixtureResult();

	FixtureResultType getTearDownClassFixtureResult();

	void markTestCreatorCompleted(TestCreator jMethod);

	void addExecutableCreatorName(String name);

	void resetExecutorCreatorQueue();

	void setUpClassInstance() throws Exception;
	void tearDownClassInstance() throws Exception;
	
	void setUpClassFragment() throws Exception;
	void tearDownClassFragment() throws Exception;

	FixtureResultType getSetUpClassFragmentFixtureResult();
	FixtureResultType getTearDownClassFragmentFixtureResult();

	boolean shouldExecuteTearDownClassFragmentFixture();

	boolean shouldExecuteSetupClassFragmentFixture();
	
	boolean shouldExecuteSetupClassInstanceFixture();

	boolean shouldExecuteTearDownClassInstanceFixture();

}
