package pvt.unitee.testobject.lib.loader;

import java.io.File;
import java.lang.reflect.Constructor;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
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
import pvt.arjunapro.ArjunaInternal;
import pvt.arjunapro.annotations.Instances;
import pvt.batteries.config.Batteries;
import pvt.batteries.discoverer.DiscoveredFile;
import pvt.batteries.discoverer.DiscoveredFileAttribute;
import pvt.batteries.hocon.HoconReader;
import pvt.batteries.hocon.HoconResourceReader;
import pvt.unitee.enums.SkipCode;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import pvt.unitee.testobject.lib.java.JavaTestClass;
import pvt.unitee.testobject.lib.java.TestClassConstructorType;
import pvt.unitee.testobject.lib.loader.tree.DependencyTreeBuilder;
import unitee.annotations.Skip;
import unitee.annotations.TestClass;

public class JavaTestClassDefinitionsLoader implements TestDefinitionsLoader {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private ClassLoader classLoader = null;
	private DependencyTreeBuilder depTreeBuilder = new DependencyTreeBuilder();
	String testDir = null;
	public static Map<String, Set<String>> CLASS_ANNOTATION_COMPAT = new HashMap<String,Set<String>>();
	public static Map<String, Set<String>> METHOD_ANNOTATION_COMPAT = new HashMap<String,Set<String>>();
	
	public JavaTestClassDefinitionsLoader() throws Exception{
		HoconReader reader1 = new HoconResourceReader(this.getClass().getResourceAsStream("/com/arjunapro/pvt/text/class_annotations_compatibility.conf"));
		reader1.process();
		Map<String, Value> rules1 = reader1.getProperties();
		for (String r: rules1.keySet()){
			Set<String> aSet = new HashSet<String>();
			aSet.addAll(rules1.get(r).asStringList());
			CLASS_ANNOTATION_COMPAT.put(r, aSet);
		}
		
		HoconReader reader2 = new HoconResourceReader(this.getClass().getResourceAsStream("/com/arjunapro/pvt/text/method_annotations_compatibility.conf"));
		reader2.process();
		Map<String, Value> rules2 = reader2.getProperties();
		for (String r: rules2.keySet()){
			Set<String> aSet = new HashSet<String>();
			aSet.addAll(rules2.get(r).asStringList());
			METHOD_ANNOTATION_COMPAT.put(r, aSet);
		}
	}
	
	@Override
	public void setTestDir(String testDir) throws Exception{
		this.testDir = testDir;	
	}
	
	private ClassLoader getClassLoader(DiscoveredFile f) throws MalformedURLException{
		if (ArjunaInternal.displayUserTestLoadingInfo){
			logger.debug("Get Class Loader for: " + f.getAttribute(DiscoveredFileAttribute.FULL_NAME));
		}
		String path = null;
		if (f.getAttribute(DiscoveredFileAttribute.CONTAINER_TYPE).toLowerCase().equals("jar")){
			path = String.format(
					"%s/%s", f.getAttribute(DiscoveredFileAttribute.DIRECTORY_ABSOLUTE_PATH), 
					f.getAttribute(DiscoveredFileAttribute.CONTAINER));
		} else {
			path =  testDir;
		}
		
		if (ArjunaInternal.displayUserTestLoadingInfo){
			logger.debug("Loading Path: " + path);
		}
		
		URL[] urls = new URL[] {new File(path).toURI().toURL()};
		// Create a new class loader with the directory
		 classLoader = new URLClassLoader(urls); //, this.getClass().getClassLoader());	
		 return classLoader;
	}
	
	
	private ClassLoader getClassLoader(String relPath) throws MalformedURLException{
		String path = this.testDir + relPath;
		
		URL[] urls = new URL[] {new File(path).toURI().toURL()};
		// Create a new class loader with the directory
		 classLoader = new URLClassLoader(urls); //, this.getClass().getClassLoader());	
		 return classLoader;
	}
	
