package pvt.unitee.testobject.lib.java.loader;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.core.lib.datasource.DataSourceType;
import pvt.unitee.enums.SkipCode;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import unitee.annotations.DriveWithData;
import unitee.annotations.DriveWithDataArray;
import unitee.annotations.DriveWithDataFile;
import unitee.annotations.DriveWithDataGenerator;
import unitee.annotations.DriveWithDataMethod;
import unitee.annotations.Skip;
import unitee.annotations.TestMethod;

public class JavaTestMethodsDefLoader implements TestCreatorLoader {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private JavaTestClassDefinition testClassDef = null;
	private TestDefInitializer javaTestClassLoader = null;
	
	public JavaTestMethodsDefLoader(TestDefInitializer parentLoader, JavaTestClassDefinition classDef) throws Exception{
		this.setContainer(classDef);
		this.javaTestClassLoader = parentLoader;
	}
	
	private boolean isTestMethod(Method m){
		return m.isAnnotationPresent(TestMethod.class) || m.getName().startsWith("test");
	}
	
	private void processSkip(Method m, JavaTestMethodDefinition methodDef){
		if (m.isAnnotationPresent(Skip.class)){
			methodDef.setSkipped(SkipCode.SKIPPED_METHOD_ANNOTATION);
		}		
	}
	
	public void load() throws Exception{
		Map<String,Method> methodMap = new HashMap<String,Method>();
		List<String> methodNames = new ArrayList<String>();
		
		JavaTestClassFixturesLoader fixtureLoader = new JavaTestClassFixturesLoader(testClassDef);

		Class<?> userTestClass = this.getTestClassDef().getUserTestClass();
		
		Map<String,DataSourceType> methodDSMap = new HashMap<String,DataSourceType>();
		
		Map<String,Integer> testMethodCountMap = new HashMap<String,Integer>();
		
		boolean multiSameTestDefFound = false;
		
		for (Method m: userTestClass.getDeclaredMethods()){
			String mName = m.getName();
			String mQualifiedName = userTestClass.getName() + "." + mName;
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug(mName);
			}
			
			boolean isReserved = false;
			isReserved = AnnotationValidator.validateReservedNamedMethod(m, mQualifiedName);
			if (!isReserved){
				AnnotationValidator.validateMethodAnnotations(m, mQualifiedName);
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
				if (testMethodCountMap.containsKey(mName.toUpperCase())){
					multiSameTestDefFound = true;
					testMethodCountMap.put(mName.toUpperCase(), testMethodCountMap.get(mName.toUpperCase()) + 1);
				} else {
					testMethodCountMap.put(mName.toUpperCase(), 1);
				}
			} else {
				getTestClassDef().getFixturesLoader().addFixtureMethod(m);
				getTestClassDef().addNonTestMethodName(m.getName());
			}
		}

		if (multiSameTestDefFound){
			Console.displayError(String.format("There is a critical error with your test class: %s", userTestClass.getName()));
			Console.displayError(String.format("Arjuna found duplicate test method(s)."));
			Console.displayError(String.format("Test Method names should be unique in a class."));
			Console.displayError(String.format("For each of the following test method names, include only one definition of method."));
			Console.displayError(String.format("Arjuna follows case-insenstive approach for method naming."));
			for (String m: methodNames){
				if (testMethodCountMap.get(m.toUpperCase()) > 1){
					Console.displayError("- " + m);
				}	
			}
			Console.display("");
			Console.displayError("Exiting...");
			System.exit(1);
		}
		
		this.getTestClassDef().setDataSourceMap(methodDSMap);

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
			// Check for skipping
			processSkip(m, methodDef);
			
			this.getTestClassDef().registerTestMethodDefinition(mName, methodDef);
		}		
	}

	private JavaTestClassDefinition getTestClassDef() {
		return testClassDef;
	}

	private void setContainer(JavaTestClassDefinition container) {
		this.testClassDef = container;
	}
	
}
