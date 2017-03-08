package com.autocognite.pvt.unitee.testobject.lib.definitions;

import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.interfaces.DataReference;
import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.DependencyTarget;
import com.autocognite.pvt.arjuna.enums.SkipCode;
import com.autocognite.pvt.arjuna.enums.UnpickedCode;
import com.autocognite.pvt.batteries.databroker.DataReferenceFactory;
import com.autocognite.pvt.unitee.core.lib.dependency.DependencyHandler;
import com.autocognite.pvt.unitee.core.lib.testvars.DefaultTestVariables;
import com.autocognite.pvt.unitee.core.lib.testvars.InternalTestVariables;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;
import com.autocognite.pvt.unitee.testobject.lib.java.TestClassConstructorType;
import com.autocognite.pvt.unitee.testobject.lib.loader.DataMethodsHandler;
import com.autocognite.pvt.unitee.testobject.lib.loader.JavaTestClassDataMethodsHandler;
import com.autocognite.pvt.unitee.testobject.lib.loader.TestPropertyAnnotationsProcessor;

public class JavaTestClassDefinition {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private DataMethodsHandler dataMethodsHandler = null;
	private String qualifiedName = null;
	private boolean dataRefPresent = false;
	private int instanceCount = 1;
	private InternalTestVariables testVars = null;
	private HashMap<Integer, InternalTestVariables> testClassInstanceTestVars = new HashMap<Integer, InternalTestVariables>();
	private Class<?> klass;
	private Constructor<?> constructor;
	private TestClassConstructorType constructorType;
	private TestFixtures fixtures = null;
	private List<String> methodNamesQueue = new ArrayList<String>();
	private List<String> unscheduledMethodsQueue = new ArrayList<String>();
	private List<String> scheduled = new ArrayList<String>();
	private Map<String, JavaTestMethodDefinition> methodDefinitions = new HashMap<String, JavaTestMethodDefinition>();
	private int instanceThreadCount = 1;
	private int creatorThreadCount = 1;
	private boolean skipIt = false;
	private SkipCode skipCode = null;
	private boolean unpicked = true;
	private UnpickedCode unpickCode = null;
	private String packageName = null;
	
	private Set<String> allMethodNameSet = new HashSet<String>();
	private Set<String> testMethodNameSet = new HashSet<String>();
	
	private Set<String> methodDependencies = new HashSet<String>();
	private Set<String> classDependencies = new HashSet<String>();
	
	public JavaTestClassDefinition() throws Exception{
		this.testVars = new DefaultTestVariables();
		this.testVars.populateDefaults();
		this.testVars.rawUdv().add(RunConfig.cloneCentralUDVs());
	}
	
	public String getPackageName() throws Exception {
		return this.packageName;
	}
	
	private String getPackageName(Class<?> klass) throws Exception {
		int index = klass.getName().lastIndexOf(klass.getSimpleName());
		if (index == 0) {
			return "default";
		} else {
			return klass.getName().substring(0, index - 1);
		}
	}

	public void setDataRefPresent(boolean flag) {
		this.dataRefPresent = flag;
	}

	public boolean isDataRefPresent() {
		return this.dataRefPresent;
	}