	@Override
	public void load(DiscoveredFile f){
		JavaTestClass jTestClass = null;
		String qualifiedName = getQualifiedName(f);
		if (ArjunaInternal.displayUserTestLoadingInfo){
			logger.debug("Get Class Loader for: " + qualifiedName);
		}

		try {
			//boolean include = JavaObjectFilter.shouldIncludeClass(cls);
//							logger.debug("Filtering: " + fullQualifiedClassName);
			Class<?> klass = this.loadClass(f, qualifiedName);
			
			boolean isReserved = false;
			isReserved = AnnotationValidator.validateReservedNamedClass(klass, qualifiedName);
			if (!isReserved){
				AnnotationValidator.validateClassAnnotations(klass, qualifiedName);
			}
			
			if (!this.isTestClass(klass)) {
				ArjunaInternal.processNonTestClass(klass);
				TestDefinitionsDB.addNonTestClassName(klass.getName());
				return;				
			}
			
			JavaTestClassDefinition classDef = new JavaTestClassDefinition();
			classDef.setUserTestClass(klass);
			
			// Filter early for better performance, no further processing
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("Process selection: " + qualifiedName);
			}
			processSkip(klass.getName(), klass, classDef);
			
			int creatorThreadCount = JavaTestLoadingUtils.getCreatorThreadCount(klass);
			if (creatorThreadCount < 1){
				System.err.println(String.format("Method Thread count must be >=1. Correction needed for: %s", classDef.getQualifiedName()));
				System.err.println("Exiting...");
				System.exit(1);
			}
			classDef.setCreatorThreadCount(creatorThreadCount);
			
			// For Data ref processing
			classDef.setDataRefPresent(JavaTestLoadingUtils.isDataRefPresent(klass));
			if (classDef.isDataRefPresent()){
				String dataRefName = JavaTestLoadingUtils.getDataRefName(klass);
				String filePath = JavaTestLoadingUtils.getDataRefPath(klass);
				if (dataRefName.equals("NOT_SET")){
					dataRefName = FilenameUtils.getBaseName(filePath).toUpperCase();
				}
				if (ArjunaInternal.displayDataMethodProcessingInfo){
					logger.debug(String.format("Now registering data reference with name %s.", dataRefName));
				}
				classDef.addFileDataRefWithPath(dataRefName, filePath);
			}

			boolean instancesAnnPresent = JavaTestLoadingUtils.isInstancesAnnotationPresent(klass);
			Instances instancesAnn = null;
			boolean userHasSuppliedProperties = false;
			HashMap<Integer,HashMap<String,String>> instanceProps = new HashMap<Integer,HashMap<String,String>>();
			int instanceCount = 1;
			int instanceThreadCount = 1;
			if (instancesAnnPresent){
				if (ArjunaInternal.displayInstanceProcessingInfo){
					logger.debug("Found @Instances Annotation");
				}
				instancesAnn = (Instances) klass.getAnnotation(Instances.class);
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
				userHasSuppliedProperties = JavaTestLoadingUtils.hasUserSuppliedProperties(qualifiedName, instancesAnn);
			}
			
			classDef.setInstanceCount(instanceCount);
			classDef.setInstanceThreadCount(instanceThreadCount);
			
			instanceProps = JavaTestLoadingUtils.loadUTVFromInstancesAnnotation(instancesAnn, classDef.getInstanceCount(), userHasSuppliedProperties);

			ConstructorDef constructorType = new ConstructorDef();
			Constructor<?> constructor = this.getConstructor(klass, constructorType, userHasSuppliedProperties, classDef.isDataRefPresent());
			
			classDef.setConstructor(constructor);
			classDef.setConstructorType(constructorType.type);
			
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("Adding instances. count=" + classDef.getInstanceCount());
			}
//			logger.debug(classDef.getInstanceCount());
			for (int i=1; i <= classDef.getInstanceCount(); i++){
				classDef.setUtvForInstance(i, instanceProps.get(i));
			}
			
			TestCreatorLoader creatorLoader = new JavaTestMethodsDefinitionLoader(this, classDef);
			creatorLoader.loadDefinitions();
			
