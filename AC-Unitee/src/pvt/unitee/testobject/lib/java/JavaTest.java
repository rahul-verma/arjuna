package pvt.unitee.testobject.lib.java;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

import org.apache.log4j.Logger;

import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.testauto.enums.TestObjectType;
import com.arjunapro.testauto.interfaces.TestVariables;

import pvt.arjunapro.ArjunaInternal;
import pvt.arjunapro.enums.FixtureResultType;
import pvt.arjunapro.enums.TestClassFixtureType;
import pvt.arjunapro.enums.TestResultCode;
import pvt.arjunapro.enums.TestResultType;
import pvt.batteries.config.Batteries;
import pvt.batteries.utils.ExceptionBatteries;
import pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import pvt.unitee.reporter.lib.test.TestResult;
import pvt.unitee.reporter.lib.test.TestResultBuilder;
import pvt.unitee.reporter.lib.test.TestResultProperties;
import pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import pvt.unitee.testobject.lib.fixture.Fixture;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.interfaces.Test;

public class JavaTest extends BaseTestObject implements Test{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private int testNumber;
	private JavaTestMethodInstance parent;
	private JavaTestMethodDefinition methodDef;
	private DataRecord dataRecord = null;

	public JavaTest(int testNumber, String testObjectId, JavaTestMethodInstance javaTestMethodInstance, JavaTestMethodDefinition methodDef) throws Exception{
		super(testObjectId, TestObjectType.TEST);
		this.testNumber = testNumber;
		this.parent = javaTestMethodInstance;
		this.methodDef = methodDef;
		super.setQualifiedName(this.parent.getQualifiedName());
		
		this.setTestVarsHandler(new DefaultTestVarsHandler(this, javaTestMethodInstance));
		this.getTestVariables().rawObjectProps().setTestNumber(this.testNumber);
		this.setThreadId(Thread.currentThread().getName());
		
		initFixtures(TestClassFixtureType.SETUP_TEST, TestClassFixtureType.TEARDOWN_TEST);
		if (this.getSetUpFixture() != null){
			this.getSetUpFixture().setTestContainerInstance(this.getTestContainerFragment().getContainerInstance());
			this.getSetUpFixture().setTestContainerFragment(this.getTestContainerFragment());
		}
		
		if (this.getTearDownFixture() != null){
			this.getTearDownFixture().setTestContainerInstance(this.getTestContainerFragment().getContainerInstance());
			this.getTearDownFixture().setTestContainerFragment(this.getTestContainerFragment());
		}
		
		this.setIgnoreExclusionTestResultCode(TestResultCode.ERROR_IN_SETUP_TEST);
	}

	@Override
	public String getQualifiedName() {
		return this.parent.getQualifiedName();
	}

	@Override
	public int getTestNumber() {
		return this.testNumber;
	}

	@Override
	public JavaTestClassFragment getTestContainerFragment() {
		return this.parent.getTestContainerFragment();
	}

	@Override
	public String getName() {
		return parent.getName();
	}
	
	private static void addStepException(Throwable e) throws Exception{
		ArjunaInternal.getCentralExecState().getCurrentThreadState().addStepException(e);	
	}
	
	public void execute() throws Exception{		
		this.initTimeStamp();
		if (this.wasUnSelected()){
			this.endTimeStamp();
			reportUnselected();
			return;
		}
		
		if (this.wasSkipped()){
			this.endTimeStamp();
			reportSkipped();
			return;
		}
		
		if (this.wasExcluded()){
			this.endTimeStamp();
			reportExclusion();
			return;
		}

		//boolean success = false;
		try{
			this.beginTest();
			this.run();
			//success = true;
		} catch (InvocationTargetException e){
			if (ArjunaInternal.logTestExceptionTraces){
				logger.debug(ExceptionBatteries.getStackTraceAsString(e.getTargetException()));
			}
			addStepException(e);			
		} catch (Exception e){
			if (ArjunaInternal.logTestExceptionTraces){
				logger.debug(ExceptionBatteries.getStackTraceAsString(e));
			}
			addStepException(e);
		}
		
		this.endTimeStamp();
		this.endTest();
		//return success;		
	}

	public void run() throws Exception {
		Method m = this.methodDef.getMethod();
		Object userTestClassObject = this.parent.getParentTestCreator().getTestContainerFragment().getContainerInstance().getUserTestContainerObject();
		
		switch(this.methodDef.getMethodSignatureType()){
		case NO_ARG:
			m.invoke(userTestClassObject);
			break;
		case SINGLEARG_TESTVARS:
			m.invoke(userTestClassObject, this.getTestVariables());
			break;
		}
	}

	private String getTestMethodName() {
		return this.getTestMethod().getName();
	}

	private Method getTestMethod() {
		return methodDef.getMethod();
	}

	@Override
	public TestVariables getTestVariablesDefinition() {
		return this.methodDef.getTestVariables();
	}

	@Override
	public TestFixtures getTestFixtures() {
		return methodDef.getClassDefinition().getFixtures();
	}

	@Override
	public void setDataRecord(DataRecord dataRecord) {
		this.dataRecord = dataRecord;
		this.getTestVariables().setDataRecord(dataRecord);
	}

	@Override
	public JavaTestMethodInstance getParentCreatorInstance(){
		return this.parent;
	}
	
	private void reportExclusion() throws Exception {
		TestResultBuilder builder = new TestResultBuilder();
		TestResult result = builder
		.testVariables(this.getTestVariables())
		.result(TestResultType.EXCLUDED)
		.code(this.getExclusionType())
		.desc(this.getExclusionDesc())
		.issueId(this.getExclusionIssueId())
		.build();
		ArjunaInternal.getCentralExecState().update(result);
		ArjunaInternal.getCentralExecState().getCurrentThreadState().endTest();		
		ArjunaInternal.getReporter().update(result);
	}
	
	private void reportUnselected() throws Exception {
		TestResultBuilder builder = new TestResultBuilder();
		TestResult result = builder
		.testVariables(this.getTestVariables())
		.result(TestResultType.UNPICKED)
		.code(this.getUnSelectedType())
		.desc(this.getUnSelectedDesc())
		.build();
		ArjunaInternal.getCentralExecState().update(result);
		ArjunaInternal.getCentralExecState().getCurrentThreadState().endTest();		
		ArjunaInternal.getReporter().update(result);
	}
	
	private void reportSkipped() throws Exception {
		TestResultBuilder builder = new TestResultBuilder();
		TestResult result = builder
		.testVariables(this.getTestVariables())
		.result(TestResultType.SKIPPED)
		.code(this.getSkipType())
		.desc(this.getSkipDesc())
		.build();
		ArjunaInternal.getCentralExecState().update(result);
		ArjunaInternal.getCentralExecState().getCurrentThreadState().endTest();		
		ArjunaInternal.getReporter().update(result);
	}

	private void beginTest() throws Exception{
		ArjunaInternal.getCentralExecState().getCurrentThreadState().beginTest(this);
	}

	private void endTest() throws Exception{
		TestResult result = new TestResult(new TestResultProperties(), this.getTestVariables());
		result.buildFromStepResults(ArjunaInternal.getCentralExecState().getCurrentThreadState().getCurrentTestStepResults());
		ArjunaInternal.getCentralExecState().update(result);
		ArjunaInternal.getCentralExecState().getCurrentThreadState().endTest();
		ArjunaInternal.getReporter().update(result);
	}
}
