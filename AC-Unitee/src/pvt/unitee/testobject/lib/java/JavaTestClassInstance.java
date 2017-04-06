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
import pvt.arjunapro.enums.IssueSubType;
import pvt.arjunapro.enums.IssueType;
import pvt.arjunapro.enums.TestClassFixtureType;
import pvt.arjunapro.enums.TestResultCode;
import pvt.batteries.config.Batteries;
import pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.issue.IssueBuilder;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.interfaces.TestContainer;
import pvt.unitee.testobject.lib.interfaces.TestContainerFragment;
import pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import pvt.unitee.testobject.lib.interfaces.TestCreator;
import pvt.unitee.testobject.lib.loader.DataMethodsHandler;

public class JavaTestClassInstance extends BaseTestObject implements TestContainerInstance {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private int instanceNumber;
	private Object testObject = null;
	private JavaTestClassDefinition classDef = null;
	private JavaTestClass container = null;
	
	private int creatorThreadCount = 1;
	
	private List<JavaTestMethod> methodsQueue = new ArrayList<JavaTestMethod>();
	private Set<TestCreator> methodExecTracker = new HashSet<TestCreator>();
	private List<String> executableCreatorNames = new ArrayList<String>();
	
	private Set<String> allScheduledCreators = new HashSet<String>();
	private int currentFragmentNumber = 0;
	private TestContainerFragment currentFragment = null;
	
	public JavaTestClassInstance(int instanceNumber, String objectId, JavaTestClassDefinition classDef, JavaTestClass container) throws Exception {
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
		
		initFixtures(TestClassFixtureType.SETUP_CLASS_INSTANCE, TestClassFixtureType.TEARDOWN_CLASS_INSTANCE);
		if (this.getSetUpFixture() != null){
			this.getSetUpFixture().setTestContainerInstance(this);	
		}
		
		if (this.getTearDownFixture() != null){
			this.getTearDownFixture().setTestContainerInstance(this);			
		}
		
		this.setIgnoreExclusionTestResultCode(TestResultCode.ERROR_IN_SETUP_CLASS_INSTANCE);
		
		try{
			switch(this.getConstructorType()){
			case NO_ARG:
				this.setUserTestClassObject(this.getConstructor().newInstance());
				break;
			case SINGLEARG_TESTVARS:
				if (ArjunaInternal.displayTestObjConstructionInfo){
					logger.debug(String.format("Calling Test Var constructor for %s", this.getQualifiedName()));
					logger.debug(this.getTestVariables().utv().strItems());
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

	@Override
	public void loadFragment(List<String> methods) throws Exception{
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Loading Fragment");
			logger.debug(methods);
		}
		
		String fragmentObjectId = String.format("%s|Fragment-%d", this.getObjectId(), ++currentFragmentNumber);
		
		this.currentFragment = new JavaTestClassFragment(currentFragmentNumber, fragmentObjectId, this.classDef, this.container, this);
		currentFragment.setCreatorNames(methods);
		currentFragment.loadTestCreators();
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
	public synchronized boolean hasCompleted() {
		return this.allScheduledCreators.size() == 0;
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
	public void setAllScheduledCreators(List<String> creatorNames) {
		if (creatorNames != null){
			this.allScheduledCreators.addAll(creatorNames);
		}
	}

	@Override
	public TestContainerFragment getCurrentFragment() {
		return this.currentFragment;
	}

	@Override
	public void markCurrentFragmentCompleted(TestContainerFragment fragment) {
		for (JavaTestMethod m: fragment.getTestCreators()){
			this.allScheduledCreators.remove(m.getName());
		}
		currentFragment = null;
	}
}
