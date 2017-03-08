package com.autocognite.pvt.unitee.testobject.lib.java;

import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.internal.arjuna.enums.TestObjectType;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;
import com.autocognite.pvt.arjuna.enums.TestResultCode;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.unitee.core.lib.dependency.DependencyHandler;
import com.autocognite.pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import com.autocognite.pvt.unitee.reporter.lib.IssueId;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import com.autocognite.pvt.unitee.testobject.lib.fixture.Fixture;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainer;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import com.autocognite.pvt.unitee.testobject.lib.loader.DataMethodsHandler;
import com.autocognite.pvt.unitee.testobject.lib.loader.group.Group;

public class JavaTestClass extends BaseTestObject implements TestContainer {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private JavaTestClassDefinition classDef = null;
	private Class<?> testClass = null;
	private Constructor<?> constructor = null;
	private TestClassConstructorType constructorType = null;
	private List<String> instanceObjectIDs = new ArrayList<String>();
	private HashMap<String,JavaTestClassInstance> instanceExecTracker = new HashMap<String,JavaTestClassInstance>();
	private List<JavaTestClassInstance> instanceQueue = new ArrayList<JavaTestClassInstance>();
	private List<String> executableCreatorNames = new ArrayList<String>();
	private boolean instancesCreated = false;
	private ArrayList<DependencyHandler> dependencies = new ArrayList<DependencyHandler>();
	private static Fixture setUpSessionFixture = null;
	private static Fixture tearDownSessionFixture = null;
	private static Fixture setUpClassFixture = null;
	private static Fixture tearDownClassFixture = null;
	private boolean firstObject = true;
	
