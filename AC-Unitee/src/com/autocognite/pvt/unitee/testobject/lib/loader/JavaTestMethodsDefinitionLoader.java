package com.autocognite.pvt.unitee.testobject.lib.loader;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

import org.apache.commons.io.FilenameUtils;
import org.apache.log4j.Logger;

import com.autocognite.arjuna.annotations.DriveWithData;
import com.autocognite.arjuna.annotations.DriveWithDataArray;
import com.autocognite.arjuna.annotations.DriveWithDataFile;
import com.autocognite.arjuna.annotations.DriveWithDataGenerator;
import com.autocognite.arjuna.annotations.DriveWithDataMethod;
import com.autocognite.arjuna.annotations.Instances;
import com.autocognite.arjuna.annotations.Skip;
import com.autocognite.arjuna.annotations.TestMethod;
import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.batteries.config.RunConfig;
import com.autocognite.batteries.util.DataBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.SkipCode;
import com.autocognite.pvt.unitee.core.lib.datasource.DataSourceBuilder;
import com.autocognite.pvt.unitee.core.lib.datasource.DataSourceType;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import com.autocognite.pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;

public class JavaTestMethodsDefinitionLoader implements TestCreatorLoader {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private JavaTestClassDefinition testClassDef = null;
	private TestDefinitionsLoader javaTestClassLoader = null;
	
	public JavaTestMethodsDefinitionLoader(TestDefinitionsLoader parentLoader, JavaTestClassDefinition classDef) throws Exception{
		this.setContainer(classDef);
		this.javaTestClassLoader = parentLoader;
	}
	
	private boolean isTestMethod(Method m){
		return m.isAnnotationPresent(TestMethod.class) || m.getName().startsWith("test");
	}
	
	private void processSelection(Method m, JavaTestMethodDefinition methodDef){
		if (m.isAnnotationPresent(Skip.class)){
			methodDef.setSkipped(SkipCode.SKIPPED_METHOD_ANNOTATION);
		}		
	}
	
	private void addFilteredMethodNameToTree(String mQualifiedName){
		TestDefinitionsDB.getDependencyTreeBuilder().addFilteredCreator(mQualifiedName);
	}
	
	public void loadDefinitions() throws Exception{
		HashMap<String,Method> methodMap = new HashMap<String,Method>();
		ArrayList<String> methodNames = new ArrayList<String>();
		
		JavaTestClassFixturesLoader fixtureLoader = new JavaTestClassFixturesLoader(testClassDef);

		Class<?> userTestClass = this.getTestClassDef().getUserTestClass();
		
		HashMap<String,DataSourceType> methodDSMap = new HashMap<String,DataSourceType>();
		for (Method m: userTestClass.getDeclaredMethods()){
			String mName = m.getName();
			String mQualifiedName = userTestClass.getName() + "." + mName;
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug(mName);
			}
			
			boolean isTestMethod = this.isTestMethod(m);
			boolean anyDataDriveAnnPresent = false;

			if (m.isAnnotationPresent(DriveWithData.class)){
				anyDataDriveAnnPresent = true;
				methodDSMap.put(mName, DataSourceType.DATA);
			} else if (m.isAnnotationPresent(DriveWithDataArray.class)){
				anyDataDriveAnnPresent = true;
				methodDSMap.put(mName, DataSourceType.DATA_ARRAY);				
			} else if (m.isAnnotationPresent(DriveWithDataMethod.class)){
				anyDataDriveAnnPresent = true;
				methodDSMap.put(mName, DataSourceType.DATA_METHOD);					
			} else if (m.isAnnotationPresent(DriveWithDataGenerator.class)) {
				anyDataDriveAnnPresent = true;
				methodDSMap.put(mName, DataSourceType.DATA_GENERATOR);				
			} else if (m.isAnnotationPresent(DriveWithDataFile.class)) {
				anyDataDriveAnnPresent = true;
				methodDSMap.put(mName, DataSourceType.DATA_FILE);					
			}
			
			if (isTestMethod || anyDataDriveAnnPresent){
				methodMap.put(mName, m);
				methodNames.add(mName);
			} else {
				getTestClassDef().addNonTestMethodName(m.getName());
				fixtureLoader.loadFixture(m);
			}
		}

