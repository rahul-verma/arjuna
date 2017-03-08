package com.autocognite.pvt.unitee.testobject.lib.loader;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

import com.autocognite.arjuna.annotations.FileDataReference;
import com.autocognite.arjuna.annotations.Instances;
import com.autocognite.arjuna.annotations.TestClass;
import com.autocognite.arjuna.annotations.TestMethod;
import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.utils.DataBatteries;
import com.autocognite.arjuna.utils.FileSystemBatteries;
import com.autocognite.pvt.batteries.enums.BatteriesPropertyType;

public class JavaTestLoadingUtils {
	private static String[] checkArray = new String[] {"NOT_SET"};
	
	private static String getDataRefPath(FileDataReference dataRefAnn) throws Exception{
		String refPath = null;

		if (dataRefAnn.path().equals("NOT_SET")){
			if (dataRefAnn.value().equals("NOT_SET")){
				throw new Exception("Used @FileDataReference annotation by providing neither path nor value attribute.");
			} else {
				refPath = dataRefAnn.value();
			}
		} else {
			refPath = dataRefAnn.path();
		}

		if (!FileSystemBatteries.isFile(refPath)){
			String relRefPath = RunConfig.value(BatteriesPropertyType.DIRECTORY_DATA_REFERENCES).asString() + "/" + refPath;
			if (!FileSystemBatteries.isFile(relRefPath)){
				throw new Exception("File path provided using @FileDataReference annotation does not exist:" + refPath);
			}
			refPath = relRefPath;
		}		
		
		return refPath;
	}

	public static String getDataRefPath(Class<?> klass) throws Exception{
		return getDataRefPath((FileDataReference) klass.getAnnotation(FileDataReference.class));
	}
	
	public static String getDataRefName(Class<?> klass) throws Exception{
		FileDataReference dataRefAnn = (FileDataReference) klass.getAnnotation(FileDataReference.class); 
		return dataRefAnn.name();
	}
	
	public static int getInstanceThreadCount(Instances ann) throws Exception{
		if (ann.instanceThreads() < 1){
			return -1;
		} else {
			return ann.instanceThreads();
		}
	}
	
	public static int getCreatorThreadCount(Class<?> klass) throws Exception{
		TestClass testClassAnn = (TestClass) klass.getAnnotation(TestClass.class); 
		return testClassAnn.methodThreads();
	}
	
	public static int getTestThreadCount(Method m) throws Exception{
		TestMethod testMethodAnn = (TestMethod) m.getAnnotation(TestMethod.class);
		// DDT methods may not have TestMethod annotation, but are considered as Test Methods.
		if (testMethodAnn != null){
			return testMethodAnn.testThreads();
		} else {
			return 1;
		}
	}
	
	public static String getDataRefName(Method m) {
		FileDataReference dataRefAnn = (FileDataReference) m.getAnnotation(FileDataReference.class); 
		return dataRefAnn.name();
	}
	
	public static String getDataRefPath(Method m) throws Exception{
		return getDataRefPath((FileDataReference) m.getAnnotation(FileDataReference.class));
	}
	
	public static boolean isDataRefPresent(Class<?> klass){
		return klass.isAnnotationPresent(FileDataReference.class);
	}
	
	public static boolean isDataRefPresent(Method m){
		return m.isAnnotationPresent(FileDataReference.class);
	}
	
	public static boolean isInstancesAnnotationPresent(Class<?> klass){
		return klass.isAnnotationPresent(Instances.class);
	}
	
	public static boolean isInstancesAnnotationPresent(Method m){
		return m.isAnnotationPresent(Instances.class);
	}
	
	public static int getInstancesCount(Instances instancesAnnotation){
		int cloneCount = 1;
		if (instancesAnnotation.count() != 1){
			if (instancesAnnotation.count() < 1){
				cloneCount = -1;
			} else {
				cloneCount = instancesAnnotation.count();
			}
		} else {
			if (instancesAnnotation.value() < 1){
				cloneCount = -1;
			} else {
				cloneCount = instancesAnnotation.value();
			}
		}
		return cloneCount;
	}
	
	public static boolean hasUserSuppliedProperties(String mQualifiedName, Instances instancesAnn){
		String[] properties = instancesAnn.udv();
		if (!Arrays.equals(properties,checkArray)){
			if (properties.length == 0){
				System.err.println("Found empty properties in @Instances annotation: " + mQualifiedName);
				System.err.println("Exiting...");
				System.exit(1);
				return false;
			} else {
				return true;
			}
		} else {
			return false;
		}		
	}
	
	public static HashMap<Integer,HashMap<String,String>> loadUDVFromInstancesAnnotation(Instances instancesAnnotation, int instanceCount, boolean userHasSuppliedProperties){
		HashMap<Integer,HashMap<String,String>> invocationWiseProps = new HashMap<Integer,HashMap<String,String>>();
		for (int i=1; i <= instanceCount; i++){
			invocationWiseProps.put(i, new HashMap<String,String>());
		}
		
		if (!userHasSuppliedProperties){
			return invocationWiseProps;
		}

		String[] properties = instancesAnnotation.udv();
		
		for(String propString: properties){
			ArrayList<String> parts = DataBatteries.split(propString,"=");
			String propKey = parts.get(0);
			String propValuesString = parts.get(1);
			for (int i=1; i <= instanceCount; i++){
				invocationWiseProps.get(i).put(propKey, null);
			}
			
			// We need to be careful here. Instance count is human count, starts with 1.
			// Prop Values is computer counting, starts from 0
			ArrayList<String> propValues = DataBatteries.split(propValuesString,",");
			String lastValue = null;
			for (int i=1; i <= instanceCount; i++){
				if (i <= propValues.size()){
					lastValue = propValues.get(i-1);
				}
				invocationWiseProps.get(i).put(propKey, lastValue);
			}
		}
		return invocationWiseProps;
	}

}
