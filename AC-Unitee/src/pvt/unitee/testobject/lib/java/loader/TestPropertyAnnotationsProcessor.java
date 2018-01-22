package pvt.unitee.testobject.lib.java.loader;

import java.lang.annotation.Annotation;
import java.util.List;
import java.util.Map;

import arjunasdk.interfaces.Value;
import arjunasdk.sysauto.batteries.DataBatteries;
import pvt.unitee.core.lib.testvars.InternalTestVariables;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import unitee.annotations.TestClass;
import unitee.annotations.TestMethod;
import unitee.enums.TestAttribute;
import unitee.interfaces.TestProperties;

public class TestPropertyAnnotationsProcessor {

	public static void populateTestProps(JavaTestClassDefinition classDef, InternalTestVariables testVars) throws Exception {
		if (classDef.getUserTestClass().isAnnotationPresent(TestClass.class)){
			Annotation annotation = classDef.getUserTestClass().getAnnotation(TestClass.class);
			TestClass testProps = (TestClass) annotation;
			setAnnotatedProperties(classDef, testVars, testProps);
		
			if (testVars.test().priority() < 1){
				System.err.println(String.format("You must provide prioriy >=1. Correction needed for: %s", classDef.getQualifiedName()));
				System.err.println("Exiting...");
				System.exit(1);
			}
		}
	}
	
	public static void populateTestProps(JavaTestClassDefinition classDef, JavaTestMethodDefinition methodDef, InternalTestVariables testVars) throws Exception {
		if (methodDef.getMethod().isAnnotationPresent(TestMethod.class)){
			Annotation annotation = methodDef.getMethod().getAnnotation(TestMethod.class);
			TestMethod testProps = (TestMethod) annotation;
			setAnnotatedProperties(classDef, testVars, testProps);
		}
	}
	
	private static void setId(InternalTestVariables testVars, String id) throws Exception{
		if (!id.equals("NOT_SET")){
			testVars.rawTestProps().setId(id);
		}
	}
	
	private static void setName(InternalTestVariables testVars, String name) throws Exception{
		if (!name.equals("NOT_SET")){
			testVars.rawTestProps().setName(name);
		}
	}
	
	private static void setIdea(InternalTestVariables testVars, String idea) throws Exception{
		if (!idea.equals("NOT_SET")){
			testVars.rawTestProps().setIdea(idea);
		}
	}
	
//	private static void setPriority(InternalTestVariables testVars, int priority) throws Exception{
//		if (priority >= 1){
//			testVars.rawTestProps().setPriority(priority);
//		} else if ((priority < 1) && (priority != -51111)){
//			System.err.println(String.format("Provided priority: %d", priority));
//			System.err.println(String.format("You must provide prioriy >=1. Correction needed for: %s", testVars.object().qualifiedName()));
//			System.err.println("Exiting...");
//			System.exit(1);
//		}
//	}
	
	private static void setAnnotatedProperties(JavaTestClassDefinition classDef, InternalTestVariables testVars, TestClass testProps) throws Exception{
		if (testProps.id().equals("NOT_SET")){
			setId(testVars, testVars.object().qualifiedName());
		} else {
			setId(testVars, testProps.id());
		}
		
		if (testProps.name().equals("NOT_SET")){
			setName(testVars, testVars.object().qualifiedName());
		} else {
			setName(testVars, testProps.name());
		}
		
		if (testProps.idea().equals("NOT_SET")){
			setIdea(testVars, testVars.object().qualifiedName());
		} else {
			setIdea(testVars, testProps.idea());
		}
		
		System.out.println(testProps.priority() );
		if (testProps.priority() == -51111){
			testVars.rawTestProps().setPriority(10);
		} else {
			if ((testProps.priority() < 1) || (testProps.priority() > 10)){
				System.err.println(String.format("You have annotated %s test class with priority: %d", classDef.getQualifiedName(), testProps.priority()));
				System.err.println(String.format("You must provide prioriy in the range of 1-10, 1 being the highest. Correct it and try again."));
				System.err.println("Exiting...");
				System.exit(1);				
			} else {
				testVars.rawTestProps().setPriority(testProps.priority());
			}
		}

		setTestAttr(testVars, testProps.attr());
	}
	
	private static void setAnnotatedProperties(JavaTestClassDefinition classDef, InternalTestVariables testVars, TestMethod testProps) throws Exception{
		TestProperties classTestProps = classDef.getTestVariables().test();

		if (testProps.id().equals("NOT_SET")){
			setId(testVars, classTestProps.id() + "::" + testVars.object().name());
		} else {
			setId(testVars, classTestProps.id() + "::" + testProps.id());
		}

		if (testProps.name().equals("NOT_SET")){
			setName(testVars, classTestProps.name() + "::" + testVars.object().name());
		} else {
			setName(testVars, classTestProps.name() + "::" + testProps.name());
		}
		
		if (testProps.idea().equals("NOT_SET")){
			setIdea(testVars, classTestProps.idea() + "::" + testVars.object().name());
		} else {
			setIdea(testVars, classTestProps.idea() + "::" + testProps.idea());
		}
		
		if (testProps.priority() == -51111){
			testVars.rawTestProps().setPriority(classTestProps.priority());
		} else {
			if ((testProps.priority() < 1) || (testProps.priority() > 10)){
				System.err.println(String.format("You have annotated %s test method with priority: %d", classDef.getQualifiedName() + "." + testVars.object().name(), testProps.priority()));
				System.err.println(String.format("You must provide prioriy in the range of 1-10, 1 being the highest. Correct it and try again."));
				System.err.println("Exiting...");
				System.exit(1);				
			} else if (testProps.priority() > classTestProps.priority()){
				System.err.println(String.format("You have annotated %s test method with priority: %d", classDef.getQualifiedName() + "." + testVars.object().name(), testProps.priority()));
				System.err.println(String.format("Test Class %s has been annotated with priority: %d", classDef.getQualifiedName(), classTestProps.priority()));
				System.err.println(String.format("Test Method priority number should be same or less than that of Test Class. Correct and try again."));
				System.err.println("Exiting...");
				System.exit(1);
			} else {
				testVars.rawTestProps().setPriority(testProps.priority());
			}
		}

		setTestAttr(testVars, testProps.attr());
	}
	
	private static void setTestAttr(InternalTestVariables testVars, String[] testAttr) throws Exception{
		for (String kv: testAttr){
			List<String> pKV = DataBatteries.split(kv, "=");
			String propName = pKV.get(0);
			String propValue = pKV.get(1);
			testVars.attr().add(propName, propValue);
		}		
	}
}
