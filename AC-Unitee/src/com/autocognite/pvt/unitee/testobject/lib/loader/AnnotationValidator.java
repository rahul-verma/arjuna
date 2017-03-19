package com.autocognite.pvt.unitee.testobject.lib.loader;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.autocognite.pvt.batteries.console.Console;

public class AnnotationValidator {
	private static Set<String> namedFixtures = new HashSet<String>(Arrays.asList(
			"setUpClass",
			"setUpClassInstance",
			"setUpClassFragment",
			"setUpMethod",
			"setUpMethodInstance",
			"setUpTest",
			"tearDownClass",
			"tearDownClassInstance",
			"tearDownClassFragment",
			"tearDownMethod",
			"tearDownMethodInstance",
			"tearDownTest"
			));
	
	private static List<String> getAnnNames(Annotation[] annos){
		List<String> annNames = new ArrayList<String>();

		for(Annotation a : annos){
			if (a.annotationType().getName().startsWith("com.autocognite.arjuna")){
				annNames.add(a.annotationType().getSimpleName());
			}
		}
		
		return annNames;
	}
	
	private static void populateAnns(String mainAnn, List<String> annNames, Map<String,Set<String>> annRulesMap, List<String> incompatibles, List<String> ddtAnns, List<String> depAnns){
		for (String annName: annNames){
			if (!annRulesMap.get(mainAnn).contains(annName)){
				incompatibles.add(annName);					
			} 
			
			if (annRulesMap.containsKey("DDTAnnList")){
				if (annRulesMap.get("DDTAnnList").contains(annName)){
					ddtAnns.add(annName);
				}
			}
			
			if (annRulesMap.containsKey("DepAnnList")){
				if (annRulesMap.get("DepAnnList").contains(annName)){
					depAnns.add(annName);
				}
			}
		}
	}
	
	private static void displayErrorHeadingForAnnotatedMethod(String mainAnn, String testObjectName, String qualifiedName, boolean annAnomaly, boolean ddtAnomaly, boolean depAnomaly){
		if (annAnomaly || ddtAnomaly || depAnomaly){
			Console.displayError(String.format("There is a critical error with your %s: %s", testObjectName, qualifiedName));
			Console.displayError(String.format("Arjuna found that it is annotated with @%s.", mainAnn));						
		}		
	}
	
	private static void displayErrorHeadingForNamedTest(String testObjectName, String qualifiedName, boolean annAnomaly, boolean ddtAnomaly, boolean depAnomaly){
		if (annAnomaly || ddtAnomaly || depAnomaly){
			Console.displayError(String.format("There is a critical error with your %s: %s", testObjectName, qualifiedName));
			Console.displayError(String.format("Arjuna found that it is a test method using the reserved 'test' prefix."));						
		}		
	}
	
	private static void displayErrorHeadingForNamedFixture(String fixtureName, String testObjectName, String qualifiedName, boolean annAnomaly, boolean ddtAnomaly, boolean depAnomaly){
		if (annAnomaly || ddtAnomaly || depAnomaly){
			Console.displayError(String.format("There is a critical error with your %s: %s", testObjectName, qualifiedName));
			Console.displayError(String.format("Arjuna found that it is a named fixture using reserved name: %s.", fixtureName));						
		}		
	}
	
	private static void exitOnAnnotationAnomaly(String testObjectName, String qualifiedName, List<String> annNames, List<String> incompatibles, boolean annAnomaly){
		if (annAnomaly){
			Console.displayError(String.format("Along with this you have annotated the %s with: %s.", testObjectName, annNames.toString()));
			Console.displayError(String.format("Out of these, these annotations are incompatible: %s.", incompatibles.toString()));
			Console.displayError(String.format("Please correct the annotation usage."));
			Console.displayError("Exiting...");
			System.exit(1);		
		}		
	}
	
	private static void exitOnDDTAnnotationAnomaly(String testObjectName, String qualifiedName, List<String> annNames, List<String> ddtAnns, boolean ddtAnomaly){
		if (ddtAnomaly){
			Console.displayError(String.format("You have used more than one DDT annotation.", qualifiedName));
			Console.displayError(String.format("You can use only one of these: %s", ddtAnns.toString()));					
			Console.displayError(String.format("Please correct the annotation usage."));
			Console.displayError("Exiting...");
			System.exit(1);							
		}	
	}
	
	private static void exitOnDepAnnotationAnomaly(String testObjectName, String qualifiedName, List<String> annNames, List<String> depAnns, boolean depAnomaly){
		if (depAnomaly){
			Console.displayError(String.format("You have used more than one Dependency annotation.", qualifiedName));
			Console.displayError(String.format("You can use only one of these: %s", depAnns.toString()));					
			Console.displayError(String.format("Please correct the annotation usage."));
			Console.displayError("Exiting...");
			System.exit(1);							
		}	
	}
	
