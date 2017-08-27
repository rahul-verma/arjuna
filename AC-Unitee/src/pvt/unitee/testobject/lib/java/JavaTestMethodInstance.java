package pvt.unitee.testobject.lib.java;

import java.lang.reflect.Method;

import org.apache.log4j.Logger;

import arjunasdk.ddauto.exceptions.DataSourceConstructionException;
import arjunasdk.ddauto.exceptions.DataSourceFinishedException;
import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.ddauto.interfaces.DataSource;
import arjunasdk.ddauto.lib.MapDataRecord;
import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.core.lib.datasource.DummyDataSource;
import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import pvt.unitee.enums.IssueSubType;
import pvt.unitee.enums.IssueType;
import pvt.unitee.enums.TestClassFixtureType;
import pvt.unitee.enums.TestResultCode;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.issue.IssueBuilder;
import pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.interfaces.Test;
import pvt.unitee.testobject.lib.interfaces.TestCreator;
import pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;
import unitee.enums.TestObjectType;
import unitee.interfaces.TestVariables;

public class JavaTestMethodInstance extends BaseTestObject implements TestCreatorInstance{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private int instanceNumber;
	private JavaTestMethod jMethod;
	private Method method;
	private JavaTestMethodDefinition methodDef = null;
	private DataSource dataSource = null;
	int currentTestNumber = 0;
	Test lastTest = null;

	public JavaTestMethodInstance(int instanceNumber, String objectId, JavaTestMethod javaTestMethod, JavaTestMethodDefinition methodDef) throws Exception{
		super(objectId, TestObjectType.TEST_METHOD_INSTANCE);
		this.instanceNumber = instanceNumber;
		this.jMethod = javaTestMethod;
		this.methodDef = methodDef;
		this.method = methodDef.getMethod();
		this.setTestVarsHandler(new DefaultTestVarsHandler(this, javaTestMethod));
		
		this.getTestVariables().rawObjectProps().setMethodInstanceNumber(this.instanceNumber);
		this.setThreadId(Thread.currentThread().getName());
		try{
			this.dataSource =  this.methodDef.getDataSource();
		} catch (DataSourceConstructionException e){
			int issueId = ArjunaInternal.getGlobalState().getIssueId();
			IssueBuilder builder = new IssueBuilder();
			Issue issue = builder
			.testVariables(this.getTestVariables())
			.exception(e)
			.trace(e.getThrowable())
			.type(IssueType.DATA_SOURCE)
			.subType(IssueSubType.DATA_SOURCE_CONSTRUCTION)
			.dataSourceName(e.getName())
			.id(issueId)
			.build();
			ArjunaInternal.getReporter().update(issue);
			this.markExcluded(
					TestResultCode.DATA_SOURCE_CONSTRUCTION_ERROR, 
					String.format("Error in %s", e.getName()),
					issueId);
			this.dataSource = new DummyDataSource();
		}
		
		initFixtures(TestClassFixtureType.SETUP_METHOD_INSTANCE, TestClassFixtureType.TEARDOWN_METHOD_INSTANCE);
		if (this.getSetUpFixture() != null){
			this.getSetUpFixture().setTestContainerInstance(this.getTestContainerFragment().getContainerInstance());	
			this.getSetUpFixture().setTestContainerFragment(this.getTestContainerFragment());
		}
		
		if (this.getTearDownFixture() != null){
			this.getTearDownFixture().setTestContainerInstance(this.getTestContainerFragment().getContainerInstance());
			this.getTearDownFixture().setTestContainerFragment(this.getTestContainerFragment());			
		}
		
		this.setIgnoreExclusionTestResultCode(TestResultCode.ERROR_IN_SETUP_METHOD_INSTANCE);
	}

	@Override
	public TestVariables getTestVariablesDefinition() {
		return this.methodDef.getTestCreatorInstanceDefinition(instanceNumber);
	}
	
	@Override
	public String getQualifiedName() {
		return this.jMethod.getQualifiedName();
	}

	@Override
	public int getTestThreadCount() {
		return this.methodDef.getTestThreadCount();
	}

	@Override
	public TestCreator getParentTestCreator() {
		return this.jMethod;
	}

	@Override
	public JavaTestClassFragment getTestContainerFragment() {
		return this.jMethod.getParent();
	}

	@Override
	public synchronized Test next() throws Exception {
//			logger.debug("Check if next Test Wrapper is available for: " + this.getTestContainer().getAuthoredTest().getUserTestClassQualifiedName() + "." + this.method.getName());
		DataRecord dataRecord = null;
		boolean dataSourceIssue = false;
		int issueId = -1;
		try{
				dataRecord = this.dataSource.next();
		} catch (DataSourceFinishedException e) {
//				logger.debug("No further sub-tests. All done.");
			//runTearDownFixtures();
			throw new SubTestsFinishedException("All Done.");
		} catch (Throwable e){
				dataSourceIssue = true;
				issueId = ArjunaInternal.getGlobalState().getIssueId();
				IssueBuilder builder = new IssueBuilder();
				Issue issue = builder
				.testVariables(this.getTestVariables())
				.exception(e)
				.message("Issue in Data Source next() call.")
				.trace(e)
				.type(IssueType.DATA_SOURCE)
				.subType(IssueSubType.DATA_SOURCE_NEXT_EXCEPTION)
				.dataSourceName(this.dataSource.getName())
				.id(issueId)
				.build();
				ArjunaInternal.getReporter().update(issue);
				this.dataSource.terminate();
		}
		
		this.currentTestNumber += 1;
		String testObjectId = String.format("%s|TestNumber-%d", this.getObjectId(), this.currentTestNumber);
		Test test = new JavaTest(currentTestNumber, testObjectId, this, methodDef);
		test.setGroup(this.getGroup());
		lastTest = test;
		if (dataSourceIssue){
			test.setDataRecord(new MapDataRecord());
			test.markExcluded(
					TestResultCode.DATA_SOURCE_NEXT_ERROR, 
					String.format("Error in getting next Data Record from %s.", this.dataSource.getName()),
					issueId);
		} else {
			test.setDataRecord(dataRecord);
		}
		return test;
	}

	public String getName() {
		return this.getParentTestCreator().getName();
	}

	@Override
	public int getInstanceNumber() {
		return this.instanceNumber;
	}
	
	public boolean shouldExecuteSetUpMethodInstanceFixture(){
//		if (this.wasUnSelected() || this.wasSkipped()){
//			return false;
//		} else 
			
		if (this.wasExcluded() && (this.getExclusionType() != TestResultCode.ERROR_IN_SETUP_METHOD_INSTANCE)){
			return false;
		}
		
		return true;
	}
	
	public boolean shouldExecuteTearDownMethodInstanceFixture(){
//		if (this.wasUnSelected() || this.wasSkipped()){
//			return false;
//		} else 
			
		if (this.wasExcluded() && (this.getExclusionType() != TestResultCode.ERROR_IN_SETUP_METHOD_INSTANCE)){
			return false;
		}
		
		return true;
	}
	
	public TestFixtures getTestFixtures() {
		return this.getParentTestCreator().getTestFixtures();
	}
		
}
