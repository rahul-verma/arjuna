package pvt.unitee.testobject.lib.java.processor;

import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.commons.io.FilenameUtils;
import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import arjunasdk.interfaces.Value;
import arjunasdk.sysauto.batteries.DataBatteries;
import pvt.batteries.config.Batteries;
import pvt.batteries.hocon.HoconReader;
import pvt.batteries.hocon.HoconResourceReader;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.java.JavaTestClass;
import pvt.unitee.testobject.lib.java.TestClassConstructorType;
import pvt.unitee.testobject.lib.java.loader.JavaTestClassFixturesLoader;
import pvt.unitee.testobject.lib.java.loader.JavaTestLoadingUtils;
import pvt.unitee.testobject.lib.loader.tree.DependencyTreeBuilder;
import unitee.annotations.Instances;
import unitee.interfaces.TestVariables;

public class JavaTestClassDefProcessor implements TestDefProcessor {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private ClassLoader classLoader = null;
	private DependencyTreeBuilder depTreeBuilder = new DependencyTreeBuilder();
	private List<Class<?>> testClasses = new ArrayList<Class<?>>();
	String testDir = null;
	
	private void emptyMethodBenchMark(){
		
	}
	
	@Override
	public void processMetaData() {
		if (ArjunaInternal.displayMetaDataProcessingInfo){
			logger.debug("Processing: " + TestDefinitionsDB.getClassDefQueueForDefProcessor());
		}
		for (String qualifiedName: TestDefinitionsDB.getClassDefQueueForDefProcessor()){
			this.load(TestDefinitionsDB.getContainerDefinition(qualifiedName));
		}
	}

