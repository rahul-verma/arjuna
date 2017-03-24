package pvt.unitee.testobject.lib.java;

import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.apache.log4j.Logger;

import com.arjunapro.testauto.enums.TestObjectType;
import com.arjunapro.testauto.interfaces.TestVariables;

import pvt.arjunapro.ArjunaInternal;
import pvt.arjunapro.enums.FixtureResultType;
import pvt.arjunapro.enums.IssueSubType;
import pvt.arjunapro.enums.IssueType;
import pvt.arjunapro.enums.TestClassFixtureType;
import pvt.arjunapro.enums.TestResultCode;
import pvt.batteries.config.Batteries;
import pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import pvt.unitee.core.lib.testvars.DefaultTestVariables;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.issue.IssueBuilder;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.fixture.Fixture;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.interfaces.TestContainer;
import pvt.unitee.testobject.lib.interfaces.TestContainerFragment;
import pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import pvt.unitee.testobject.lib.interfaces.TestCreator;
import pvt.unitee.testobject.lib.loader.DataMethodsHandler;

public class JavaTestClassFragment extends BaseTestObject implements TestContainerFragment {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	
	private int fragmentNumber;
	private Object testObject = null;
	private JavaTestClassDefinition classDef = null;
	private JavaTestClass container = null;
	private JavaTestClassInstance containerInstance = null;
	
	private int creatorThreadCount = 1;
	
	private List<JavaTestMethod> methodsQueue = new ArrayList<JavaTestMethod>();
	private List<String> executableCreatorNames = null;
	
	public JavaTestClassFragment(int fragmentNumber, String objectId, JavaTestClassDefinition classDef, JavaTestClass container, JavaTestClassInstance containerInstance) throws Exception {
		super(objectId, TestObjectType.TEST_CLASS_FRAGMENT);
		this.fragmentNumber = fragmentNumber;
		this.container = container;
		this.containerInstance = containerInstance;
		this.classDef = classDef;
		this.setQualifiedName(container.getQualifiedName());
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Populating Test Variables for %s instance# %d fragment# %d", this.getQualifiedName(), this.containerInstance.getInstanceNumber(), this.fragmentNumber));
		}
		this.setTestVarsHandler(new DefaultTestVarsHandler(this, containerInstance));
		
		this.getTestVariables().rawObjectProps().setClassFragmentNumber(this.fragmentNumber);
		this.setThreadId(Thread.currentThread().getName());
		
		initFixtures(TestClassFixtureType.SETUP_CLASS_FRAGMENT, TestClassFixtureType.TEARDOWN_CLASS_FRAGMENT);
		if (this.getSetUpFixture() != null){
			this.getSetUpFixture().setTestContainerInstance(this.getContainerInstance());
			this.getSetUpFixture().setTestContainerFragment(this);
		}
		
		if (this.getTearDownFixture() != null){
			this.getTearDownFixture().setTestContainerInstance(this.getContainerInstance());
			this.getTearDownFixture().setTestContainerFragment(this);			
		}
	
		this.setIgnoreExclusionTestResultCode(TestResultCode.ERROR_IN_SETUP_CLASS_FRAGMENT);
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
		}
	}

	@Override
	public TestContainer getContainer() {
		return container;
	}

	public Class<?> getTestClass() {
		return classDef.getUserTestClass();
	}

	@Override
	public TestVariables getTestVariablesDefinition() throws Exception {
		return new DefaultTestVariables();
//		return this.classDef.getTestContainerInstanceDefinition(this.instanceNumber);
	}

	@Override
	public String getQualifiedName() {
		return this.classDef.getQualifiedName();
	}

	public Object getUserTestContainerObject() {
		return this.testObject;
	}

	@Override
	public List<JavaTestMethod> getTestCreators() {
		return this.methodsQueue;
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
	public void setCreatorNames(List<String> names) {
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Adding creator names for class fragment: " + names);
		}
		this.executableCreatorNames = names;
		
	}

	@Override
	public int getFragmentNumber() {
		return this.fragmentNumber;
	}

	@Override
	public TestContainerInstance getContainerInstance() {
		return this.containerInstance;
	}
}
