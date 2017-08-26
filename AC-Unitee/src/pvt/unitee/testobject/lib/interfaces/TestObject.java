package pvt.unitee.testobject.lib.interfaces;

import pvt.unitee.enums.FixtureResultType;
import pvt.unitee.enums.TestResultCode;
import pvt.unitee.testobject.lib.fixture.Fixture;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import unitee.enums.TestObjectType;
import unitee.interfaces.TestVariables;

public interface TestObject {
	
	TestVariables getTestVariablesDefinition() throws Exception;

	String getObjectId();

	String getQualifiedName();

	TestVariables getTestVariables();

	TestObjectType getObjectType();
	
	void markExcluded(TestResultCode exType, String desc, int issueId);
	
	boolean wasExcluded();
	
	TestResultCode getExclusionType();
	
	String getExclusionDesc();
	
	int getExclusionIssueId();

//	void markUnSelected(TestResultCode type, String desc);
//
//	boolean wasUnSelected();
//
//	TestResultCode getUnSelectedType();
//
//	String getUnSelectedDesc();
//	
//	void markSkipped(TestResultCode type, String desc);
//
//	boolean wasSkipped();
//
//	TestResultCode getSkipType();
//
//	String getSkipDesc();

	void setThreadId(String id) throws Exception;
	
	void initTimeStamp() throws Exception;
	
	void endTimeStamp() throws Exception;
	
	Fixture getSetUpFixture() throws Exception;
	
	Fixture getTearDownFixture() throws Exception;
	
	void setUp() throws Exception;
	
	void tearDown() throws Exception;
	
	boolean wasSetUpExecuted() throws Exception;
	
	boolean wasTearDownExecuted() throws Exception;
	
	boolean wasSetUpSuccessful() throws Exception;
	
	boolean wasTearDownSuccessful() throws Exception;
	
	boolean shouldExecuteSetUp() throws Exception;
	
	boolean shouldExecuteTearDown() throws Exception;
	
	FixtureResultType getSetUpResult() throws Exception;
	
	FixtureResultType getTearDownResult() throws Exception;
	
	TestFixtures getTestFixtures();

	boolean hasCompleted();
	
	void populateUserProps() throws Exception;
}
