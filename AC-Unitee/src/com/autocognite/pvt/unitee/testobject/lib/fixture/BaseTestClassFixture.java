package com.autocognite.pvt.unitee.testobject.lib.fixture;

import java.lang.reflect.Method;

import org.apache.log4j.Logger;

import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.arjuna.enums.IssueSubType;
import com.autocognite.pvt.arjuna.enums.IssueType;
import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.unitee.reporter.lib.fixture.FixtureResult;
import com.autocognite.pvt.unitee.reporter.lib.fixture.FixtureResultBuilder;
import com.autocognite.pvt.unitee.reporter.lib.issue.Issue;
import com.autocognite.pvt.unitee.reporter.lib.issue.IssueBuilder;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestObject;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestClassInstance;

public abstract class BaseTestClassFixture implements Fixture {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private Class<?> testClass = null;
	private Method method = null;
	private String fixtureName = null;
	private TestClassFixtureType type = null;
	private JavaTestClassInstance classInstance = null;
	private TestObject testObject = null;
	private FixtureResultType resultType = FixtureResultType.NOT_EXECUTED;
	private int issueId = -1;

	public BaseTestClassFixture(Class<?> testClass, TestClassFixtureType fType, Method m){
		this.setTestClass(testClass);
		this.setType(fType);
		this.setMethod(m);
		this.setName(m.getName());
	}
	
	public abstract void executeFixture() throws Exception;
	
	public boolean execute() throws Exception{

		try{
//			logger.debug(String.format("Executing fixture: %s.%s", testContainer.getUserTestClassQualifiedName(),fixture));
			this.executeFixture();
			//		} catch (java.lang.reflect.InvocationTargetException e){
			//			logger.debug(ExceptionBatteries.getStackTraceAsString(e.getTargetException()));
			//			reportFixtureError(test, type, e);
			//			return false;
		} catch (Throwable e){
			if (ArjunaInternal.logFixtureError){
				logger.debug(String.format("Error in fixture: %s.%s", this.getClass().getName(), this.getName()));
			}
			//			logger.debug(ExceptionBatteries.getStackTraceAsString(e));
			reportFixtureError(e);
			return false;
		}
		
		reportFixtureSuccess();
		return true;		
	}

	public Class<?> getTestClass() {
		return testClass;
	}

	public void setTestClass(Class<?> testClass) {
		this.testClass = testClass;
	}

	public Method getMethod() {
		return method;
	}

	public void setMethod(Method method) {
		this.method = method;
	}

	public TestClassFixtureType getType() {
		return type;
	}

	public void setType(TestClassFixtureType type) {
		this.type = type;
	}

	public JavaTestClassInstance getTestClassInstance() {
		return classInstance;
	}

	public void setTestContainerInstance(JavaTestClassInstance classInstance) {
		this.classInstance = classInstance;
	}
	
	@Override
	public TestObject getTestObject() {
		return this.testObject;
	}

	@Override
	public void setTestObject(TestObject testObject) {
		this.testObject  = testObject;
	}
	
	@Override
	public String getName() {
		return this.fixtureName;
	}
	
	@Override
	public String getFixtureClassName() {
		return this.testClass.getSimpleName();
	}
	
	public Fixture clone() throws CloneNotSupportedException{
		return null;	
	}

	public void setName(String fixtureName) {
		this.fixtureName = fixtureName;
	}
	
	private void reportFixtureError(Throwable e) throws Exception{
		Issue issueResult = this.getFixtureIssue(e);
		this.setResultType(FixtureResultType.ERROR);
		ArjunaInternal.getReporter().update(issueResult);
		FixtureResult fResult = this.getFixtureErrorResult(issueResult.resultProps().id());
		ArjunaInternal.getReporter().update(fResult);
	}
	
	private void reportFixtureSuccess() throws Exception{
		FixtureResultBuilder builder = new FixtureResultBuilder();
		FixtureResult result = builder
		.testVariables(this.getTestObject().getTestVariables())
		.type(this.getType())
		.result(FixtureResultType.SUCCESS)
		.execPoint(this.getFixturePoint())
		.method(this.getMethod().getName())
		.build();
		
		ArjunaInternal.getReporter().update(result);
	}
	
	private FixtureResult getFixtureErrorResult(int issueId) throws Exception{
		FixtureResultBuilder builder = new FixtureResultBuilder();
		return builder
		.testVariables(this.getTestObject().getTestVariables())
		.type(this.getType())
		.result(FixtureResultType.ERROR)
		.execPoint(this.getFixturePoint())
		.method(this.getMethod().getName())
		.issueId(issueId)
		.build();	
	}
	
