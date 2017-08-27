package pvt.unitee.testobject.lib.definitions;

import java.lang.annotation.Annotation;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.log4j.Logger;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.core.lib.annotate.None;
import pvt.unitee.enums.SkipCode;
import pvt.unitee.enums.UnpickedCode;
import pvt.unitee.testobject.lib.loader.tree.DependencyTreeBuilder;
import pvt.unitee.testobject.lib.loader.tree.DependencyUtils;
import unitee.annotations.ClassDependency;
import unitee.annotations.MethodDependency;

public class TestDefinitionsDB {
	private static Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private static DependencyTreeBuilder depTreeBuilder = new DependencyTreeBuilder();
	
	// For checking whether a class name exists in the current project
	private static Set<String> allClassNameSet = new HashSet<String>();
	// For pulling out class definitions by name
	private static Map<String, JavaTestClassDefinition> testClassDefinitions = new HashMap<String, JavaTestClassDefinition>();
	private static List<String> discoveredQueue = new ArrayList<String>();
	// This is what would be got by groups for pickers processing. If a group picks up something, it calls setPicked()
	private static List<String> forPickerProcessing = new ArrayList<String>();
	// The following gets populated from above, if classDef.isNotPickedByAnyGroup() is True
	private static List<String> forProcessor = new ArrayList<String>();

	public static synchronized JavaTestClassDefinition getClassTestVars(String fullClassName){
		return null;
	}

