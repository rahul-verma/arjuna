package com.autocognite.pvt.unitee.testobject.lib.loader;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.annotations.AfterClass;
import com.autocognite.arjuna.annotations.AfterClassFragment;
import com.autocognite.arjuna.annotations.AfterClassInstance;
import com.autocognite.arjuna.annotations.AfterMethod;
import com.autocognite.arjuna.annotations.AfterMethodInstance;
import com.autocognite.arjuna.annotations.AfterTest;
import com.autocognite.arjuna.annotations.BeforeClass;
import com.autocognite.arjuna.annotations.BeforeClassFragment;
import com.autocognite.arjuna.annotations.BeforeClassInstance;
import com.autocognite.arjuna.annotations.BeforeMethod;
import com.autocognite.arjuna.annotations.BeforeMethodInstance;
import com.autocognite.arjuna.annotations.BeforeTest;
import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.arjuna.utils.batteries.DataBatteries;
import com.autocognite.arjuna.utils.batteries.SystemBatteries;
import com.autocognite.arjuna.utils.console.Console;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.arjuna.enums.TestClassFixtureType;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.unitee.reporter.lib.reportable.ReportableFactory;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import com.autocognite.pvt.unitee.testobject.lib.fixture.BoundFixture;
import com.autocognite.pvt.unitee.testobject.lib.fixture.Fixture;
import com.autocognite.pvt.unitee.testobject.lib.fixture.StaticFixture;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestClassFixtures;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;

public class JavaTestClassFixturesLoader {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private JavaTestClassDefinition classDef = null;
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
	private List<Fixture> allFixtures = new ArrayList<Fixture>();

	private HashMap<TestClassFixtureType, ArrayList<String>> fixtureCounts = new HashMap<TestClassFixtureType, ArrayList<String>>();
	private boolean fixtureAnomaly = false;

	public JavaTestClassFixturesLoader(JavaTestClassDefinition container) throws Exception{
		this.setContainer(container);
	}

