package com.autocognite.pvt.unitee.testobject.lib.interfaces;

import java.util.List;

import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.unitee.reporter.lib.IssueId;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestClassInstance;
import com.autocognite.pvt.unitee.testobject.lib.loader.DataMethodsHandler;
import com.autocognite.pvt.unitee.testobject.lib.loader.group.Group;

public interface TestContainer extends TestObject {

	void loadInstances() throws Exception;

	int getInstanceCount();

	Class<?> getUserTestClass();

	void addExecutableCreatorName(String name);

	List<JavaTestClassInstance> getInstances();

	int getInstanceThreadCount();

	TestFixtures getTestFixtures();

	DataMethodsHandler getDataMethodsHandler();

	void resetExecutorCreatorQueue();

	void load() throws Throwable;

	boolean areInstancesCreated();

	boolean shouldExecute(IssueId outId);

	void setGroup(Group g) throws Exception;

	FixtureResultType getSetUpSessionFixtureResult();
	FixtureResultType getTearDownSessionFixtureResult();

	boolean shouldExecuteTearDownClassFixture();

	void setUpClass() throws Exception;

	void tearDownClass() throws Exception;

	boolean shouldExecuteSetupClassFixture();

	boolean wasSetUpClassFixtureExecuted();

	boolean hasCompleted();

	void markTestClassInstanceCompleted(TestContainerInstance instance);

	void setAllScheduledCreators(List<String> scheduledCreatorsForContainer);
}
