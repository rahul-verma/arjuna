package com.autocognite.pvt.unitee.testobject.lib.java;

import java.lang.reflect.Method;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.exceptions.DataSourceFinishedException;
import com.autocognite.arjuna.interfaces.DataSource;
import com.autocognite.arjuna.interfaces.DataRecord;
import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.internal.arjuna.enums.TestObjectType;
import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;
import com.autocognite.pvt.arjuna.enums.TestResultCode;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import com.autocognite.pvt.unitee.testobject.lib.fixture.Fixture;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.Test;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreator;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

public class JavaTestMethodInstance extends BaseTestObject implements TestCreatorInstance{
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private int instanceNumber;
	private JavaTestMethod jMethod;
	private Method method;
	private JavaTestMethodDefinition methodDef = null;
	private Fixture setUpMethodFixture = null;
	private Fixture tearDownMethodFixture = null;
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
		this.dataSource =  this.methodDef.getDataSource();
		
		JavaTestClassInstance classInstance = this.getParentTestCreator().getTestContainerInstance();
		this.setUpMethodFixture = classInstance.getTestFixtures().getFixture(TestClassFixtureType.SETUP_METHOD_INSTANCE);
		if (setUpMethodFixture != null){
			setUpMethodFixture.setTestContainerInstance(classInstance);
			setUpMethodFixture.setTestObject(this);
		}
		this.tearDownMethodFixture = classInstance.getTestFixtures().getFixture(TestClassFixtureType.TEARDOWN_METHOD_INSTANCE);
		if (tearDownMethodFixture != null){
			tearDownMethodFixture.setTestContainerInstance(classInstance);
			tearDownMethodFixture.setTestObject(this);
		}
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
	public FixtureResultType getSetUpMethodFixtureResult() {
		if (this.setUpMethodFixture != null){
			return this.setUpMethodFixture.getResultType();
		} else {
			return FixtureResultType.SUCCESS;
		}
	}

	@Override
	public FixtureResultType getTearDownMethodFixtureResult() {
		if (this.tearDownMethodFixture != null){
			return this.tearDownMethodFixture.getResultType();
		} else {
			return FixtureResultType.SUCCESS;
		}
	}
	
	@Override
	public boolean wasSetUpMethodInstanceFixtureExecuted(){
		if (this.setUpMethodFixture != null){
			return this.setUpMethodFixture.wasExecuted();
		} else {
			return true;
		}
	}
	
	@Override
	public boolean didSetUpMethodFixtureSucceed(){
		if (this.setUpMethodFixture != null){
			return this.setUpMethodFixture.wasSuccessful();
		} else {
			return true;
		}
	}
	
	@Override
	public boolean wasTearDownMethodFixtureExecuted(){
		if (this.tearDownMethodFixture != null){
			return this.setUpMethodFixture.wasExecuted();
		} else {
			return true;
		}
	}
	
	@Override
	public boolean didTearDownMethodFixtureSucceed(){
		if (this.tearDownMethodFixture != null){
			return this.setUpMethodFixture.wasSuccessful();
		} else {
			return true;
		}
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
	public JavaTestClassInstance getTestContainerInstance() {
		return this.jMethod.getParent();
	}

	@Override
	public synchronized Test next() throws Exception {
		try{
//			logger.debug("Check if next Test Wrapper is available for: " + this.getTestContainer().getAuthoredTest().getUserTestClassQualifiedName() + "." + this.method.getName());
			DataRecord dataRecord = this.dataSource.next();
			this.currentTestNumber += 1;
			String testObjectId = String.format("%s|TestNumber-%d", this.getObjectId(), this.currentTestNumber);
			Test test = new JavaTest(currentTestNumber, testObjectId, this, methodDef);
			lastTest = test;
			test.setDataRecord(dataRecord);
			return test;
		} catch (DataSourceFinishedException e) {
//			logger.debug("No further sub-tests. All done.");
			//runTearDownFixtures();
			throw new SubTestsFinishedException("All Done.");
		}
	}

	public String getName() {
		return this.getParentTestCreator().getName();
	}

	@Override
	public int getInstanceNumber() {
		return this.instanceNumber;
	}
	
	@Override
	public void setUpMethodInstance() throws Exception{
		if (this.setUpMethodFixture != null){
			boolean success = this.setUpMethodFixture.execute();
			if (!success){
				this.markExcluded(
						TestResultCode.ERROR_IN_SETUP_METHOD_INSTANCE, 
						String.format("Error in \"%s.%s\" fixture", this.setUpMethodFixture.getFixtureClassName(), this.setUpMethodFixture.getName()),
						this.setUpMethodFixture.getIssueId()
				);
						
			}
		}
	}

	@Override
	public void tearDownMethodInstance() throws Exception {
		if (this.tearDownMethodFixture != null){
			boolean success = tearDownMethodFixture.execute();
			if (!success){
				this.markExcluded(
						TestResultCode.ERROR_IN_TEARDOWN_METHOD_INSTANCE, 
						String.format("Error in \"%s.%s\" fixture", this.tearDownMethodFixture.getFixtureClassName(), this.tearDownMethodFixture.getName()),
						this.tearDownMethodFixture.getIssueId()
				);
			}
		}
	}
	
	public boolean shouldExecuteSetUpMethodInstanceFixture(){
		if (this.wasUnSelected() || this.wasSkipped()){
			return false;
		} else if (this.wasExcluded() && (this.getExclusionType() != TestResultCode.ERROR_IN_SETUP_METHOD_INSTANCE)){
			return false;
		}
		
		return true;
	}
	
	public boolean shouldExecuteTearDownMethodInstanceFixture(){
		if (this.wasUnSelected() || this.wasSkipped()){
			return false;
		} else if (this.wasExcluded() && (this.getExclusionType() != TestResultCode.ERROR_IN_SETUP_METHOD_INSTANCE)){
			return false;
		}
		
		return true;
	}
		
}