	public JavaTestClass(JavaTestClassDefinition classDef) throws Exception{
		super(Thread.currentThread().getName() + "|" + classDef.getUserTestClass().getName(), TestObjectType.TEST_CLASS);
		this.setQualifiedName(classDef.getUserTestClass().getName());
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Creating Test Container Object: %s", this.getQualifiedName()));
		}
		this.classDef = classDef;
		this.setConstructor(classDef.getConstructor());
		this.setTestClass(classDef.getUserTestClass());
		this.setConstructorType(classDef.getConstructorType());
		this.setTestVarsHandler(new DefaultTestVarsHandler(this));
		
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Number of dependencies for %s: %s", this.getQualifiedName(), this.classDef.getDependencies().size()));
		}
		for (DependencyHandler dep: this.classDef.getDependencies()){
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug(String.format("Adding dep for %s: %s", this.getQualifiedName(), dep));
			}
			this.addDependency(dep);
		}
		
		this.setThreadId(Thread.currentThread().getName());
		if (firstObject){
			
			setUpClassFixture = this.getTestFixtures().getFixture(TestClassFixtureType.SETUP_CLASS);
			if (setUpClassFixture != null){
				setUpClassFixture.setTestObject(this);
			}
			
			tearDownClassFixture = this.getTestFixtures().getFixture(TestClassFixtureType.TEARDOWN_CLASS);
			if (tearDownClassFixture != null){
				tearDownClassFixture.setTestObject(this);
			}
		}

	}
	
	@Override
	public FixtureResultType getSetUpSessionFixtureResult() {
		if (this.setUpSessionFixture != null){
			return this.setUpSessionFixture.getResultType();
		} else {
			return FixtureResultType.SUCCESS;
		}
	}

	@Override
	public FixtureResultType getTearDownSessionFixtureResult() {
		if (this.tearDownSessionFixture != null){
			return this.tearDownSessionFixture.getResultType();
		} else {
			return FixtureResultType.SUCCESS;
		}
	}
	
	@Override
	public void setGroup(Group g) throws Exception{
		this.getTestVariables().rawUdv().add(g.getUDV());
		this.getTestVariables().rawObjectProps().setSessionNodeName(g.getSessionNode().getName());
		this.getTestVariables().rawObjectProps().setSessionNodeId(g.getSessionNode().getId());
		this.getTestVariables().rawObjectProps().setSessionSubNodeId(g.getSessionSubNode().getId());
		this.getTestVariables().rawObjectProps().setGroupName(g.getName());
	}
	
	public void addDependency(DependencyHandler dep){
		this.dependencies.add(dep);
	}
	
	@Override
	public boolean shouldExecute(IssueId outId){
		if (ArjunaInternal.displayDependencyDefInfo){
			logger.debug(String.format("Check whether dependencies are met for %s.", this.getQualifiedName()));
		}
		for (DependencyHandler dep: dependencies){
			if (!dep.isMet(outId)){
				if (ArjunaInternal.displayDependencyDefInfo){
					logger.debug("Dependencies NOT met for " + this.getQualifiedName());
				}
				return false;
			}
		}
		
		if (ArjunaInternal.displayDependencyDefInfo){
			logger.debug("Dependencies met for " + this.getQualifiedName());
		}
		return true;
	}
	
	public void load() throws Exception{
		// Create Instances
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Creating instances...");
		}

		for (int i=1; i <= classDef.getInstanceCount(); i++){
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug(String.format("Creating instance #%d", i));
			}
			this.createInstance(i);
		}
		instancesCreated = true;
	}

	public Class<?> getUserTestClass() {
		return testClass;
	}

	private void setTestClass(Class<?> testClass) {
		this.testClass = testClass;
	}
	
	public String getUserTestClassName(){
		return this.getUserTestClass().getSimpleName();
	}

	private Constructor<?> getConstructor() {
		return constructor;
	}

	private void setConstructor(Constructor<?> constructor) {
		this.constructor = constructor;
	}

	private TestClassConstructorType getConstructorType() {
		return constructorType;
	}

	private void setConstructorType(TestClassConstructorType constructorType) {
		this.constructorType = constructorType;
	}

	public void createInstance(int instanceNumber) throws Exception {
		String instanceId = String.format("%s|TCC%d", this.getObjectId(), instanceNumber);
		JavaTestClassInstance classClone = new JavaTestClassInstance(instanceNumber, instanceId, this, this.classDef);
		this.instanceExecTracker.put(instanceId, classClone);
		this.instanceQueue.add(classClone);
	}
	
	public void loadInstances() throws Exception{
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Loading instances...");
			logger.debug("Instance Queue: " + this.instanceQueue);
		}
		for (TestContainerInstance instance: this.instanceQueue){
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug(String.format("Loading instance #%d", instance.getInstanceNumber()));
				logger.debug(String.format("Configuring test methods: %s", this.executableCreatorNames));
			}
			instance.resetExecutorCreatorQueue();
			for (String creatorName: this.executableCreatorNames){
				instance.addExecutableCreatorName(creatorName);
			}
			instance.loadTestCreators();
		}
	}

	@Override
	public int getInstanceCount() {
		return this.instanceQueue.size();
	}
	
	public TestFixtures getFixtures() {
		return this.classDef.getFixtures();
	}

	@Override
	public void addExecutableCreatorName(String name) {
		this.executableCreatorNames.add(name);
	}

	@Override
	public List<JavaTestClassInstance> getInstances() {
		return this.instanceQueue;
	}

	@Override
	public int getInstanceThreadCount() {
		return classDef.getInstanceThreadCount();
	}

	@Override
	public TestFixtures getTestFixtures() {
		return classDef.getFixtures();
	}

	@Override
	public DataMethodsHandler getDataMethodsHandler() {
		return classDef.getDataMethodsHandler();
	}

	@Override
	public void resetExecutorCreatorQueue() {
		this.executableCreatorNames = new ArrayList<String>();
	}

	@Override
	public TestVariables getTestVariablesDefinition() {
		return classDef.getTestVariables();
	}

	@Override
	public boolean areInstancesCreated() {
		return this.instancesCreated;
	}
	
	@Override
	public void setUpClass() throws Exception{
		if (ArjunaInternal.displayFixtureExecInfo){
			logger.debug("Inside Java Test Class Set Up Class.");
		}
		if (setUpClassFixture != null){
			boolean success = this.setUpClassFixture.execute();
			if (!success){
				this.markExcluded(
						TestResultCode.ERROR_IN_SETUP_CLASS, 
						String.format("Error in \"%s.%s\" fixture", this.setUpClassFixture.getFixtureClassName(), this.setUpClassFixture.getName()),
						this.setUpClassFixture.getIssueId());
			}
		}
	}

	@Override
	public void tearDownClass() throws Exception {
		if (tearDownClassFixture != null){
			boolean success = tearDownClassFixture.execute();
			if (!success){
				this.markExcluded(
						TestResultCode.ERROR_IN_TEARDOWN_CLASS, 
						String.format("Error in \"%s.%s\" fixture", this.tearDownClassFixture.getFixtureClassName(), this.tearDownClassFixture.getName()),
						this.tearDownClassFixture.getIssueId());
			}
		}
	}

	@Override
	public boolean wasSetUpClassFixtureExecuted() {
		if (this.setUpClassFixture != null){
			return this.setUpClassFixture.wasExecuted();
		} else {
			return true;
		}
	}
	
	@Override
	public boolean shouldExecuteTearDownClassFixture() {
		if (this.wasUnSelected() || this.wasSkipped()){
			return false;
		} else if (this.wasExcluded() && (this.getExclusionType() != TestResultCode.ERROR_IN_SETUP_CLASS)){
			return false;
		}
		
		return true;
	}
	
	@Override
	public boolean hasCompleted() {
		return this.instanceExecTracker.size() == 0;
	}
	
	@Override
	public void markTestClassInstanceCompleted(TestContainerInstance instance) {
		this.instanceExecTracker.remove(instance.getObjectId());
	}
}