	public static void registerTestClassDefinition(String name, JavaTestClassDefinition classDef) {
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Registering class definition for: %s", name));
		}
		allClassNameSet.add(name);
		testClassDefinitions.put(name, classDef);
		discoveredQueue.add(name);
	}

	public static synchronized void buildPickerQueueFromDiscoveredQueue() throws Exception{
		for (String name: discoveredQueue){
			JavaTestClassDefinition classDef = testClassDefinitions.get(name);
			if (!classDef.shouldBeSkipped()){
				forPickerProcessing.add(name);
			} else {
				classDef.setSkipCode(SkipCode.SKIPPED_CLASS_ANNOTATION);
			}
			
			classDef.buildPickerQueueFromDiscoveredQueue();
		}
	}
	
	public static synchronized List<String> getClassDefQueueForDefPickerProcessing(){
		return forPickerProcessing;
	}
	
	public static synchronized void buildProcessorQueueFromPickerQueue() throws Exception{
		for (String name: forPickerProcessing){
			JavaTestClassDefinition classDef = testClassDefinitions.get(name);
			if (classDef.isPicked()){
				forProcessor.add(name);
			} else {
				classDef.setUnpicked(UnpickedCode.UNPICKED_CLASS);
			}
			
			classDef.buildProcessorQueueFromPickerQueue();
		}
	}
	
	public static synchronized List<String> getClassDefQueueForDefProcessor(){
		return forProcessor;
	}

	public static synchronized JavaTestClassDefinition getContainerDefinition(String name) {
		if (ArjunaInternal.displayDefProcessingInfo){
			logger.debug(String.format("Fetching class definition for: %s", name));
		}
		return testClassDefinitions.get(name);
	}
	
	public static synchronized void processDependencies() throws Exception{
		for (String name: testClassDefinitions.keySet()){
			processClassLevelDependencies(testClassDefinitions.get(name));
		}
		depTreeBuilder.processDependencies();
		depTreeBuilder.validate();
	}

	public static synchronized DependencyTreeBuilder getDependencyTreeBuilder() {
		return depTreeBuilder;
	}

	public static synchronized boolean isTestClass(String name) {
		return TestDefinitionsDB.testClassDefinitions.containsKey(name);
	}
	
	public static synchronized boolean isTestClassMarkedAsSkipped(String name) throws Exception {
		if (!isTestClass(name)){
			throw new Exception("Not a test class.");
		} else {
			return testClassDefinitions.get(name).shouldBeSkipped();
		}
	}
	
	public static synchronized boolean hasClass(String name) {
		return allClassNameSet.contains(name);
	}
	
	public static synchronized void addNonTestClassName(String name) {
		allClassNameSet.add(name);
	}
	
	public static synchronized void processClassLevelDependencies(JavaTestClassDefinition classDef) throws Exception{
		Class<?> userTestClass = classDef.getUserTestClass();
		String containerQualifiedName = classDef.getQualifiedName();

		if (userTestClass.isAnnotationPresent(MethodDependency.class)){
			Annotation annotation = userTestClass.getAnnotation(MethodDependency.class);
			MethodDependency depAnn = (MethodDependency) annotation;
			List<String> processedDepMethodNames =  new ArrayList<String>();
			List<String> depMethodNames = Arrays.asList(DependencyUtils.getDependencyMethods(classDef.getQualifiedName(), depAnn));
			if (ArjunaInternal.displayDependencyDefInfo){
				logger.debug(String.format("Found dependencies for %s: %s", classDef.getQualifiedName(), depMethodNames));
			}

			if (depMethodNames.size() > 0){
				
				Class<?> containerClass = depAnn.containerClass();
				JavaTestClassDefinition depClassDef = null;
				if (containerClass == None.class){
					logger.error(String.format("A dependency defined for %s is invalid.", classDef.getQualifiedName()));
					logger.error("Dependency Target Type: TEST_METHODS");
					logger.error("Error: Did not provide \"containerClass\" attribute for @MethodDependency annotation on Test Class.");
					logger.error("Solution: Provide \"containerClass\" attribute for @MethodDependency annotation to tell about the test class, that contains the dependency methods.");
					logger.error("Exiting...");
					System.exit(1);
				} else {
					depClassDef = DependencyUtils.getClassDefForDependencyClass(classDef.getQualifiedName(), containerClass);
				}
				
				if (depClassDef == null){
					return;
				}
				
				DependencyUtils.validateDependencyMethodNames(classDef.getQualifiedName(), depClassDef, depMethodNames);

				for (String dependencyMethodName: depMethodNames){
					processedDepMethodNames.add(depClassDef.getQualifiedName() + "." + dependencyMethodName);
				}
			}
			
			if (processedDepMethodNames != null){
				if (ArjunaInternal.displayDependencyDefInfo){
					logger.debug("Adding dependencies to Method Definition : " + processedDepMethodNames);
				}
				classDef.addDependencyMethodNames(processedDepMethodNames);
			}
		}

		if (userTestClass.isAnnotationPresent(ClassDependency.class)){
			Annotation annotation = userTestClass.getAnnotation(ClassDependency.class);
			ClassDependency depAnn = (ClassDependency) annotation;
			List<String> processedClassDeps = new ArrayList<String>();
			List<Class<?>> depClasses = Arrays.asList(DependencyUtils.getDependencyClasses(classDef.getQualifiedName(), depAnn));
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug(String.format("Found class dependencies type annotation for %s: %s.", classDef.getQualifiedName(), depClasses));
			}
			
			for (Class<?> dependencyClass: depClasses){
				JavaTestClassDefinition depClassDef = DependencyUtils.getClassDefForDependencyClass(containerQualifiedName, dependencyClass);
				if (depClassDef == null){
					continue;
				}
				processedClassDeps.add(dependencyClass.getName());
			}
			
			if (processedClassDeps.size() != 0){
				if (ArjunaInternal.displayDependencyDefInfo){
					logger.debug("Adding Class dependencies to Class Definition : " + processedClassDeps);
				}
				classDef.addDependencyClassNames(processedClassDeps);
			}
		}
		
		if (ArjunaInternal.displayDependencyDefInfo){
			logger.debug("Deps processed.");
		}
	}

	public static Set<String> getAllProjectClassNames() {
		return allClassNameSet;
	}

}
