package pvt.unitee.testobject.lib.java.loader;

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
import pvt.unitee.testobject.lib.loader.tree.DependencyTreeBuilder;
import unitee.annotations.Instances;
import unitee.annotations.Skip;
import unitee.annotations.TestClass;

public class JavaTestClassDefLoader implements TestDefInitializer {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private ClassLoader classLoader = null;
	private List<Class<?>> testClasses = new ArrayList<Class<?>>();
	String testDir = null;
	
	@Override
	public void init(String testDir) throws Exception{
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
	
	private boolean isTestClass(Class<?> klass){
		return klass.isAnnotationPresent(TestClass.class) || klass.getSimpleName().startsWith("Test");
	}
	
	public void handle(DiscoveredFile f){
		try{
			String qualifiedName = getQualifiedName(f);
			if (ArjunaInternal.displayUserTestLoadingInfo){
				logger.debug("Get Class Loader for: " + qualifiedName);
			}
			Class<?> klass = this.loadClass(f, qualifiedName);		

			if (!this.isTestClass(klass)) {
				ArjunaInternal.processNonTestClass(klass);
				TestDefinitionsDB.addNonTestClassName(klass.getName());			
			} else {
				testClasses.add(klass);
			}
		} catch (Throwable e) {
			Console.displayExceptionBlock(e);
		}
	}
	
	@Override
	public void load() {
		for (Class<?> testClass: this.testClasses){
			this.load(testClass, testClass.getName());
		}
	}

	private void load(Class<?> klass, String qualifiedName){
		JavaTestClass jTestClass = null;

		try {
			//boolean include = JavaObjectFilter.shouldIncludeClass(cls);
//							logger.debug("Filtering: " + fullQualifiedClassName);

			
			boolean isReserved = false;
			isReserved = AnnotationValidator.validateReservedNamedClass(klass, qualifiedName);
			if (!isReserved){
				AnnotationValidator.validateClassAnnotations(klass, qualifiedName);
			}
			
			JavaTestClassDefinition classDef = new JavaTestClassDefinition();
			classDef.setUserTestClass(klass);
			
			// Filter early for better performance, no further processing
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("Process selection: " + qualifiedName);
			}
			
			if (klass.isAnnotationPresent(Skip.class)){
				classDef.setSkipped(SkipCode.SKIPPED_CLASS_ANNOTATION);
			}
			
			TestCreatorLoader creatorLoader = new JavaTestMethodsDefLoader(this, classDef);
			creatorLoader.load();
			
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
	
	public List<Class<?>> getSuperClasses(Class<?> klass) {
		  List<Class<?>> classList = new ArrayList<Class<?>>();
		  Class<?> superclass = klass.getSuperclass();
		  classList.add(superclass);
		  while (superclass != null) {   
		    klass = superclass;
		    superclass = klass.getSuperclass();
		    if (superclass != null){
		    	classList.add(superclass);
		    }
		  }
		  return classList;
	}
}