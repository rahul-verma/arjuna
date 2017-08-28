package pvt.unitee.testobject.lib.java;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.core.lib.dependency.DependencyHandler;
import pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import pvt.unitee.enums.TestClassFixtureType;
import pvt.unitee.enums.TestResultCode;
import pvt.unitee.reporter.lib.IssueId;
import pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.interfaces.TestCreator;
import unitee.enums.TestObjectType;
import unitee.interfaces.TestVariables;

public class JavaTestMethod extends BaseTestObject implements TestCreator{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private JavaTestMethodDefinition methodDef = null;
	private Method method = null;
	private String mName = null;;
	private List<JavaTestMethodInstance> methodInstanceQueue = new ArrayList<JavaTestMethodInstance>();
	private int instanceCount;
	private JavaTestClassFragment containerFragment;
	private List<DependencyHandler> dependencies = new ArrayList<DependencyHandler>();
	private TestFixtures fixtures = null;
	
	public JavaTestMethod(String objectId, JavaTestClassFragment containerFragment, JavaTestMethodDefinition methodDef) throws Exception {
		super(objectId, TestObjectType.TEST_METHOD);
		this.containerFragment = containerFragment;
		this.methodDef = methodDef;
		this.method = methodDef.getMethod();
		this.mName =  this.method.getName();
		this.setQualifiedName(this.methodDef.getQualifiedName());
		this.setTestVarsHandler(new DefaultTestVarsHandler(this, containerFragment));
		this.setThreadId(Thread.currentThread().getName());
		// Override object properties
//		this.getTestVariables().rawObjectProps().setName(mName);
		
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Number of dependencies for %s: %s", this.getQualifiedName(), this.methodDef.getDependencies().size()));
		}
		for (DependencyHandler dep: this.methodDef.getDependencies()){
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug(String.format("Adding dep for %s: %s", this.getQualifiedName(), dep));
			}
			this.addDependency(dep);
		}
		
		initFixtures(TestClassFixtureType.SETUP_METHOD, TestClassFixtureType.TEARDOWN_METHOD);
		if (this.getSetUpFixture() != null){
			this.getSetUpFixture().setTestContainerInstance(this.getTestContainerFragment().getContainerInstance());
			this.getSetUpFixture().setTestContainerFragment(this.getTestContainerFragment());
		}
		
		if (this.getTearDownFixture() != null){
			this.getTearDownFixture().setTestContainerInstance(this.getTestContainerFragment().getContainerInstance());
			this.getTearDownFixture().setTestContainerFragment(this.getTestContainerFragment());			
		}

		this.setIgnoreExclusionTestResultCode(TestResultCode.ERROR_IN_SETUP_METHOD);
		
//		if (methodDef.isUnpicked()){
//			this.markUnSelected(
//					  TestResultCode.valueOf(UnpickedCode.UNPICKED_METHOD.toString()),
//					  String.format("%s not selected.", methodDef.getQualifiedName())
//			);						
//		} else if (methodDef.shouldBeSkipped()){
//			this.markSkipped(
//					  TestResultCode.valueOf(SkipCode.SKIPPED_METHOD_ANNOTATION.toString()),
//					  String.format("%s has @Skip.", methodDef.getQualifiedName())
//			);							
//		}
	}

	public TestFixtures getTestFixtures() {
		return this.containerFragment.getTestFixtures();
	}
	
	@Override
	public void loadInstances() throws Exception{
		this.instanceCount = methodDef.getInstanceCount();
		
		// Create Instances
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Creating Method instances");
		}
		for (int i=1; i <= instanceCount; i++){
			this.createInstance(i);
		}		
	}

	private void createInstance(int i) throws Exception {
		String instanceId = String.format("%s|Instance-%d", this.getObjectId(), i);
		JavaTestMethodInstance methodInstance = new JavaTestMethodInstance(i, instanceId, this, this.methodDef);
		methodInstance.setGroup(this.getGroup());
		this.methodInstanceQueue.add(methodInstance);
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
			if (!dep.isMet(this, outId)){
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

	public JavaTestClassFragment getParent() {
		return this.containerFragment;
	}

	@Override
	public JavaTestClassFragment getTestContainerFragment() {
		return this.containerFragment;
	}
}