		TestFixtures fixtures = fixtureLoader.build(); 
		this.getTestClassDef().setFixtures(fixtures);

		Collections.sort(methodNames);
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Registering methods for test class: %s", userTestClass.getName()));
		}
		
		for(String mName: methodNames){
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug(String.format("Method Name: %s", mName));
			}
			Method m = methodMap.get(mName);
			String mQualifiedName = userTestClass.getName() + "." + mName;
			JavaTestMethodDefinition methodDef = new JavaTestMethodDefinition();
			methodDef.setClassDefinition(this.getTestClassDef());
			methodDef.setMethod(m);
			processSelection(m, methodDef);
			int testThreadCount = JavaTestLoadingUtils.getTestThreadCount(m);
			if (testThreadCount < 1){
				System.err.println(String.format("Test Thread count must be >=1. Correction needed for: %s", methodDef.getQualifiedName()));
				System.err.println("Exiting...");
				System.exit(1);
			}
			methodDef.setTestThreadCount(testThreadCount);
			
			boolean hasDataSourceAnn = false;
			// Data Source
			if (methodDSMap.containsKey(mName)){
				DataSourceBuilder builder = new DataSourceBuilder();
				builder.testClassDef(testClassDef);
				builder.dataSourceType(methodDSMap.get(mName));
				builder.testMethod(m);
				builder.process();
				methodDef.setDataSourceBuilder(builder);
				hasDataSourceAnn = true;
			}
			
			// For Data ref processing
			methodDef.setDataRefPresent(JavaTestLoadingUtils.isDataRefPresent(m));
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("Data Ref Present? " + methodDef.isDataRefPresent());
			}
			
			if (methodDef.isDataRefPresent()){
				String dataRefName = JavaTestLoadingUtils.getDataRefName(m);
				String filePath = JavaTestLoadingUtils.getDataRefPath(m);
				if (dataRefName.equals("NOT_SET")){
					dataRefName = FilenameUtils.getBaseName(filePath).toUpperCase();
				}
				if (ArjunaInternal.displayLoadingInfo){
					logger.debug(String.format("Now registering data reference with name %s.", dataRefName));
				}
				methodDef.addFileDataRefWithPath(dataRefName, filePath);
			}
			
			boolean instancesAnnotationPresent = JavaTestLoadingUtils.isInstancesAnnotationPresent(m);
			boolean hasUserSuppliedProperties = false;
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("Instances Annotation Present? " + instancesAnnotationPresent);
			}
			Instances instancesAnn = null;
			HashMap<Integer,HashMap<String,String>> instanceProps = new HashMap<Integer,HashMap<String,String>>();
			if (instancesAnnotationPresent){
				if (ArjunaInternal.displayLoadingInfo){
					logger.debug("Found @Instances Annotation");
				}
				instancesAnn = (Instances) m.getAnnotation(Instances.class);
				int instanceCount = JavaTestLoadingUtils.getInstancesCount(instancesAnn);
				if (instanceCount == -1){
					System.err.println(String.format("Instance count must be >=1. Correction needed for: %s", methodDef.getQualifiedName()));
					System.err.println("Exiting...");
					System.exit(1);
				}
				
				int instanceThreadCount = JavaTestLoadingUtils.getInstanceThreadCount(instancesAnn);
				if (instanceThreadCount == -1){
					System.err.println(String.format("Instance Thread count must be >=1. Correction needed for: %s", methodDef.getQualifiedName()));
					System.err.println("Exiting...");
					System.exit(1);
				}
				
				methodDef.setInstanceCount(instanceCount);
				methodDef.setInstanceThreadCount(instanceThreadCount);
				if (ArjunaInternal.displayInstanceProcessingInfo){
					logger.debug("Instance Count: " + methodDef.getInstanceCount());
				}
				hasUserSuppliedProperties = JavaTestLoadingUtils.hasUserSuppliedProperties(mQualifiedName, instancesAnn);
				if (ArjunaInternal.displayUDVProcessingInfo){
					logger.debug("User has supplied UDVs: " + hasUserSuppliedProperties);
				}
			}
			
			boolean testVarsAreMandatory = hasUserSuppliedProperties || methodDef.isDataRefPresent() || hasDataSourceAnn;
			this.populateExpectedSignature(m, methodDef, mQualifiedName, testVarsAreMandatory);
			instanceProps = JavaTestLoadingUtils.loadUDVFromInstancesAnnotation(instancesAnn, methodDef.getInstanceCount(), hasUserSuppliedProperties);	
			
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("Adding instances. count=" + methodDef.getInstanceCount());
			}
			for (int i=1; i <= methodDef.getInstanceCount(); i++){
				methodDef.setUdvForInstance(i, instanceProps.get(i));
			}
			
			this.getTestClassDef().addTestMethodDefinition(mName, methodDef);
			
			TestDefinitionsDB.getDependencyTreeBuilder().createNode(mQualifiedName, methodDef);
		}		
	}

	public JavaTestClassDefinition getTestClassDef() {
		return testClassDef;
	}
