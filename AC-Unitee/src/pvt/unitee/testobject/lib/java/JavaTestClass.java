package pvt.unitee.testobject.lib.java;

import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.log4j.Logger;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.core.lib.dependency.DependencyHandler;
import pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import pvt.unitee.enums.TestClassFixtureType;
import pvt.unitee.enums.TestResultCode;
import pvt.unitee.reporter.lib.IssueId;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.interfaces.TestContainer;
import pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import pvt.unitee.testobject.lib.java.loader.DataMethodsHandler;
import pvt.unitee.testobject.lib.loader.group.Group;
import unitee.enums.TestObjectType;
import unitee.interfaces.TestVariables;

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
	private List<String> allScheduledCreators = null;
	
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
			
		initFixtures(TestClassFixtureType.SETUP_CLASS, TestClassFixtureType.TEARDOWN_CLASS);
		this.setIgnoreExclusionTestResultCode(TestResultCode.ERROR_IN_SETUP_CLASS);
	}
	
	@Override
	public void setGroup(Group g) throws Exception{
		this.getTestVariables().rawExecVars().add(g.getExecVars());
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
			JavaTestClassInstance instance = this.createInstance(i);
			instance.setAllScheduledCreators(this.allScheduledCreators);
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

	private void setConstructor(Constructor<?> constructor) {
		this.constructor = constructor;
	}

	private void setConstructorType(TestClassConstructorType constructorType) {
		this.constructorType = constructorType;
	}

	public JavaTestClassInstance createInstance(int instanceNumber) throws Exception {
		String instanceId = String.format("%s|TCC%d", this.getObjectId(), instanceNumber);
		JavaTestClassInstance classClone = new JavaTestClassInstance(instanceNumber, instanceId, this.classDef, this);
		this.instanceExecTracker.put(instanceId, classClone);
		this.instanceQueue.add(classClone);
		return classClone;
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
			instance.loadFragment(executableCreatorNames);			
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
	public boolean hasCompleted() {
		return this.instanceExecTracker.size() == 0;
	}
	
	@Override
	public void markTestClassInstanceCompleted(TestContainerInstance instance) {
		this.instanceExecTracker.remove(instance.getObjectId());
	}

	@Override
	public void setAllScheduledCreators(List<String> creatorNames) {
		this.allScheduledCreators  = creatorNames;
	}

}
