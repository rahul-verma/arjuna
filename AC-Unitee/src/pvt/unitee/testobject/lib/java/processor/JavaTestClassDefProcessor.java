package pvt.unitee.testobject.lib.java.processor;

import java.io.File;
import java.lang.reflect.Constructor;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.bcel.Repository;
import org.apache.bcel.classfile.Code;
import org.apache.bcel.classfile.JavaClass;
import org.apache.commons.io.FilenameUtils;
import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import arjunasdk.interfaces.Value;
import arjunasdk.sysauto.batteries.DataBatteries;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtConstructor;
import javassist.CtNewConstructor;
import pvt.batteries.config.Batteries;
import pvt.batteries.discoverer.DiscoveredFile;
import pvt.batteries.discoverer.DiscoveredFileAttribute;
import pvt.batteries.hocon.HoconReader;
import pvt.batteries.hocon.HoconResourceReader;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.SkipCode;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import pvt.unitee.testobject.lib.java.JavaTestClass;
import pvt.unitee.testobject.lib.java.TestClassConstructorType;
import pvt.unitee.testobject.lib.java.loader.JavaTestLoadingUtils;
import pvt.unitee.testobject.lib.java.loader.TestCreatorLoader;
import pvt.unitee.testobject.lib.loader.tree.DependencyTreeBuilder;
import unitee.annotations.Instances;
import unitee.annotations.Skip;
import unitee.annotations.TestClass;

public class JavaTestClassDefProcessor implements TestDefProcessor {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private ClassLoader classLoader = null;
	private DependencyTreeBuilder depTreeBuilder = new DependencyTreeBuilder();
	private List<Class<?>> testClasses = new ArrayList<Class<?>>();
	String testDir = null;
	public static Map<String, Set<String>> CLASS_ANNOTATION_COMPAT = new HashMap<String,Set<String>>();
	public static Map<String, Set<String>> METHOD_ANNOTATION_COMPAT = new HashMap<String,Set<String>>();
	byte[] emptyCodeCheck = null;
	
	private void emptyMethodBenchMark(){
		
	}
	
	public JavaTestClassDefProcessor() throws Exception{
		// Empty method processor
		JavaClass emptyKlass =  Repository.lookupClass(EmptyBenchmarkClass.class);
		org.apache.bcel.classfile.Method[]  jMethods = emptyKlass.getMethods();
		for (org.apache.bcel.classfile.Method jMethod: jMethods){
			if (jMethod.getName().equals("<init>")){
				emptyCodeCheck = jMethod.getCode().getCode();
			}
		}
		
		HoconReader reader1 = new HoconResourceReader(this.getClass().getResourceAsStream("/com/autocognite/pvt/text/class_annotations_compatibility.conf"));
		reader1.process();
		Map<String, Value> rules1 = reader1.getProperties();
		for (String r: rules1.keySet()){
			Set<String> aSet = new HashSet<String>();
			aSet.addAll(rules1.get(r).asStringList());
			CLASS_ANNOTATION_COMPAT.put(r, aSet);
		}
		
		HoconReader reader2 = new HoconResourceReader(this.getClass().getResourceAsStream("/com/autocognite/pvt/text/method_annotations_compatibility.conf"));
		reader2.process();
		Map<String, Value> rules2 = reader2.getProperties();
		for (String r: rules2.keySet()){
			Set<String> aSet = new HashSet<String>();
			aSet.addAll(rules2.get(r).asStringList());
			METHOD_ANNOTATION_COMPAT.put(r, aSet);
		}
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
			HashMap<Integer,HashMap<String,String>> instanceProps = new HashMap<Integer,HashMap<String,String>>();
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
	
	private Constructor<?> getConstructor(Class<?> userClass, ConstructorDef constructorType, boolean userHasSuppliedProperties, boolean userHasSuppliedDataRef) throws Exception{
		boolean constDefFound = false;

		List<Class<?>> jClasses =  new ArrayList<Class<?>>();
		jClasses.add(userClass);
		System.out.println(this.getSuperClasses(userClass));
		for (Class<?> parent: this.getSuperClasses(userClass)){
			System.out.println(parent.getName());
			if(parent.getName().equals("java.lang.Object")){
				continue;
			}
			jClasses.add(parent);
		}
		
		for (Class<?> jClass: jClasses){
			System.out.println(jClass.getName());
			Constructor<?>[]  constructors = jClass.getDeclaredConstructors();
			System.out.println(Arrays.toString(constructors));
			if (constructors.length > 1){
				constDefFound = true;
				break;
			} else if (constructors[0].getParameterTypes().length > 0){
				constDefFound = true;	
				break;
			}
		}
		
		if (constDefFound){
			Console.displayError(String.format("Critical Error. Constructor definition found for test class: %s",userClass.getSimpleName()));
			Console.displayError(String.format("Arjuna Test classes or their base classes should not define any constructor."));
			Console.displayError(String.format("Please remove any constructors from %s and its base classes, if any.", userClass.getSimpleName()));
			Console.displayError(String.format("Modify your logic to use an appropriate set-up fixture provisioned by Arjuna Test classes."));
			Console.displayError("Exiting...");
			System.exit(1);	
		}
		
		constructorType.type = TestClassConstructorType.NO_ARG;
		
		return userClass.getConstructor();
			
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