//	
//	public JavaTestClass getJavaTestClass() {
//		return container;
//	}

	private void setContainer(JavaTestClassDefinition container) {
		this.testClassDef = container;
	}
	
	private void populateExpectedSignature(Method m, JavaTestMethodDefinition methodDef, String mQualifiedName, boolean testVarsAreMandatory){
		//validate
		JavaTestMethodSignatureType sigType = null;

		String mName = m.getName();
		Class<?>[] paramTypes = m.getParameterTypes();
		StringBuilder builder = new StringBuilder();
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
		String currentMethodSignatureString = String.format("Your current test method signature is: %s(%s)", m.getName(), argString);
		String expectedSigntureString = null;
		String expectedArgPrefix = null;
		if (paramTypes.length > 1){
			if (testVarsAreMandatory){
				logger.debug("Unsupported signature, requires Test Variables args");
				expectedArgPrefix = "TestVariables testMethodVars";
				expectedSigntureString = String.format("public void %s(%s)", mName, expectedArgPrefix);
				System.err.println(String.format("Your usage of annotations would not work with current method signature: %s", mQualifiedName));
				System.err.println(currentMethodSignatureString);
				System.err.println(String.format("You must provide the test method signature as: %s", expectedSigntureString));
				System.err.println("Exiting...");
				System.exit(1);	
			} else {
				logger.debug("Unsupported signature, Test Variables arg is optional.");
				expectedArgPrefix = "TestVariables testMethodVars";
				String option1 = String.format("public void %s(%s)", mName, expectedArgPrefix);
				String option2 = String.format("public void %s()", mName);
				System.err.println(String.format("You are using an unsupported test method signature for: %s", mQualifiedName));
				System.err.println(currentMethodSignatureString);
				System.err.println("Following are allowed signatures for your usage:");
				System.err.println(String.format("Option 1: %s", option1));
				System.err.println(String.format("Option 2: %s", option2));
				System.err.println("Exiting...");
				System.exit(1);	
			}								
		} else if (paramTypes.length == 1){
			expectedArgPrefix = "TestVariables testVars";
			expectedSigntureString = String.format("public void %s(%s)", mName, expectedArgPrefix);
			if (TestVariables.class.equals(paramTypes[0].getClass())){
				System.err.println(String.format("Your usage of annotations would not work with current method signature: %s", mQualifiedName));
				System.err.println(currentMethodSignatureString);
				System.err.println(String.format("You must provide the test method signature as: %s", expectedSigntureString));
				System.err.println("Exiting...");
				System.exit(1);					
			} else {
				sigType = JavaTestMethodSignatureType.SINGLEARG_TESTVARS;
			}
				
		} else if (paramTypes.length == 0){
			if (testVarsAreMandatory){
				expectedArgPrefix = "TestVariables testMethodVars";
				expectedSigntureString = String.format("public void %s(%s)", mName, expectedArgPrefix);
				System.err.println(String.format("Your usage of annotations would not work with current method signature: %s", mQualifiedName));
				System.err.println(currentMethodSignatureString);
				System.err.println(String.format("You must provide the test method signature as: %s", expectedSigntureString));
				System.err.println("Exiting...");
				System.exit(1);	
			} else {
				expectedSigntureString = String.format("public void %s()", mName);
				sigType = JavaTestMethodSignatureType.NO_ARG;
			}
		}
		methodDef.setMethodSignatureType(sigType);
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Expected Test Signature Type: " + sigType);
			logger.debug("Expected Test Signature: " + expectedSigntureString);
		}
	}

}