	private static void validateCompatibleAnns(String mainAnn, List<String> annNames, Map<String,Set<String>> annRulesMap, String testObjectName, String qualifiedName){
		List<String> incompatibles = new ArrayList<String>();
		List<String> ddtAnns = new ArrayList<String>();
		List<String> depAnns = new ArrayList<String>();
		boolean annAnomaly = false;
		boolean ddtAnomaly = false;
		boolean depAnomaly = false;
		populateAnns(mainAnn, annNames, annRulesMap, incompatibles, ddtAnns, depAnns);
		if (incompatibles.size() > 0){
			annAnomaly = true;
		}
		
		if (ddtAnns.size() > 0){
			ddtAnomaly = true;
		}
		
		if (depAnns.size() > 0){
			depAnomaly = true;
		}
		displayErrorHeadingForAnnotatedMethod(mainAnn, testObjectName, qualifiedName, annAnomaly, ddtAnomaly, depAnomaly);
		exitOnAnnotationAnomaly(testObjectName, qualifiedName, annNames, incompatibles, annAnomaly);
		exitOnDDTAnnotationAnomaly(testObjectName, qualifiedName, annNames, ddtAnns, ddtAnomaly);
		exitOnDepAnnotationAnomaly(testObjectName, qualifiedName, annNames, depAnns, depAnomaly);
	}
	
	private static void validateAnns(List<String> annNames, Map<String,Set<String>> annRulesMap, String testObjectName, String qualifiedName){
		// Check for compatible annotations usage.
		// Only applicable if more than one annotations exist for one method
		if (annNames.size() > 1){
			Collections.sort(annNames);
			String mainAnn = annNames.get(0);
			annNames.remove(0);
			if (!annRulesMap.containsKey(mainAnn)){
				Console.displayError(String.format("There is a critical error with your %s: %s", testObjectName, qualifiedName));
				Console.displayError(String.format("Arjuna found that it is annotated with @%s.", mainAnn));
				Console.displayError(String.format("Along with this you have annotated the %s with: %s.", testObjectName, annNames.toString()));
				Console.displayError(String.format("@%s annotation can not be used along with any other annotation.", mainAnn));
				Console.displayError(String.format("Please correct the annotation usage."));
				Console.displayError("Exiting...");
				System.exit(1);					
			} else {
				validateCompatibleAnns(mainAnn, annNames, annRulesMap, testObjectName, qualifiedName);
			}
		}				
	}
	
	public static boolean validateReservedNamedMethod(Method m, String qualifiedName){
		boolean isReserved = false;
		List<String> annNames = getAnnNames(m.getAnnotations());
		if (m.getName().startsWith("test")){
			isReserved = true;
		} else if (namedFixtures.contains(m.getName())){
			isReserved = true;
		}
		
		if (annNames.size() == 0){
			return isReserved;
		} else {
			Collections.sort(annNames);
		}
		
		List<String> incompatibles = new ArrayList<String>();
		List<String> ddtAnns = new ArrayList<String>();
		List<String> depAnns = new ArrayList<String>();
		boolean annAnomaly = false;
		boolean ddtAnomaly = false;
		boolean depAnomaly = false;
		String testObjectName = "method";
		if (m.getName().startsWith("test")){
			populateAnns("test", annNames, JavaTestClassDefinitionsLoader.METHOD_ANNOTATION_COMPAT, incompatibles, ddtAnns, depAnns);
			if (incompatibles.size() > 0){
				annAnomaly = true;
			}
			
			if (ddtAnns.size() > 0){
				ddtAnomaly = true;
			}
			
			
			if (depAnns.size() > 0){
				depAnomaly = true;
			}
			
			displayErrorHeadingForNamedTest(testObjectName, qualifiedName, annAnomaly, ddtAnomaly, depAnomaly);
			exitOnAnnotationAnomaly(testObjectName, qualifiedName, annNames, incompatibles, annAnomaly);
			exitOnDDTAnnotationAnomaly(testObjectName, qualifiedName, annNames, ddtAnns, ddtAnomaly);
			exitOnDepAnnotationAnomaly(testObjectName, qualifiedName, annNames, depAnns, depAnomaly);
		} else if (namedFixtures.contains(m.getName())){
			String fixtureName = m.getName();
			populateAnns(fixtureName, annNames, JavaTestClassDefinitionsLoader.METHOD_ANNOTATION_COMPAT, incompatibles, ddtAnns, depAnns);
			if (incompatibles.size() > 0){
				annAnomaly = true;
			}
			
			if (ddtAnns.size() > 0){
				ddtAnomaly = true;
			}
			
			
			if (depAnns.size() > 0){
				depAnomaly = true;
			}
			displayErrorHeadingForNamedFixture(fixtureName, testObjectName, qualifiedName, annAnomaly, ddtAnomaly, depAnomaly);
			exitOnAnnotationAnomaly(testObjectName, qualifiedName, annNames, incompatibles, annAnomaly);
			exitOnDDTAnnotationAnomaly(testObjectName, qualifiedName, annNames, ddtAnns, ddtAnomaly);
			exitOnDepAnnotationAnomaly(testObjectName, qualifiedName, annNames, depAnns, depAnomaly);
		}
		
		return isReserved;
	}
	
	public static void validateClassAnnotations(Class<?> klass, String qualifiedName){
		List<String> annNames = getAnnNames(klass.getAnnotations());
		validateAnns(annNames, JavaTestClassDefinitionsLoader.CLASS_ANNOTATION_COMPAT, "class", qualifiedName);
	}

	public static void validateMethodAnnotations(Method m, String qualifiedName){
		List<String> annNames = getAnnNames(m.getAnnotations());
		validateAnns(annNames, JavaTestClassDefinitionsLoader.METHOD_ANNOTATION_COMPAT, "method", qualifiedName);		
	}
}
