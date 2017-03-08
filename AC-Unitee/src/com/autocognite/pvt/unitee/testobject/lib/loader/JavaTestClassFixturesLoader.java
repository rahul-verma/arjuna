package com.autocognite.pvt.unitee.testobject.lib.loader;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.annotations.*;
import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.console.Console;
import com.autocognite.arjuna.utils.DataBatteries;
import com.autocognite.arjuna.utils.SystemBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;
import com.autocognite.pvt.unitee.reporter.lib.reportable.ReportableFactory;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import com.autocognite.pvt.unitee.testobject.lib.fixture.*;

public class JavaTestClassFixturesLoader {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private JavaTestClassDefinition classDef = null;
	private Fixture setUpSessionFixture = null;
	private Fixture tearDownSessionFixture = null;
	private Fixture setUpClassFixture = null;
	private Fixture tearDownClassFixture = null;
	private Fixture setUpClassInstanceFixture = null;
	private Fixture tearDownClassInstanceFixture = null;
	private Fixture setUpClassFragmentFixture = null;
	private Fixture tearDownClassFragmentFixture = null;
	private Fixture setUpMethodFixture = null;
	private Fixture tearDownMethodFixture = null;
	private Fixture setUpMethodInstanceFixture = null;
	private Fixture tearDownMethodInstanceFixture = null;
	private Fixture setUpTestFixture = null;
	private Fixture tearDownTestFixture = null;
	String sep = SystemBatteries.getLineSeparator();
	
	private HashMap<TestClassFixtureType, ArrayList<String>> fixtureCounts = new HashMap<TestClassFixtureType, ArrayList<String>>();
	private boolean fixtureAnomaly = false;
	
	public JavaTestClassFixturesLoader(JavaTestClassDefinition container) throws Exception{
		this.setContainer(container);
	}
	
