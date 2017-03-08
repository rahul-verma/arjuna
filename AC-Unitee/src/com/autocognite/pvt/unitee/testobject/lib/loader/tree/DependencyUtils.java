package com.autocognite.pvt.unitee.testobject.lib.loader.tree;

import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.annotations.ClassDependency;
import com.autocognite.arjuna.annotations.MethodDependency;
import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.utils.DataBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import com.autocognite.pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;

public class DependencyUtils {
	private static Logger logger = Logger.getLogger(RunConfig.getCentralLogName());

	public static Class<?>[] getDependencyClasses(String testObjectQualifiedName, ClassDependency depAnn) throws Exception{
		Class<?>[] depClasses = null;
		if (depAnn.testClasses().length == 0){
			if (depAnn.value().length == 0){
				logger.error(String.format("A dependency defined for %s is invalid.", testObjectQualifiedName));
				logger.error("Dependency Target Type: TEST_CLASSES");
				logger.error("Error: Provided empty \"testClasses\" attribute for @Dependency annotation");
				logger.error("Solution: Provide \"testClasses\" attribute for @Dependency annotation with a class array of length > 0");
				logger.error("Exiting...");
				System.exit(1);
			} else {
				depClasses = depAnn.value();
			}
		} else {
			depClasses = depAnn.testClasses();
		}
		
		return depClasses;
	}
	
	public static String[] getDependencyMethods(String testObjectQualifiedName,MethodDependency depAnn) throws Exception{
		String[] methodNames = null;
		if (depAnn.testMethods().length == 0){
			if (depAnn.value().length == 0){
				logger.error(String.format("A dependency defined for %s is invalid.", testObjectQualifiedName));
				logger.error("Dependency Target Type: TEST_METHODS");
				logger.error("Error: Provided empty test method names array for @MethodDependency annotation");
				logger.error("Solution: Provide either value or \"testMethods\" attribute for @MethodsDependency annotation with a string array of length > 0");
				logger.error("Exiting...");
				System.exit(1);
			} else {
				methodNames = depAnn.value();
			}
		} else {
			methodNames = depAnn.testMethods();
		}
		
		return methodNames;
	}
	
	public static JavaTestClassDefinition getClassDefForDependencyClass(String testObjectQualifiedName, Class<?> containerClass) throws Exception{
		String containerName = containerClass.getName();
		if (TestDefinitionsDB.hasClass(containerName)){
			if (TestDefinitionsDB.isTestClass(containerName)){
				if (TestDefinitionsDB.isTestClassMarkedAsSkipped(containerName)){
					logger.error(String.format("A dependency defined for %s would be ignored.", testObjectQualifiedName));
					logger.error(String.format("%s test class was skipped as per your filter configuration.", containerClass.getName()));
					return null;
				} else {
					return TestDefinitionsDB.getContainerDefinition(containerClass.getName());
				}
			} else {
				logger.error(String.format("A dependency defined for %s is invalid", testObjectQualifiedName));
				logger.error(String.format("%s is not a test class.", containerClass.getName()));
				logger.error("Exiting...");
				System.exit(1);	
			}
		} else {
			logger.error(String.format("No class with name %s found in the test directory", containerClass.getName()));
			logger.error("Classes in DB:");
			logger.error(DataBatteries.flatten(TestDefinitionsDB.getTestContainerNames()));
			logger.error(String.format("A dependency defined for %s would be ignored.", testObjectQualifiedName));
			return null;			
		}
		
		return null;
	}
	
	public static void validateDependencyMethodNames(String testObjectQualifiedName, JavaTestClassDefinition dependencyClassDef, List<String> dependencyMethodNames) throws Exception{
		String dependencyClassQualifiedName = dependencyClassDef.getQualifiedName();
		for(String dependencyMethodName: dependencyMethodNames){
			if (!dependencyClassDef.hasMethod(dependencyMethodName)){
				logger.error(String.format("Test Method dependency defined for %s is invalid", testObjectQualifiedName));
				logger.error(String.format("There is no method: %s in %s", dependencyMethodName, dependencyClassQualifiedName));
				logger.error("Exiting...");
				System.exit(1);	
			}
			
			if (!dependencyClassDef.isTestMethod(dependencyMethodName)){
				logger.error(String.format("Test Method dependency defined for %s is invalid", testObjectQualifiedName));
				logger.error(String.format("%s is not a test method in %s test class.", dependencyMethodName, dependencyClassQualifiedName));
				logger.error("Exiting...");
				System.exit(1);	
			}
			
			if (!dependencyClassDef.isTestMethodMarkedForSkipping(dependencyMethodName)){
				if (ArjunaInternal.logIgnoreDepInfo){
					logger.error(String.format("Test Method dependency defined for %s would be ignored.", testObjectQualifiedName));
					logger.error(String.format("Test method: %s in %s was skipped as per filter options.", dependencyMethodName, dependencyClassQualifiedName));
				}
			}		
		}
	}
}
