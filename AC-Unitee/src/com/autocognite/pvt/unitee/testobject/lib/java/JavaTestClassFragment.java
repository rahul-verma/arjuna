package com.autocognite.pvt.unitee.testobject.lib.java;

import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.internal.arjuna.enums.TestObjectType;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.arjuna.enums.IssueSubType;
import com.autocognite.pvt.arjuna.enums.IssueType;
import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;
import com.autocognite.pvt.arjuna.enums.TestResultCode;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.unitee.core.lib.metadata.DefaultTestVarsHandler;
import com.autocognite.pvt.unitee.core.lib.testvars.DefaultTestVariables;
import com.autocognite.pvt.unitee.reporter.lib.issue.Issue;
import com.autocognite.pvt.unitee.reporter.lib.issue.IssueBuilder;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import com.autocognite.pvt.unitee.testobject.lib.fixture.Fixture;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainer;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerFragment;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreator;
import com.autocognite.pvt.unitee.testobject.lib.loader.DataMethodsHandler;

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
		this.setTestVarsHandler(new DefaultTestVarsHandler(this, container));
		
		this.getTestVariables().rawObjectProps().setClassFragmentNumber(this.fragmentNumber);
		this.setThreadId(Thread.currentThread().getName());
		
		initFixtures(TestClassFixtureType.SETUP_CLASS_FRAGMENT, TestClassFixtureType.TEARDOWN_CLASS_FRAGMENT);
		this.getSetUpFixture().setTestContainerInstance(this.getContainerInstance());
		this.getTearDownFixture().setTestContainerInstance(this.getContainerInstance());
		this.getSetUpFixture().setTestContainerFragment(this);
		this.getTearDownFixture().setTestContainerFragment(this);
		
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
