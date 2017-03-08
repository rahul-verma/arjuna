package com.autocognite.pvt.unitee.testobject.lib.java;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.annotations.TestMethod;
import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.internal.arjuna.enums.TestObjectType;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.SkipCode;
import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;
import com.autocognite.pvt.arjuna.enums.TestResultCode;
import com.autocognite.pvt.arjuna.enums.UnpickedCode;
import com.autocognite.pvt.unitee.core.lib.dependency.DependencyHandler;
import com.autocognite.pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import com.autocognite.pvt.unitee.reporter.lib.IssueId;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import com.autocognite.pvt.unitee.testobject.lib.fixture.Fixture;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreator;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

public class JavaTestMethod extends BaseTestObject implements TestCreator{
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private JavaTestMethodDefinition methodDef = null;
	private Method method = null;
	private String mName = null;;
	private HashMap<String,JavaTestMethodInstance> instanceExecTracker = new HashMap<String,JavaTestMethodInstance>();
	private List<JavaTestMethodInstance> methodInstanceQueue = new ArrayList<JavaTestMethodInstance>();
	private int instanceCount;
	private Fixture setUpMethodFixture = null;
	private Fixture tearDownMethodFixture = null;
	private JavaTestClassInstance containerInstance;
	private ArrayList<DependencyHandler> dependencies = new ArrayList<DependencyHandler>();
	private TestFixtures fixtures = null;
	
	public JavaTestMethod(String objectId, JavaTestClassInstance containerInstance, JavaTestMethodDefinition methodDef) throws Exception {
		super(objectId, TestObjectType.TEST_METHOD);
		this.containerInstance = containerInstance;
		this.methodDef = methodDef;
		this.method = methodDef.getMethod();
		this.mName =  this.method.getName();
		this.setQualifiedName(this.methodDef.getQualifiedName());
		this.setTestVarsHandler(new DefaultTestVarsHandler(this, containerInstance));
		this.setThreadId(Thread.currentThread().getName());
		// Override object properties
//		this.getTestVariables().rawObjectProps().setName(mName);
		
		this.instanceCount = methodDef.getInstanceCount();
		
		// Create Instances
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Creating Method instances");
		}
		for (int i=1; i <= instanceCount; i++){
			this.createInstance(i);
		}
		
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Number of dependencies for %s: %s", this.getQualifiedName(), this.methodDef.getDependencies().size()));
		}
		for (DependencyHandler dep: this.methodDef.getDependencies()){
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug(String.format("Adding dep for %s: %s", this.getQualifiedName(), dep));
			}
			this.addDependency(dep);
		}
		
		this.setUpMethodFixture = this.getTestFixtures().getFixture(TestClassFixtureType.SETUP_METHOD);
		if (setUpMethodFixture != null){
			setUpMethodFixture.setTestContainerInstance(this.getTestContainerInstance());
			setUpMethodFixture.setTestObject(this);
		}
		this.tearDownMethodFixture = this.getTestFixtures().getFixture(TestClassFixtureType.TEARDOWN_METHOD);
		if (tearDownMethodFixture != null){
			tearDownMethodFixture.setTestContainerInstance(this.getTestContainerInstance());
			tearDownMethodFixture.setTestObject(this);
		}
		
		if (methodDef.isUnpicked()){
			this.markUnSelected(
					  TestResultCode.valueOf(UnpickedCode.UNPICKED_METHOD.toString()),
					  String.format("%s not selected.", methodDef.getQualifiedName())
			);						
		} else if (methodDef.shouldBeSkipped()){
			this.markSkipped(
					  TestResultCode.valueOf(SkipCode.SKIPPED_METHOD_ANNOTATION.toString()),
					  String.format("%s has @Skip.", methodDef.getQualifiedName())
			);							
		}
	}

	private TestFixtures getTestFixtures() {
		return this.containerInstance.getTestFixtures();
	}

	private void createInstance(int i) throws Exception {
		String instanceId = String.format("%s|Instance-%d", this.getObjectId(), i);
		JavaTestMethodInstance methodInstance = new JavaTestMethodInstance(i, instanceId, this, this.methodDef);
		this.methodInstanceQueue.add(methodInstance);
		instanceExecTracker.put(methodInstance.getObjectId(), methodInstance);
	}

	@Override
	public TestVariables getTestVariablesDefinition() {
		return methodDef.getTestVariables();
	}

	@Override
	public List<JavaTestMethodInstance> getInstances() {
		return this.methodInstanceQueue;
	}

	@Override
	public int getInstanceThreadCount() {
		return this.methodDef.getInstanceThreadCount();
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

	public String getName() {
		return this.mName;
	}

	public JavaTestClassInstance getParent() {
		return this.containerInstance;
	}

	@Override
	public JavaTestClassInstance getTestContainerInstance() {
		return this.containerInstance;
	}
	
	@Override
	public boolean hasCompleted() {
		return this.instanceExecTracker.size() == 0;
	}
	
	@Override
	public void markTestMethodInstanceCompleted(TestCreatorInstance instance) {
		this.instanceExecTracker.remove(instance.getObjectId());
	}
	
	@Override
	public boolean shouldExecuteTearDownMethodFixture() {
		if (this.wasUnSelected() || this.wasSkipped()){
			return false;
		} else if (this.wasExcluded() && (this.getExclusionType() != TestResultCode.ERROR_IN_SETUP_METHOD)){
			return false;
		}
		
		return true;
	}
	
	@Override
	public void setUpMethod() throws Exception{
		if (ArjunaInternal.displayFixtureExecInfo){
			logger.debug("Inside Java Test Class Set Up Class.");
		}
		if (setUpMethodFixture != null){
			boolean success = this.setUpMethodFixture.execute();
			if (!success){
				this.markExcluded(
						TestResultCode.ERROR_IN_SETUP_METHOD, 
						String.format("Error in \"%s.%s\" fixture", this.setUpMethodFixture.getFixtureClassName(), this.setUpMethodFixture.getName()),
						this.setUpMethodFixture.getIssueId());
			}
		}
	}

	@Override
	public void tearDownMethod() throws Exception {
		if (tearDownMethodFixture != null){
			boolean success = tearDownMethodFixture.execute();
			if (!success){
				this.markExcluded(
						TestResultCode.ERROR_IN_TEARDOWN_CLASS, 
						String.format("Error in \"%s.%s\" fixture", this.tearDownMethodFixture.getFixtureClassName(), this.tearDownMethodFixture.getName()),
						this.tearDownMethodFixture.getIssueId());
			}
		}
	}
	
	@Override
	public boolean wasSetUpMethodFixtureExecuted() {
		if (this.setUpMethodFixture != null){
			return this.setUpMethodFixture.wasExecuted();
		} else {
			return true;
		}
	}
}


