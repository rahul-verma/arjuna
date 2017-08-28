package pvt.unitee.testobject.lib.java.processor;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.FilenameUtils;
import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import arjunasdk.sysauto.batteries.DataBatteries;
import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.core.lib.datasource.DataSourceBuilder;
import pvt.unitee.core.lib.datasource.DataSourceType;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import pvt.unitee.testobject.lib.java.loader.JavaTestLoadingUtils;
import unitee.annotations.Instances;
import unitee.interfaces.TestVariables;

public class JavaTestMethodsDefProcessor implements TestCreatorProcessor {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private JavaTestClassDefinition testClassDef = null;
	private TestDefProcessor classDefProcessor = null;
	
	public JavaTestMethodsDefProcessor(TestDefProcessor parentProcessor, JavaTestClassDefinition classDef) throws Exception{
		this.setContainer(classDef);
		this.classDefProcessor = parentProcessor;
	}
	
	public void processMetaData() throws Exception {
		Class<?> userTestClass = getTestClassDef().getUserTestClass();
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Loading method meta data for test class: %s", userTestClass.getName()));
		}
		
		for (String qualifiedName: testClassDef.getMethodDefQueueForDefProcessor()){
			this.process(
					testClassDef.getTestMethodDefinition(qualifiedName),
					userTestClass,
					testClassDef.getDataSourceMap()
			);
		}
	}
	
	private void process(JavaTestMethodDefinition methodDef, Class<?> userTestClass, Map<String,DataSourceType> methodDSMap) throws Exception{
		Method m =  methodDef.getMethod();
		String mName = m.getName();
		String mQualifiedName = methodDef.getQualifiedName();

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
			try{
				builder.process();
			} catch (Exception e){
				Console.displayError("!!!FATAL Error!!!");
				Console.displayError(String.format("Error in processing data driven annotation for test method [%s] in test class [%s].", m.getName(), userTestClass.getName()));
				Console.displayExceptionBlock(e);
				Console.displayError("Exiting...");
				System.exit(1);				
			}
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
		Map<Integer,HashMap<String,String>> instanceProps = new HashMap<Integer,HashMap<String,String>>();
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
			if (ArjunaInternal.displayExecVarProcessingInfo){
				logger.debug("User has supplied Exec Vars: " + hasUserSuppliedProperties);
			}
		}
		
		boolean testVarsAreMandatory = hasUserSuppliedProperties || methodDef.isDataRefPresent() || hasDataSourceAnn;
		this.populateExpectedSignature(m, methodDef, mQualifiedName, testVarsAreMandatory);
		instanceProps = JavaTestLoadingUtils.loadExecVarsFromInstancesAnnotation(instancesAnn, methodDef.getInstanceCount(), hasUserSuppliedProperties);	
		
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Adding instances. count=" + methodDef.getInstanceCount());
		}
		for (int i=1; i <= methodDef.getInstanceCount(); i++){
			methodDef.setExecVarsForInstance(i, instanceProps.get(i));
		}
		
		TestDefinitionsDB.getDependencyTreeBuilder().createNode(mQualifiedName, methodDef);	
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
		MethodSignatureType sigType = null;

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
				sigType = MethodSignatureType.SINGLEARG_TESTVARS;
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
				sigType = MethodSignatureType.NO_ARG;
			}
		}
		methodDef.setMethodSignatureType(sigType);
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Expected Test Signature Type: " + sigType);
			logger.debug("Expected Test Signature: " + expectedSigntureString);
		}
	}

}