	private Issue getFixtureIssue(Throwable e) throws Exception {
		try{
			throw e;
		}
		catch (java.lang.reflect.InvocationTargetException g) {
			if (ArjunaInternal.logFixtureError){
					logger.debug("Java Error in Reflected Method.");
			}
//				logger.debug(g.getMessage());
				if (g.getTargetException().getCause()  == null){
					return getFixtureIssueResult(g.getTargetException());
				} else {
					return getFixtureIssueResult(g.getTargetException().getCause());
				}
		} catch (Throwable h) {
			if (ArjunaInternal.logFixtureError){
				logger.debug("Java Error");
			}
			return getFixtureIssueResult(h);
		}
		
	}
	
	private IssueSubType getIssueSubTypeForFixtureType(){
		return IssueSubType.valueOf("FIXTURE_" + this.getType().toString());
	}
	
	private Issue getFixtureIssueResult(Throwable e) throws Exception{
		int issueId = ArjunaInternal.getCentralExecState().getIssueId();
		this.setIssueId(issueId);
		IssueBuilder builder = new IssueBuilder();
		return builder
		.testVariables(this.getTestObject().getTestVariables())
		.exception(e)
		.type(IssueType.FIXTURE)
		.subType(getIssueSubTypeForFixtureType())
		.fixtureName(this.getMethod().getName())
		.id(issueId)
		.build();
	}

	@Override
	public FixtureResultType getResultType() {
		return resultType;
	}

	protected void setResultType(FixtureResultType resultType) {
		this.resultType = resultType;
	}

	@Override
	public boolean wasExecuted(){
		return !(getResultType() == FixtureResultType.NOT_EXECUTED);
	}
	
	@Override
	public boolean wasSuccessful(){
		return getResultType() == FixtureResultType.SUCCESS;
	}

	public int getIssueId() {
		return issueId;
	}

	private void setIssueId(int intIssueId) {
		this.issueId = intIssueId;
	}
	
	protected String getFixturePoint() throws Exception {
		String qualifiedName = this.getTestObject().getTestVariables().objectProps().qualifiedName();
		String suffix = null;
		String suffix2 = null;
		String suffix3 = null;
		if (ArjunaInternal.displayFixtureExecInfo){
			logger.debug("Retreiving fixture execution point for: " + this.getTestObject().getTestVariables().objectProps().objectType());
		}
		switch (this.getTestObject().getTestVariables().objectProps().objectType()){
		case TEST_CLASS:
			suffix = String.format("For each occurance of Test Class [%s]. %%s instance.", qualifiedName);
			switch(this.getType()){		
			case SETUP_CLASS: return String.format(suffix, "before first");
			case TEARDOWN_CLASS: return String.format(suffix, "after last");
			}
			break;
		case TEST_CLASS_INSTANCE:
			suffix = String.format("all methods in Test Class - [%s], Class Instance #%d.", qualifiedName, this.getTestClassInstance().getInstanceNumber());
			suffix2 = String.format("all methods in Test Class - [%s], Class Instance #%d, Fragment.", qualifiedName, this.getTestClassInstance().getInstanceNumber());
			switch(this.getType()){		
			case SETUP_CLASS_INSTANCE: return String.format("For each occurance of a test class. Before %s", suffix);
			case TEARDOWN_CLASS_INSTANCE: return String.format("For each occurance of a test class. After %s", suffix);
			case SETUP_CLASS_FRAGMENT: return String.format("For each occurance of a test class. Before %s", suffix2);
			case TEARDOWN_CLASS_FRAGMENT: return String.format("For each occurance of a test class. After %s", suffix2);
			}
			break;
		case TEST_METHOD:
			suffix = String.format("all minstances of Test Method [%s]", this.getTestObject().getTestVariables().objectProps().name());
			switch(this.getType()){
			case SETUP_METHOD: return String.format("Before %s", suffix);
			case TEARDOWN_METHOD: return String.format("After %s", suffix);
			}
			break;
		case TEST_METHOD_INSTANCE:
			suffix = String.format("all tests created by Test Method [%s], Method Instance# %d.", this.getTestObject().getTestVariables().objectProps().name(), this.getTestObject().getTestVariables().objectProps().methodInstanceNumber());
			switch(this.getType()){
			case SETUP_METHOD_INSTANCE: return String.format("Before %s", suffix);
			case TEARDOWN_METHOD_INSTANCE: return String.format("After %s", suffix);
			}
			break;
		case TEST:
			suffix = String.format("Test Method [%s], Method Instance# %d, Test# %d",
					this.getTestObject().getTestVariables().objectProps().name(),
					this.getTestObject().getTestVariables().objectProps().methodInstanceNumber(),
					this.getTestObject().getTestVariables().objectProps().testNumber());
			switch(this.getType()){		
			case SETUP_TEST: return String.format("Before %s", suffix);
			case TEARDOWN_TEST: return String.format("After %s", suffix);
			}
			break;
		}

		return null;
	}
}
