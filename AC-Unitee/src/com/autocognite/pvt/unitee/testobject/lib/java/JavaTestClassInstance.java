package com.autocognite.pvt.unitee.testobject.lib.java;

import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.enums.TestObjectType;
import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.arjuna.enums.IssueSubType;
import com.autocognite.pvt.arjuna.enums.IssueType;
import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;
import com.autocognite.pvt.arjuna.enums.TestResultCode;
import com.autocognite.pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import com.autocognite.pvt.unitee.reporter.lib.issue.Issue;
import com.autocognite.pvt.unitee.reporter.lib.issue.IssueBuilder;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import com.autocognite.pvt.unitee.testobject.lib.fixture.Fixture;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainer;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreator;
import com.autocognite.pvt.unitee.testobject.lib.loader.DataMethodsHandler;

public class JavaTestClassInstance extends BaseTestObject implements TestContainerInstance {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private int instanceNumber;
	private Object testObject = null;
	private JavaTestClass container = null;
	private List<JavaTestMethod> methodsQueue = new ArrayList<JavaTestMethod>();
	private JavaTestClassDefinition classDef = null;
	private Fixture setUpClassInstanceFixture = null;
	private Fixture tearDownClassInstanceFixture = null;
	private Fixture setUpClassFragmentFixture = null;
	private Fixture tearDownClassFragmentFixture = null;
	private Set<TestCreator> methodExecTracker = new HashSet<TestCreator>();
	private int creatorThreadCount = 1;
	private List<String> executableCreatorNames = new ArrayList<String>();
	
	public JavaTestClassInstance(int instanceNumber, String objectId, JavaTestClass container, JavaTestClassDefinition classDef) throws Exception {
		super(objectId, TestObjectType.TEST_CLASS_INSTANCE);
		this.instanceNumber = instanceNumber;
		this.container = container;
		this.classDef = classDef;
		this.setQualifiedName(container.getQualifiedName());
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Populating Test Variables for %s instance# %d", this.getQualifiedName(), this.instanceNumber));
		}
		this.setTestVarsHandler(new DefaultTestVarsHandler(this, container));
		
		this.getTestVariables().rawObjectProps().setClassInstanceNumber(this.instanceNumber);
		this.setThreadId(Thread.currentThread().getName());
		
		this.setUpClassInstanceFixture = this.getTestFixtures().getFixture(TestClassFixtureType.SETUP_CLASS_INSTANCE);
		if (setUpClassInstanceFixture != null){
			setUpClassInstanceFixture.setTestContainerInstance(this);
			setUpClassInstanceFixture.setTestObject(this);
		}
		this.tearDownClassInstanceFixture = this.getTestFixtures().getFixture(TestClassFixtureType.TEARDOWN_CLASS_INSTANCE);
		if (tearDownClassInstanceFixture != null){
			tearDownClassInstanceFixture.setTestContainerInstance(this);
			tearDownClassInstanceFixture.setTestObject(this);
		}
		
		this.setUpClassFragmentFixture = this.getTestFixtures().getFixture(TestClassFixtureType.SETUP_CLASS_FRAGMENT);
		if (setUpClassFragmentFixture != null){
			setUpClassFragmentFixture.setTestContainerInstance(this);
			setUpClassFragmentFixture.setTestObject(this);
		}
		this.tearDownClassFragmentFixture = this.getTestFixtures().getFixture(TestClassFixtureType.TEARDOWN_CLASS_FRAGMENT);
		if (tearDownClassFragmentFixture != null){
			tearDownClassFragmentFixture.setTestContainerInstance(this);
			tearDownClassFragmentFixture.setTestObject(this);
		}
		
