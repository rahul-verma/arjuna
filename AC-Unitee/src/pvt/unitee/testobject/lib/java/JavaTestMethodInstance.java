package pvt.unitee.testobject.lib.java;

import java.lang.reflect.Method;

import org.apache.log4j.Logger;

import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.ddt.interfaces.DataSource;
import com.arjunapro.testauto.enums.TestObjectType;
import com.arjunapro.testauto.exceptions.DataSourceFinishedException;
import com.arjunapro.testauto.interfaces.TestVariables;

import pvt.arjunapro.enums.FixtureResultType;
import pvt.arjunapro.enums.TestClassFixtureType;
import pvt.arjunapro.enums.TestResultCode;
import pvt.batteries.config.Batteries;
import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import pvt.unitee.testobject.lib.fixture.Fixture;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.interfaces.Test;
import pvt.unitee.testobject.lib.interfaces.TestCreator;
import pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

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
		this.dataSource =  this.methodDef.getDataSource();
		
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
	
	public TestFixtures getTestFixtures() {
		return this.getParentTestCreator().getTestFixtures();
	}
		
}
