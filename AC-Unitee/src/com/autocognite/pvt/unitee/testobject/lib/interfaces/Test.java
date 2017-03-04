package com.autocognite.pvt.unitee.testobject.lib.interfaces;

import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.batteries.databroker.ReadOnlyDataRecord;
import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.unitee.testobject.lib.fixture.Fixture;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestMethodInstance;

public interface Test extends TestObject{

	String getQualifiedName();

	int getTestNumber();

	boolean didSetUpTestFixtureSucceed();

	TestVariables getTestVariables();

	TestContainerInstance getTestContainerInstance();

	String getName();

	void run() throws Exception;

	FixtureResultType getTearDownTestFixtureResult();

	boolean wasSetUpTestFixtureExecuted();

	boolean wasTearDownTestFixtureExecuted();

	boolean didTearDownTestFixtureSucceed();

	FixtureResultType getSetUpTestFixtureResult();

	TestFixtures getTestFixtures();

	void setUpTest() throws Exception;

	void tearDownTest() throws Exception;

	void execute() throws Exception;

	Fixture getSetupTestFixture();

	void setDataRecord(ReadOnlyDataRecord dataRecord);

	JavaTestMethodInstance getParentCreatorInstance();

	boolean shouldExecuteSetupTestFixture();

	boolean shouldExecuteTearDownTestFixture();
}