	private boolean isBeforeClassFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeClass.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPCLASS_NAME).asString()));	
	}
	
	private boolean isAfterClassFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterClass.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNCLASS_NAME).asString()));	
	}
	
	private boolean isBeforeClassInstanceFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeClassInstance.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPCLASSINSTANCE_NAME).asString()));	
	}
	
	private boolean isAfterClassInstanceFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterClassInstance.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNCLASSINSTANCE_NAME).asString()));	
	}

	private boolean isBeforeClassFragmentFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeClassInstance.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPCLASSFRAGMENT_NAME).asString()));	
	}
	
	private boolean isAfterClassFragmentFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterClassInstance.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNCLASSFRAGMENT_NAME).asString()));	
	}
	
	private boolean isBeforeMethodFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeMethod.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPMETHOD_NAME).asString()));	
	}
	
	private boolean isAfterMethodFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterMethod.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNMETHOD_NAME).asString()));	
	}
	
	private boolean isBeforeMethodInstanceFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeMethodInstance.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPMETHODINSTANCE_NAME).asString()));	
	}
	
	private boolean isAfterMethodInstanceFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterMethodInstance.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNMETHODINSTANCE_NAME).asString()));	
	}
	
	private boolean isBeforeTestFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeTest.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPTEST_NAME).asString()));	
	}
	
	private boolean isAfterTestFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterTest.class) || 
				m.getName().equals(RunConfig.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNTEST_NAME).asString()));	
	}
	
	public void incrementFixtureCount(HashMap<TestClassFixtureType, ArrayList<String>> tracker, TestClassFixtureType type, String fixtureName){
		if (!tracker.containsKey(type)){
			tracker.put(type, new ArrayList<String>());
		} else {
			fixtureAnomaly = true;
		}
		tracker.get(type).add(fixtureName);	
	}
	
	private void validateStatic(Method m) throws Exception{
		if (!Modifier.isStatic(m.getModifiers())){
			String msg = String.format("Test Class: %s. Found anomaly in fixture:%s. This fixture needs to be static."
					, classDef.getUserTestClass().getName(),m.getName());
			Console.displayError("!!!ALERT!!!");
			Console.displayError(msg);
			Console.displayError("Exiting...");
			System.exit(1);			
		}
	}
	
	private void validatePublic(Method m) throws Exception{
		if (!Modifier.isPublic(m.getModifiers())){
			String msg = String.format("Test Class: %s. Found anomaly in fixture:%s. Fixture methods should be public."
					, classDef.getUserTestClass().getName(),m.getName());
			Console.displayError("!!!ALERT!!!");
			Console.displayError(msg);
			Console.displayError("Exiting...");
			System.exit(1);			
		}
	}
	
	public void loadFixture(Method m) throws Exception{
		if (ArjunaInternal.displayFixtureProcessingInfo){
			logger.debug(String.format("Processing fixtures for %s", this.classDef.getQualifiedName()));
		}
		
		if (this.isBeforeClassFixture(m)){
			validatePublic(m);
			validateStatic(m);
			setUpClassFixture = new StaticFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_CLASS, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_CLASS, m.getName());
		} else if (this.isAfterClassFixture(m)){
			validatePublic(m);
			validateStatic(m);
			tearDownClassFixture = new StaticFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_CLASS, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_CLASS, m.getName());
		} else if (this.isBeforeClassInstanceFixture(m)){
			validatePublic(m);
			setUpClassInstanceFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_CLASS_INSTANCE, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_CLASS_INSTANCE, m.getName());
		} else if (this.isAfterClassInstanceFixture(m)){
			validatePublic(m);
			tearDownClassInstanceFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_CLASS_INSTANCE, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_CLASS_INSTANCE, m.getName());
		} else if (this.isBeforeClassFragmentFixture(m)){
			validatePublic(m);
			setUpClassFragmentFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_CLASS_FRAGMENT, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_CLASS_FRAGMENT, m.getName());
		} else if (this.isAfterClassFragmentFixture(m)){
			validatePublic(m);
			tearDownClassFragmentFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_CLASS_FRAGMENT, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_CLASS_FRAGMENT, m.getName());
		} else if (this.isBeforeMethodFixture(m)){
			validatePublic(m);
			setUpMethodFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_METHOD, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_METHOD, m.getName());
		} else if (this.isAfterMethodFixture(m)){
			validatePublic(m);
			tearDownMethodFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_METHOD, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_METHOD, m.getName());
		} else if (this.isBeforeMethodInstanceFixture(m)){
			validatePublic(m);
			setUpMethodInstanceFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_METHOD_INSTANCE, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_METHOD_INSTANCE, m.getName());
		} else if (this.isAfterMethodInstanceFixture(m)){
			validatePublic(m);
			tearDownMethodInstanceFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_METHOD_INSTANCE, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_METHOD_INSTANCE, m.getName());
		} else if (this.isBeforeTestFixture(m)){
			validatePublic(m);
			setUpTestFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_TEST, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_TEST, m.getName());
		} else if (this.isAfterTestFixture(m)){
			validatePublic(m);
			tearDownTestFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_TEST, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_TEST, m.getName());
		}
	}
	
	public JavaTestClassDefinition getJavaTestClass() {
		return classDef;
	}

	private void setContainer(JavaTestClassDefinition container) {
		this.classDef = container;
	}
	
	private void validate() throws Exception{
		if (fixtureAnomaly){
			StringBuilder sb = new StringBuilder();
			for (TestClassFixtureType fixture: fixtureCounts.keySet()){
				ArrayList<String> names = fixtureCounts.get(fixture);
				if (names.size() > 1){
					sb.append(String.format("Fixture Type: %s%s", fixture.toString(), sep));
					sb.append(DataBatteries.flatten(names));
					sb.append(sep);
				}
			}
			
			String msg = String.format("Test Class: %s%sFound anomaly in fixtures.%sDuplicate fixtures detected.%sCheck annotation usage.%s"
					, classDef.getUserTestClass().getName(),sep,sep,sep,sep);
			logger.error("!!!ALERT!!!");			
			ArjunaInternal.getReporter().update(ReportableFactory.createAlert(
					"Test Scheduler",
					msg + sb.toString()));
			logger.error(msg);
			logger.error("Exiting...");
			ArjunaInternal.getReporter().tearDown();
			System.exit(1);
		}		
	}
	
	public TestFixtures build() throws Exception{
		validate();
		return new TestClassFixtures(
				setUpClassFixture,
				tearDownClassFixture,
				setUpClassInstanceFixture,
				tearDownClassInstanceFixture, 
				setUpClassFragmentFixture,
				tearDownClassFragmentFixture, 
				setUpMethodFixture,
				tearDownMethodFixture, 
				setUpMethodInstanceFixture,
				tearDownMethodInstanceFixture, 
				setUpTestFixture, 
				tearDownTestFixture
		);
	}
}