		try{
			switch(this.getConstructorType()){
			case NO_ARG:
				this.setUserTestClassObject(this.getConstructor().newInstance());
				break;
			case SINGLEARG_TESTVARS:
				if (ArjunaInternal.displayTestObjConstructionInfo){
					logger.debug(String.format("Calling Test Var constructor for %s", this.getQualifiedName()));
					logger.debug(this.getTestVariables().udv().strItems());
				}
				this.setUserTestClassObject(this.getConstructor().newInstance(this.getTestVariables()));
				break;	
			}
		} catch (java.lang.reflect.InvocationTargetException g) {
			Throwable f = null;
			if (g.getTargetException().getCause() == null){
				logger.debug(g.getTargetException().getMessage());
				f = g.getTargetException();
			} else {
				logger.debug(g.getTargetException().getMessage());
				f = g.getTargetException().getCause();
				g.getTargetException().getCause().printStackTrace();
			}
			processContainerConstructorException(f);
		}catch (Throwable e){
			logger.debug(e.getMessage());
			e.printStackTrace();
			processContainerConstructorException(e);
		}
	}
	
	private void processContainerConstructorException(Throwable e) throws Exception{
		int issueId = ArjunaInternal.getCentralExecState().getIssueId();
		IssueBuilder builder = new IssueBuilder();
		Issue issue = builder
		.testVariables(this.getTestVariables())
		.exception(e)
		.type(IssueType.CONSTRUCTOR)
		.subType(IssueSubType.CONSTRUCTOR)
		.id(issueId)
		.build();
		ArjunaInternal.getReporter().update(issue);
		this.markExcluded(
				TestResultCode.TEST_CONTAINER_CONSTRUCTOR_ERROR, 
				String.format("Error in constructor of %s", this.getUserTestContainer().getSimpleName()),
				issueId);		
	}

	public void loadTestCreators() throws Exception{
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Loading test creators");
			logger.debug(this.executableCreatorNames);
		}
		JavaTestMethod testMethod = null;
		for (String creatorName: this.executableCreatorNames){
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug(creatorName);
			}
			String methodObjectId = String.format("%s|%s", this.getObjectId(), creatorName);
			testMethod = new JavaTestMethod(methodObjectId, this, classDef.getTestCreatorDefinition(creatorName));
			this.methodsQueue.add(testMethod);
			methodExecTracker.add(testMethod);
		}
	}

	private void setUserTestClassObject(Object testObject) {
		this.testObject = testObject;
	}

	@Override
	public TestContainer getContainer() {
		return container;
	}

	public Class<?> getTestClass() {
		return classDef.getUserTestClass();
	}

	private Constructor<?> getConstructor() {
		return classDef.getConstructor();
	}

	private TestClassConstructorType getConstructorType() {
		return classDef.getConstructorType();
	}

	@Override
	public TestVariables getTestVariablesDefinition() {
		return this.classDef.getTestContainerInstanceDefinition(this.instanceNumber);
	}

	@Override
	public String getQualifiedName() {
		return this.classDef.getQualifiedName();
	}

	@Override
	public int getInstanceNumber() {
		return this.instanceNumber;
	}

	public Object getUserTestContainerObject() {
		return this.testObject;
	}

	@Override
	public List<JavaTestMethod> getTestCreators() {
		return this.methodsQueue;
	}
	
	@Override
	public FixtureResultType getSetUpClassFixtureResult() {
		if (this.setUpClassInstanceFixture != null){
			return this.setUpClassInstanceFixture.getResultType();
		} else {
			return FixtureResultType.SUCCESS;
		}
	}

	@Override
	public FixtureResultType getTearDownClassFixtureResult() {
		if (this.tearDownClassInstanceFixture != null){
			return this.tearDownClassInstanceFixture.getResultType();
		} else {
			return FixtureResultType.SUCCESS;
		}
	}

	@Override
	public FixtureResultType getSetUpClassFragmentFixtureResult() {
		if (this.setUpClassFragmentFixture != null){
			return this.setUpClassFragmentFixture.getResultType();
		} else {
			return FixtureResultType.SUCCESS;
		}
	}

	@Override
	public FixtureResultType getTearDownClassFragmentFixtureResult() {
		if (this.tearDownClassFragmentFixture != null){
			return this.tearDownClassFragmentFixture.getResultType();
		} else {
			return FixtureResultType.SUCCESS;
		}
	}
	
	@Override
	public boolean wasSetUpClassInstanceFixtureExecuted(){
		if (this.setUpClassInstanceFixture != null){
			return this.setUpClassInstanceFixture.wasExecuted();
		} else {
			return true;
		}
	}
	
	@Override
	public boolean didSetUpClassFixtureSucceed(){
		if (this.setUpClassInstanceFixture != null){
			return this.setUpClassInstanceFixture.wasSuccessful();
		} else {
			return true;
		}
	}
	
	@Override
	public boolean wasTearDownClassFixtureExecuted(){
		if (this.tearDownClassInstanceFixture != null){
			return this.tearDownClassInstanceFixture.wasExecuted();
		} else {
			return true;
		}
	}
	
	@Override
	public boolean didTearDownClassFixtureSucceed(){
		if (this.tearDownClassInstanceFixture != null){
			return this.tearDownClassInstanceFixture.wasSuccessful();
		} else {
			return true;
		}
	}

	@Override
	public boolean hasCompleted() {
		return this.methodExecTracker.size() == 0;
	}
	
	@Override
	public void markTestCreatorCompleted(TestCreator testCreator) {
		this.methodExecTracker.remove(testCreator);
	}

	@Override
	public int getCreatorThreadCount() {
		return classDef.getCreatorThreadCount();
	}

	@Override
	public Class<?> getUserTestContainer() {
		return classDef.getUserTestClass();
	}

	@Override
	public DataMethodsHandler getDataMethodsHandler() {
		return classDef.getDataMethodsHandler();
	}

	@Override
	public TestFixtures getTestFixtures() {
		return classDef.getFixtures();
	}

	@Override
	public void addExecutableCreatorName(String name) {
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Adding creator name for current execution slot: " + name);
		}
		this.executableCreatorNames.add(name);
		
	}
	
	@Override
	public void resetExecutorCreatorQueue() {
		this.executableCreatorNames = new ArrayList<String>();
		this.methodsQueue = new ArrayList<JavaTestMethod>();
	}
	
	@Override
	public void setUpClassInstance() throws Exception{
		if (ArjunaInternal.displayFixtureExecInfo){
			logger.debug("Inside Java Test Class Set Up Class.");
		}
		if (this.setUpClassInstanceFixture != null){
			boolean success = this.setUpClassInstanceFixture.execute();
			if (!success){
				this.markExcluded(
						TestResultCode.ERROR_IN_SETUP_CLASS_INSTANCE, 
						String.format("Error in \"%s.%s\" fixture", this.setUpClassInstanceFixture.getFixtureClassName(), this.setUpClassInstanceFixture.getName()),
						this.setUpClassInstanceFixture.getIssueId());
			}
		}
	}

	@Override
	public void tearDownClassInstance() throws Exception {
		if (this.tearDownClassInstanceFixture != null){
			boolean success = tearDownClassInstanceFixture.execute();
			if (!success){
				this.markExcluded(
						TestResultCode.ERROR_IN_TEARDOWN_CLASS_INSTANCE, 
						String.format("Error in \"%s.%s\" fixture", this.tearDownClassInstanceFixture.getFixtureClassName(), this.tearDownClassInstanceFixture.getName()),
						this.tearDownClassInstanceFixture.getIssueId());
			}
		}
	}
	
	@Override
	public void setUpClassFragment() throws Exception{
		if (ArjunaInternal.displayFixtureExecInfo){
			logger.debug("Inside Java Test Class Set Up Class.");
		}
		if (this.setUpClassFragmentFixture != null){
			boolean success = this.setUpClassFragmentFixture.execute();
			if (!success){
				this.markExcluded(
						TestResultCode.ERROR_IN_SETUP_CLASS_FRAGMENT, 
						String.format("Error in \"%s.%s\" fixture", this.setUpClassFragmentFixture.getFixtureClassName(), this.setUpClassFragmentFixture.getName()),
						this.setUpClassFragmentFixture.getIssueId());
			}
		}
	}

	@Override
	public void tearDownClassFragment() throws Exception {
		if (this.tearDownClassFragmentFixture != null){
			boolean success = tearDownClassFragmentFixture.execute();
			if (!success){
				this.markExcluded(
						TestResultCode.ERROR_IN_TEARDOWN_CLASS_FRAGMENT, 
						String.format("Error in \"%s.%s\" fixture", this.tearDownClassFragmentFixture.getFixtureClassName(), this.tearDownClassFragmentFixture.getName()),
						this.tearDownClassFragmentFixture.getIssueId());
			}
		}
	}

	@Override
	public boolean shouldExecuteTearDownClassInstanceFixture(){
		if (this.wasUnSelected() || this.wasSkipped()){
			return false;
		} else if (this.wasExcluded() && (this.getExclusionType() != TestResultCode.ERROR_IN_SETUP_CLASS_INSTANCE)){
			return false;
		}
		
		return true;
	}
	
	@Override
	public boolean shouldExecuteTearDownClassFragmentFixture() {
		if (this.wasUnSelected() || this.wasSkipped()){
			return false;
		} else if (this.wasExcluded() && (this.getExclusionType() != TestResultCode.ERROR_IN_SETUP_CLASS_FRAGMENT)){
			return false;
		}
		
		return true;
	}
}