	private void load(JavaTestClassDefinition classDef){
		if (ArjunaInternal.displayTestDefLoadingInfo){
			logger.debug("Processing: " + classDef.getQualifiedName());
		}
		JavaTestClass jTestClass = null;

		try {
			Class<?> userClass = classDef.getUserTestClass();
			
			JavaTestClassFixturesLoader fixtureLoader = classDef.getFixturesLoader();
			fixtureLoader.load();
			TestFixtures fixtures = fixtureLoader.build(); 
			classDef.setFixtures(fixtures);
			
			int creatorThreadCount = JavaTestLoadingUtils.getCreatorThreadCount(userClass);
			if (creatorThreadCount < 1){
				System.err.println(String.format("Method Thread count must be >=1. Correction needed for: %s", classDef.getQualifiedName()));
				System.err.println("Exiting...");
				System.exit(1);
			}
			classDef.setCreatorThreadCount(creatorThreadCount);
			
			// For Data ref processing
			classDef.setDataRefPresent(JavaTestLoadingUtils.isDataRefPresent(userClass));
			if (classDef.isDataRefPresent()){
				String dataRefName = JavaTestLoadingUtils.getDataRefName(userClass);
				String filePath = JavaTestLoadingUtils.getDataRefPath(userClass);
				if (dataRefName.equals("NOT_SET")){
					dataRefName = FilenameUtils.getBaseName(filePath).toUpperCase();
				}
				if (ArjunaInternal.displayDataMethodProcessingInfo){
					logger.debug(String.format("Now registering data reference with name %s.", dataRefName));
				}
				classDef.addFileDataRefWithPath(dataRefName, filePath);
			}

			boolean instancesAnnPresent = JavaTestLoadingUtils.isInstancesAnnotationPresent(userClass);
			Instances instancesAnn = null;
			boolean userHasSuppliedProperties = false;
			Map<Integer,HashMap<String,String>> instanceProps = new HashMap<Integer,HashMap<String,String>>();
			int instanceCount = 1;
			int instanceThreadCount = 1;
			if (instancesAnnPresent){
				if (ArjunaInternal.displayInstanceProcessingInfo){
					logger.debug("Found @Instances Annotation");
				}
				instancesAnn = (Instances) userClass.getAnnotation(Instances.class);
				instanceCount = JavaTestLoadingUtils.getInstancesCount(instancesAnn);
				if (instanceCount == -1){
					System.err.println(String.format("Instance count must be >=1. Correction needed for: %s", classDef.getQualifiedName()));
					System.err.println("Exiting...");
					System.exit(1);
				}
				
				instanceThreadCount = JavaTestLoadingUtils.getInstanceThreadCount(instancesAnn);
				if (instanceThreadCount == -1){
					System.err.println(String.format("Instance Thread count must be >=1. Correction needed for: %s", classDef.getQualifiedName()));
					System.err.println("Exiting...");
					System.exit(1);
				}
				userHasSuppliedProperties = JavaTestLoadingUtils.hasUserSuppliedProperties(classDef.getQualifiedName(), instancesAnn);
			}
			
			classDef.setInstanceCount(instanceCount);
			classDef.setInstanceThreadCount(instanceThreadCount);
			
			instanceProps = JavaTestLoadingUtils.loadExecVarsFromInstancesAnnotation(instancesAnn, classDef.getInstanceCount(), userHasSuppliedProperties);

			ConstructorDef constructorType = new ConstructorDef();
			Constructor<?> constructor = this.getConstructor(userClass, constructorType, userHasSuppliedProperties, classDef.isDataRefPresent());
			
			classDef.setConstructor(constructor);
			classDef.setConstructorType(constructorType.type);
			
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("Adding instances. count=" + classDef.getInstanceCount());
			}
//			logger.debug(classDef.getInstanceCount());
			for (int i=1; i <= classDef.getInstanceCount(); i++){
				classDef.setExecVarsForInstance(i, instanceProps.get(i));
			}
			
			TestCreatorProcessor creatorProcessor = new JavaTestMethodsDefProcessor(this, classDef);
			creatorProcessor.processMetaData();
		} catch (Throwable e) {
			Console.displayExceptionBlock(e);
		}
		
	}
	
	private List<Class<?>> getSuperClasses(Class<?> userClass) {
		  List<Class<?>> classList = new ArrayList<Class<?>>();
		  Class<?> superclass = userClass.getSuperclass();
		  classList.add(superclass);
		  while (superclass != null) {   
		    userClass = superclass;
		    superclass = userClass.getSuperclass();
		    if (superclass != null){
		    	classList.add(superclass);
		    }
		  }
		  return classList;
	}
	
	public Constructor<?> getConstructor(Class<?> klass, ConstructorDef constructorType, boolean userHasSuppliedProperties, boolean userHasSuppliedDataRef) throws Exception{
		
		Constructor<?>[] constructors = klass.getConstructors();
		if (constructors.length > 1){
			Console.displayError(String.format("Critical Error. Multiple constructors found for test class: %s",klass.getSimpleName()));
			System.err.println(String.format("You can define one and only one of the following public constructors for %s: ",klass.getSimpleName()));
			System.err.println(String.format("Option 1: public %s(TestVariables testClassVars)",klass.getSimpleName()));
			System.err.println(String.format("Option 2: public %s()",klass.getSimpleName()));
			System.err.println("Exiting...");
			System.exit(1);					
		}
		
		Constructor<?> constructor = constructors[0];
		
		Class<?>[] paramTypes = constructor.getParameterTypes();
		
		if (paramTypes.length == 0){
			constructor =  klass.getConstructor();
			constructorType.type = TestClassConstructorType.NO_ARG;
			return constructor;
		} else if ((paramTypes.length == 1) && (TestVariables.class.equals(paramTypes[0]))){
			constructor =  klass.getConstructor(TestVariables.class);
			constructorType.type = TestClassConstructorType.SINGLEARG_TESTVARS;
			return constructor;
		} else {
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
			
			Console.displayError(String.format("Critical Error. Incompatible constructor found for test class: %s",klass.getSimpleName()));
			Console.displayError(String.format("Your current constructor signature is: %s(%s)", klass.getSimpleName(), argString));
			System.err.println(String.format("You can define one and only one of the following public constructors for %s: ",klass.getSimpleName()));
			System.err.println(String.format("Option 1: public %s(TestVariables testClassVars)",klass.getSimpleName()));
			System.err.println(String.format("Option 2: public %s()",klass.getSimpleName()));
			System.err.println("Exiting...");
			System.exit(1);
		}
		
		return null;
			
	}

	@Override
	public void processDependencies() throws Exception {
		TestDefinitionsDB.processDependencies();
	}	
}

class ConstructorDef{
	 public TestClassConstructorType type = TestClassConstructorType.NO_ARG;
}

class EmptyBenchmarkClass{
	
	public EmptyBenchmarkClass(){
		super();
	}
	
}