	private boolean isBeforeClassFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeClass.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPCLASS_NAME).asString()));	
	}

	private boolean isAfterClassFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterClass.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNCLASS_NAME).asString()));	
	}

	private boolean isBeforeClassInstanceFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeClassInstance.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPCLASSINSTANCE_NAME).asString()));	
	}

	private boolean isAfterClassInstanceFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterClassInstance.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNCLASSINSTANCE_NAME).asString()));	
	}

	private boolean isBeforeClassFragmentFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeClassFragment.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPCLASSFRAGMENT_NAME).asString()));	
	}

	private boolean isAfterClassFragmentFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterClassFragment.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNCLASSFRAGMENT_NAME).asString()));	
	}

	private boolean isBeforeMethodFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeMethod.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPMETHOD_NAME).asString()));	
	}

	private boolean isAfterMethodFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterMethod.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNMETHOD_NAME).asString()));	
	}

	private boolean isBeforeMethodInstanceFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeMethodInstance.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPMETHODINSTANCE_NAME).asString()));	
	}

	private boolean isAfterMethodInstanceFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterMethodInstance.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNMETHODINSTANCE_NAME).asString()));	
	}

	private boolean isBeforeTestFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(BeforeTest.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_SETUPTEST_NAME).asString()));	
	}

	private boolean isAfterTestFixture(Method m) throws Exception{
		return (m.isAnnotationPresent(AfterTest.class) || 
				m.getName().equals(Batteries.getCentralProperty(ArjunaProperty.FIXTURE_TESTCLASS_TEARDOWNTEST_NAME).asString()));	
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
			allFixtures.add(setUpClassFixture);
		} else if (this.isAfterClassFixture(m)){
			validatePublic(m);
			validateStatic(m);
			tearDownClassFixture = new StaticFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_CLASS, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_CLASS, m.getName());
			allFixtures.add(tearDownClassFixture);
		} else if (this.isBeforeClassInstanceFixture(m)){
			validatePublic(m);
			setUpClassInstanceFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_CLASS_INSTANCE, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_CLASS_INSTANCE, m.getName());
			allFixtures.add(setUpClassInstanceFixture);
		} else if (this.isAfterClassInstanceFixture(m)){
			validatePublic(m);
			tearDownClassInstanceFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_CLASS_INSTANCE, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_CLASS_INSTANCE, m.getName());
			allFixtures.add(tearDownClassInstanceFixture);
		} else if (this.isBeforeClassFragmentFixture(m)){
			validatePublic(m);
			setUpClassFragmentFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_CLASS_FRAGMENT, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_CLASS_FRAGMENT, m.getName());
			allFixtures.add(setUpClassFragmentFixture);
		} else if (this.isAfterClassFragmentFixture(m)){
			validatePublic(m);
			tearDownClassFragmentFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_CLASS_FRAGMENT, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_CLASS_FRAGMENT, m.getName());
			allFixtures.add(tearDownClassFragmentFixture);
		} else if (this.isBeforeMethodFixture(m)){
			validatePublic(m);
			setUpMethodFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_METHOD, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_METHOD, m.getName());
			allFixtures.add(setUpMethodFixture);
		} else if (this.isAfterMethodFixture(m)){
			validatePublic(m);
			tearDownMethodFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_METHOD, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_METHOD, m.getName());
			allFixtures.add(tearDownMethodFixture);
		} else if (this.isBeforeMethodInstanceFixture(m)){
			validatePublic(m);
			setUpMethodInstanceFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_METHOD_INSTANCE, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_METHOD_INSTANCE, m.getName());
			allFixtures.add(setUpMethodInstanceFixture);
		} else if (this.isAfterMethodInstanceFixture(m)){
			validatePublic(m);
			tearDownMethodInstanceFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_METHOD_INSTANCE, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_METHOD_INSTANCE, m.getName());
			allFixtures.add(tearDownMethodInstanceFixture);
		} else if (this.isBeforeTestFixture(m)){
			validatePublic(m);
			setUpTestFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.SETUP_TEST, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.SETUP_TEST, m.getName());
			allFixtures.add(setUpTestFixture);
		} else if (this.isAfterTestFixture(m)){
			validatePublic(m);
			tearDownTestFixture = new BoundFixture(this.classDef.getUserTestClass(), TestClassFixtureType.TEARDOWN_TEST, m);
			incrementFixtureCount(fixtureCounts, TestClassFixtureType.TEARDOWN_TEST, m.getName());
			allFixtures.add(tearDownTestFixture);
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
			Console.displayError("!!!ALERT!!!");
			Console.displayError(msg);
			Console.displayError(sb.toString());
			Console.displayError("Exiting...");
			System.exit(1);
		}		
	}

	public void populateSignatureTypes(){
		for (Fixture fixture: this.allFixtures){
			Class<?>[] paramTypes = fixture.getMethod().getParameterTypes();
			if ((paramTypes.length > 1) || ((paramTypes.length == 1) && (!TestVariables.class.equals(paramTypes[0])))){
				List<String> tStrings =  new ArrayList<String>();
				for (Class<?> t: paramTypes){
					tStrings.add(t.getSimpleName());
				}

				String argString = null;
				if (tStrings.size() == 0){
					argString = "";
				} else {
					argString = DataBatteries.join(tStrings, ",");
				}
				
				String staticPlug = "";
				
				if(StaticFixture.class.isAssignableFrom(fixture.getClass())){
					staticPlug = "static ";
				}

				String option1 = String.format("public %svoid %s(%s)", staticPlug, fixture.getMethod().getName(), "TestVariables testVars");
				String option2 = String.format("public %svoid %s()", staticPlug, fixture.getMethod().getName());

				Console.displayError(String.format("There is a critical issue with your test fixture: %s.%s", fixture.getFixtureClassName(), fixture.getMethod().getName()));
				Console.displayError(String.format("Your current fixture method signature is: %s(%s)", fixture.getMethod().getName(), argString));
				Console.displayError("Following are allowed signatures for your fixture method:");
				Console.displayError(String.format("Option 1: %s", option1));
				Console.displayError(String.format("Option 2: %s", option2));
				Console.displayError("Exiting...");
				System.exit(1);	

			}

			if (paramTypes.length == 0){
				fixture.setSignatureType(MethodSignatureType.NO_ARG);
			} else if (paramTypes.length == 1){
				fixture.setSignatureType(MethodSignatureType.SINGLEARG_TESTVARS);
			}

		}
	}

	public TestFixtures build() throws Exception{
		validate();
		populateSignatureTypes();
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
