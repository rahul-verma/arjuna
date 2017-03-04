package com.autocognite.pvt.unitee.testobject.lib.loader;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

import com.autocognite.arjuna.annotations.TestClass;
import com.autocognite.arjuna.annotations.TestMethod;
import com.autocognite.batteries.config.RunConfig;
import com.autocognite.batteries.util.DataBatteries;
import com.autocognite.batteries.util.FileSystemBatteries;
import com.autocognite.pvt.batteries.enums.BatteriesPropertyType;

public class JavaTestLoadingUtils {
	private static String[] checkArray = new String[] {"NOT_SET"};
	
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
}
