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

import pvt.arjunapro.ArjunaInternal;
import pvt.arjunapro.annotations.ClassDependency;
import pvt.arjunapro.annotations.MethodDependency;
import pvt.batteries.config.Batteries;
import pvt.unitee.core.lib.annotate.None;
import pvt.unitee.testobject.lib.loader.tree.DependencyTreeBuilder;
import pvt.unitee.testobject.lib.loader.tree.DependencyUtils;

public class TestDefinitionsDB {
	private static Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private static Map<String, JavaTestClassDefinition> classDefinitions = new HashMap<String, JavaTestClassDefinition>();
	private static Set<String> allClassNameSet = new HashSet<String>();
	private static Set<String> testClassNameSet =  new HashSet<String>();
	private static DependencyTreeBuilder depTreeBuilder = new DependencyTreeBuilder();
	private static List<String> allClassNameQueue = new ArrayList<String>();
	private static List<String> unscheduled = new ArrayList<String>();
	private static List<String> scheduled = new ArrayList<String>();

	public static synchronized JavaTestClassDefinition getClassTestVars(String fullClassName){
		return null;
	}

	public static void registerTestClassDefinition(String name, JavaTestClassDefinition classDef) {
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Registering class definition for: %s", name));
		}
		classDefinitions.put(name, classDef);
		allClassNameQueue.add(name);
		unscheduled.add(name);
		allClassNameSet.add(name);
		testClassNameSet.add(name);
	}
	
	public static synchronized List<String> getClassNameList(){
		return allClassNameQueue;
	}
	
	public static synchronized void markScheduled(String sessionName, List<String> containerNames) throws Exception{
		for (String cName: containerNames){
			JavaTestClassDefinition classDef = getContainerDefinition(cName);
			classDef.updateSessionInfo(sessionName);
		}
		unscheduled.removeAll(containerNames);
	}
	
	public static synchronized void markScheduledNonSkipped(String sessionName, List<String> containerNames) throws Exception{
		markScheduled(sessionName, containerNames);
		for (String name: containerNames){
			if (!scheduled.contains(name)){
				scheduled.add(name);
			}
		}
	}
	
	public static synchronized void removeAsSkipped(List<String> containerNames){
		allClassNameQueue.removeAll(containerNames);
	}
	
	public static synchronized List<String> getUnscheduledContainers(){
		return unscheduled;
	}
	
	public static synchronized List<String> getScheduledContainers(){
		return scheduled;
	}
	
	public static synchronized Set<String> getTestContainerNames(){
		return testClassNameSet;
	}

	public static synchronized JavaTestClassDefinition getContainerDefinition(String name) {
		if (ArjunaInternal.displayDefProcessingInfo){
			logger.debug(String.format("Fetching class definition for: %s", name));
		}
		return classDefinitions.get(name);
	}
	
	public static synchronized void validateDependencies() throws Exception{
		for (String name: classDefinitions.keySet()){
			processClassLevelDependencies(classDefinitions.get(name));
		}
		depTreeBuilder.processDependencies();
		depTreeBuilder.validate();
	}

	public static synchronized DependencyTreeBuilder getDependencyTreeBuilder() {
		return depTreeBuilder;
	}

	public static synchronized boolean isTestClass(String name) {
		return TestDefinitionsDB.testClassNameSet.contains(name);
	}
	
	public static synchronized boolean isTestClassMarkedAsSkipped(String name) throws Exception {
		if (!isTestClass(name)){
			throw new Exception("Not a test class.");
		} else {
			return classDefinitions.get(name).shouldBeSkipped();
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
					logger.error("Error: Did not provide \"containerClass\" attribute for @Dependency annotation on Test Class.");
					logger.error("Solution: Provide \"containerClass\" attribute for @Dependency annotation to tell about the test class, that contains the dependency methods.");
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

}
