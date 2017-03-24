package pvt.unitee.testobject.lib.fixture;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.arjunapro.pvt.ArjunaInternal;
import com.arjunapro.sysauto.batteries.DataBatteries;
import com.arjunapro.testauto.interfaces.TestVariables;

import pvt.arjunapro.enums.FixtureResultType;
import pvt.arjunapro.enums.IssueSubType;
import pvt.arjunapro.enums.IssueType;
import pvt.arjunapro.enums.TestClassFixtureType;
import pvt.arjunapro.enums.TestResultCode;
import pvt.batteries.config.Batteries;
import pvt.unitee.reporter.lib.fixture.FixtureResult;
import pvt.unitee.reporter.lib.fixture.FixtureResultBuilder;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.issue.IssueBuilder;
import pvt.unitee.testobject.lib.interfaces.TestContainerFragment;
import pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import pvt.unitee.testobject.lib.interfaces.TestObject;
import pvt.unitee.testobject.lib.java.JavaTestClassFragment;
import pvt.unitee.testobject.lib.java.JavaTestClassInstance;
import pvt.unitee.testobject.lib.loader.MethodSignatureType;

public abstract class BaseTestClassFixture implements Fixture {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private Class<?> testClass = null;
	private Method method = null;
	private String fixtureName = null;
	private TestClassFixtureType type = null;
	private TestContainerInstance classInstance = null;
	private TestContainerFragment classFragment = null;
	private TestObject testObject = null;
	private FixtureResultType resultType = FixtureResultType.NOT_EXECUTED;
	private int issueId = -1;
	private TestResultCode errorCodeForFixture = TestResultCode.ALL_STEPS_PASS;
	private MethodSignatureType sigType = MethodSignatureType.NO_ARG;

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
			this.errorCodeForFixture = this.getErrorTestResultCode();
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

	public TestContainerInstance getTestClassInstance() {
		return classInstance;
	}

	public void setTestContainerInstance(TestContainerInstance classInstance) {
		this.classInstance = classInstance;
	}
	
	public TestContainerFragment getTestClassFragment() {
		return this.classFragment;
	}

	public void setTestContainerFragment(TestContainerFragment classFragment) {
		this.classFragment = classFragment;
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
		this.setResultType(FixtureResultType.SUCCESS);
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
		this.setResultType(FixtureResultType.ERROR);
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
	
	protected TestResultCode getErrorTestResultCode() throws Exception {
		return TestResultCode.valueOf(String.format("ERROR_IN_%s",this.getType().toString()));
	}
	
	protected String getFixturePoint() throws Exception {
		String qualifiedName = this.getTestObject().getTestVariables().object().qualifiedName();
		String suffix = null;
		String suffix2 = null;
		String suffix3 = null;
		if (ArjunaInternal.displayFixtureExecInfo){
			logger.debug("Retreiving fixture execution point for: " + this.getTestObject().getTestVariables().object().objectType());
		}
		switch (this.getTestObject().getTestVariables().object().objectType()){
		case TEST_CLASS:
			suffix = String.format("Within a group, once %%s Test Class [%s].", qualifiedName);
			switch(this.getType()){		
			case SETUP_CLASS: return String.format(suffix, "before");
			case TEARDOWN_CLASS: return String.format(suffix, "after");
			}
			break;
		case TEST_CLASS_INSTANCE:
			suffix = String.format("Once %%s Test Class [%s], Instance [%d]", qualifiedName, this.getTestClassInstance().getInstanceNumber());
			switch(this.getType()){		
			case SETUP_CLASS_INSTANCE: return String.format(suffix, "before");
			case TEARDOWN_CLASS_INSTANCE: return String.format(suffix, "after");
			}
			break;
		case TEST_CLASS_FRAGMENT:
			suffix = String.format("Once %%s Test Class [%s], Instance [%d], Fragment [%d]", qualifiedName, this.getTestClassInstance().getInstanceNumber(), this.getTestClassFragment().getFragmentNumber());
			switch(this.getType()){		
			case SETUP_CLASS_FRAGMENT: return String.format(suffix, "before");
			case TEARDOWN_CLASS_FRAGMENT: return String.format(suffix, "after");
			}
			break;
		case TEST_METHOD:
			suffix = String.format("Once %%s Test Class [%s], Instance [%d], Fragment [%d], Method [%s]", qualifiedName, 
					this.getTestClassInstance().getInstanceNumber(), this.getTestClassFragment().getFragmentNumber(),
					this.getTestObject().getTestVariables().object().name());
			switch(this.getType()){		
			case SETUP_METHOD: return String.format(suffix, "before");
			case TEARDOWN_METHOD: return String.format(suffix, "after");
			}
			break;
		case TEST_METHOD_INSTANCE:
			suffix = String.format("Once %%s Test Class [%s], Instance [%d], Fragment [%d], Method [%s], Method Instance [%d]", qualifiedName, 
					this.getTestClassInstance().getInstanceNumber(), this.getTestClassFragment().getFragmentNumber(),
					this.getTestObject().getTestVariables().object().name(),
					this.getTestObject().getTestVariables().object().methodInstanceNumber());
			switch(this.getType()){		
			case SETUP_METHOD_INSTANCE: return String.format(suffix, "before");
			case TEARDOWN_METHOD_INSTANCE: return String.format(suffix, "after");
			}
			break;
		case TEST:
			suffix = String.format("Once %%s Test Class [%s], Instance [%d], Fragment [%d], Method [%s], Method Instance [%d], Test [%d]", qualifiedName, 
					this.getTestClassInstance().getInstanceNumber(), this.getTestClassFragment().getFragmentNumber(),
					this.getTestObject().getTestVariables().object().name(),
					this.getTestObject().getTestVariables().object().methodInstanceNumber(),
					this.getTestObject().getTestVariables().object().testNumber());
			switch(this.getType()){		
			case SETUP_TEST: return String.format(suffix, "before");
			case TEARDOWN_TEST: return String.format(suffix, "after");
			}
			break;
		}

		return null;
	}
	
	@Override
	public TestResultCode getTestResultCodeForFixtureError() {
		return this.errorCodeForFixture;
	}

	public MethodSignatureType getSignatureType() {
		return sigType;
	}

	public void setSignatureType(MethodSignatureType sigType) {
		this.sigType = sigType;
	}
}