	public void addFileDataRefWithPath(String name, String path) throws Exception {
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug("Adding data reference");
		}
		DataReference dataRef = DataReferenceFactory.getReference(path);
		this.testVars.addDataReference(name, dataRef);
	}

	public int getInstanceCount() {
		return instanceCount;
	}

	public void setInstanceCount(int instanceCount) throws Exception {
		this.instanceCount = instanceCount;
		for (int i=1; i <= instanceCount; i++){
			this.testClassInstanceTestVars.put(i, new DefaultTestVariables());
		}
	}

	public void setUdvForInstance(int instanceNumber, HashMap<String, String> udv) throws Exception {
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(this.testClassInstanceTestVars);
			logger.debug(instanceNumber);
			logger.debug(this.testClassInstanceTestVars.get(instanceNumber));
			logger.debug(this.testClassInstanceTestVars.get(instanceNumber).udv());
			logger.debug(udv);
		}
		this.testClassInstanceTestVars.get(instanceNumber).udv().addAsStringValue(udv);
	}

	public Class<?> getUserTestClass() {
		return klass;
	}

	public void setUserTestClass(Class<?> klass) throws Exception {
		this.klass = klass;
		this.qualifiedName = klass.getName();
		DataMethodsHandler handler = new JavaTestClassDataMethodsHandler(klass);
		handler.process();
		this.dataMethodsHandler = handler;
		packageName = getPackageName(klass);
		this.testVars.rawObjectProps().setParentQualifiedName(packageName);
		this.testVars.rawObjectProps().setPackage(packageName);
		this.testVars.rawObjectProps().setClass(klass.getSimpleName());
		this.testVars.rawObjectProps().setName(klass.getSimpleName());
		
		TestPropertyAnnotationsProcessor.populateTestProps(this, this.testVars);
	}

	public void setConstructor(Constructor<?> constructor) {
		this.constructor = constructor;
	}

	public Constructor<?> getConstructor() {
		return constructor;
	}

	public void setConstructorType(TestClassConstructorType type) {
		this.constructorType = type;
	}

	public TestClassConstructorType getConstructorType() {
		return constructorType;
	}

	public void setFixtures(TestFixtures fixtures) {
		this.fixtures = fixtures;
	}

	public TestFixtures getFixtures() {
		return this.fixtures;
	}

	public void addTestMethodDefinition(String name, JavaTestMethodDefinition methodDef) {
		this.methodNamesQueue.add(name);
		this.unscheduledMethodsQueue.add(name);
		testMethodNameSet.add(name);
		allMethodNameSet.add(name);
		this.methodDefinitions.put(name, methodDef);
	}
	
	public synchronized void markScheduled(String sessionName, List<String> creatorNames) throws Exception{
		for (String cName: creatorNames){
			JavaTestMethodDefinition classDef = this.getTestCreatorDefinition(cName);
			classDef.updateSessionInfo(sessionName);
		}
		unscheduledMethodsQueue.removeAll(creatorNames);
	}
	
	public void markScheduledNonSkipped(String sessionName, List<String> names) throws Exception {
		markScheduled(sessionName, names);
		for (String name: names){
			if (!scheduled.contains(name)){
				scheduled.add(name);
			}
		}
	}
	
	public synchronized List<String> getUnscheduledCreators(){
		return unscheduledMethodsQueue;
	}

	public boolean hasMethodWithName(String depMethodName) {
		return this.methodDefinitions.containsKey(depMethodName);
	}

	public List<String> getTestMethodQueue() {
		return this.methodNamesQueue;
	}
	
	public JavaTestMethodDefinition getTestCreatorDefinition(String name) {
//		logger.debug(String.format("Fetching definition for test method: %s", name));
		return this.methodDefinitions.get(name);
	}

	public String getQualifiedName() {
		return this.qualifiedName;
	}

	public int getCreatorThreadCount() {
		return this.creatorThreadCount;
	}

	public DataMethodsHandler getDataMethodsHandler() {
		return dataMethodsHandler;
	}

	public int getInstanceThreadCount() {
		return this.instanceThreadCount;
	}

	public TestVariables getTestContainerInstanceDefinition(int instanceNumber) {
		return this.testClassInstanceTestVars.get(instanceNumber);
	}

	public TestVariables getTestVariables() {
		return this.testVars;
	}

	public void setCreatorThreadCount(int creatorThreadCount) {
		this.creatorThreadCount = creatorThreadCount;
	}

	public void setInstanceThreadCount(int instanceThreadCount) {
		this.instanceThreadCount = instanceThreadCount;
	}

	public void addNonTestMethodName(String name) {
		this.allMethodNameSet.add(name);
	}
	
	public synchronized boolean isTestMethod(String name) {
		return this.testMethodNameSet.contains(name);
	}
	
	public synchronized boolean hasMethod(String name) {
		return allMethodNameSet.contains(name);
	}
	
	public synchronized boolean isTestMethodMarkedForSkipping(String name) throws Exception {
		if (!testMethodNameSet.contains(name)){
			throw new Exception("Not a test method.");
		} else {
			return this.methodDefinitions.get(name).shouldBeSkipped();
		}
	}
	
	public void addDependencyMethodNames(List<String> names){
		this.methodDependencies.addAll(names);
	}
	
	public void addDependencyClassNames(List<String> names){
		this.classDependencies.addAll(names);
	}
	
	public Set<String> getDependencyMethodNames(){
		return this.methodDependencies;
	}
	
	public Set<String> getDependencyClassNames(){
		return this.classDependencies;
	}
	
	public List<DependencyHandler> getDependencies() {
		ArrayList<DependencyHandler> dependencies = new ArrayList<DependencyHandler>();
		DependencyHandler methodDep = new DependencyHandler();
		methodDep.setTargets(this.methodDependencies);
		methodDep.setType(DependencyTarget.TEST_METHODS);
		dependencies.add(methodDep);
		
		DependencyHandler classDep = new DependencyHandler();
		classDep.setTargets(this.classDependencies);
		classDep.setType(DependencyTarget.TEST_CLASSES);
		dependencies.add(classDep);		
		return dependencies;
	}
	
	public void updateSessionInfo(String sessionName) throws Exception{
		this.testVars.rawObjectProps().setSessionName(sessionName);	
	}
	
	public void setPicked() throws Exception{
		logger.debug(String.format("Mark Class Def picked: %s", this.getQualifiedName()));
		this.unpicked = false;
		this.unpickCode = null;
	}
	
	public void setUnpicked(UnpickedCode code) throws Exception{
		logger.debug(String.format("Mark Class Def Unpicked: %s", this.getQualifiedName()));
		this.unpicked = true;
		this.unpickCode = code;
	}
	
	public void setSkipped(SkipCode code) throws Exception{
		logger.debug(String.format("Mark Class Def Skipped: %s", this.getQualifiedName()));
		this.skipIt = true;
		this.skipCode = code;
		this.unpicked = false;
		logger.debug("Should Skip?" + this.shouldBeSkipped());
	}

	public boolean shouldBeSkipped() throws Exception{
		return this.skipIt;
	}
	
	public boolean isUnpicked() throws Exception{
		return this.unpicked;
	}

	public UnpickedCode getUnpickCode() {
		return this.unpickCode;
	}
	
	public SkipCode getSkipCode() {
		return this.skipCode;
	}

	public String getName() {
		return klass.getSimpleName();
	}

}