			TestDefinitionsDB.registerTestClassDefinition(klass.getName(), classDef);
		} catch (Throwable e) {
			Console.displayExceptionBlock(e);
		}
		
	}
	
	private String getQualifiedName(DiscoveredFile f){
		String fullQualifiedClassName = null;
		if (f.getAttribute(DiscoveredFileAttribute.PACKAGE_DOT_NOTATION).equals("")){
			fullQualifiedClassName = f.getAttribute(DiscoveredFileAttribute.NAME);
		} else {
			fullQualifiedClassName = f.getAttribute(DiscoveredFileAttribute.PACKAGE_DOT_NOTATION)
					+ "."
					+ f.getAttribute(DiscoveredFileAttribute.NAME);				
		}
		return fullQualifiedClassName;
	}
	
//	private Class<?> loadClass(String fullName) throws Exception{
//		return classLoader.loadClass(fullName);
//	}

	private Class<?> loadClass(DiscoveredFile f, String fullName) throws Exception{
		try {
			if (ArjunaInternal.displayUserTestLoadingInfo){
				logger.debug("Try default loading");
			}
			return this.getClassLoader(f).loadClass(fullName);
		} catch (Throwable e){
			if (f.getAttribute(DiscoveredFileAttribute.CONTAINER_TYPE).toLowerCase().equals("jar")){
				throw e;
			}
//			logger.debug(fullName);
			List<String> parts = DataBatteries.split(fullName, "\\.");
			int i = 0;
			Class<?> klass = null;
			while (i < parts.size()){
				List<String> temp = parts.subList(i, parts.size());
				List<String> temp2 = null;
				if (i == 0){
					temp2 = new ArrayList<String>();
				} else {
					temp2 = parts.subList(0, i);
				}
//				logger.debug(temp);
				if (temp.size() == 1){
					klass = getClassLoader("/" + DataBatteries.join(temp2, "/")).loadClass(temp.get(0));
//					logger.debug(klass);
					return klass;
				}
				String pkg = DataBatteries.join(temp, ".");
//				logger.debug(pkg);
				
				try{
					klass = getClassLoader("/" + DataBatteries.join(temp2, "/")).loadClass(pkg);
//					logger.debug(klass);
					return klass;
				} catch (Throwable h){
//					logger.debug(e.getMessage());
//					logger.debug(e.getMessage());
				}
				
				i++;
			}
		}
		
		throw new Exception("Not able to load test class: " + fullName);
}
	private boolean isTestClass(Class<?> klass){
		return klass.isAnnotationPresent(TestClass.class) || klass.getSimpleName().startsWith("Test");
	}
	
	private void processSkip(String fullName, Class<?> klass, JavaTestClassDefinition classDef) throws Exception{
		if (klass.isAnnotationPresent(Skip.class)){
			classDef.setSkipped(SkipCode.SKIPPED_CLASS_ANNOTATION);
		}
	}
	
	public Constructor<?> getConstructor(Class<?> klass, ConstructorDef constructorType, boolean userHasSuppliedProperties, boolean userHasSuppliedDataRef) throws Exception{
		Constructor<?>[] constructors = klass.getConstructors();
		if ((constructors.length > 1) || (constructors[0].getParameterTypes().length > 0)){
			Console.displayError(String.format("Critical Error. Non-default constructor found for test class: %s",klass.getSimpleName()));
			Console.displayError(String.format("Arjuna Test classes can only use default public constructor."));
			Console.displayError(String.format("Change constructor to:"));
			Console.displayError(String.format("public %s()",klass.getSimpleName()));
			Console.displayError("Exiting...");
			System.exit(1);				
		}
		
		constructorType.type = TestClassConstructorType.NO_ARG;
		
		return klass.getConstructor();
			
	}

	@Override
	public void validateDependencies() throws Exception {
		TestDefinitionsDB.validateDependencies();
	}
	
}

class ConstructorDef{
	 public TestClassConstructorType type = TestClassConstructorType.NO_ARG;
}
