package pvt.unitee.testobject.lib.definitions;

import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.log4j.Logger;

import arjunasdk.ddauto.interfaces.DataReference;
import pvt.batteries.config.Batteries;
import pvt.batteries.databroker.DataReferenceFactory;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.core.lib.datasource.DataSourceType;
import pvt.unitee.core.lib.dependency.DependencyHandler;
import pvt.unitee.core.lib.testvars.DefaultTestVariables;
import pvt.unitee.core.lib.testvars.InternalTestVariables;
import pvt.unitee.enums.DependencyTarget;
import pvt.unitee.enums.IgnoredTestReason;
import pvt.unitee.enums.IgnoredTestStatus;
import pvt.unitee.enums.IssueSubType;
import pvt.unitee.enums.IssueType;
import pvt.unitee.enums.SkipCode;
import pvt.unitee.enums.UnpickedCode;
import pvt.unitee.reporter.lib.ignored.IgnoredTest;
import pvt.unitee.reporter.lib.ignored.IgnoredTestBuilder;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.issue.IssueBuilder;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.java.TestClassConstructorType;
import pvt.unitee.testobject.lib.java.loader.DataMethodsHandler;
import pvt.unitee.testobject.lib.java.loader.JavaTestClassDataMethodsHandler;
import pvt.unitee.testobject.lib.java.loader.JavaTestClassFixturesLoader;
import pvt.unitee.testobject.lib.java.loader.TestPropertyAnnotationsProcessor;
import unitee.interfaces.TestVariables;

public class JavaTestClassDefinition {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
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
	private int instanceThreadCount = 1;
	private int creatorThreadCount = 1;
	private boolean skipIt = false;
	private SkipCode skipCode = null;
	private boolean unpicked = true;
	private UnpickedCode unpickCode = null;
	private String packageName = null;
	
	private Set<String> methodDependencies = new HashSet<String>();
	private Set<String> classDependencies = new HashSet<String>();
	private Map<String, DataSourceType> dsMap = null;
	
	// For checking whether a method name exists in a given class
	private Set<String> allMethodsNameSet = new HashSet<String>();
	// For pulling out class definitions by name
	private Map<String, JavaTestMethodDefinition> testMethodDefinitions = new HashMap<String, JavaTestMethodDefinition>();
	private List<String> dicoveredQueue = new ArrayList<String>();
	// This is what would be got by groups for pickers processing. If a group picks up something, it calls setPicked()
	private List<String> forPickerProcessing = new ArrayList<String>();
	// The following gets populated from above, if classDef.isNotPickedByAnyGroup() is True
	private List<String> forProcessor = new ArrayList<String>();
	private JavaTestClassFixturesLoader fixtureLoader = null;
	
	public JavaTestClassDefinition() throws Exception{
		this.testVars = new DefaultTestVariables();
		this.testVars.populateDefaults();
		this.testVars.rawExecVars().add(Batteries.cloneCentralExecVars());
		this.fixtureLoader = new JavaTestClassFixturesLoader(this);
	}
	
	public JavaTestClassFixturesLoader getFixturesLoader(){
		return this.fixtureLoader;
	}
	
	public synchronized List<String> getMethodDefQueueForDefPickerProcessing(){
		return forPickerProcessing;
	}
	
	public synchronized List<String> getMethodDefQueueForDefProcessor(){
		return forProcessor;
	}
	
	public void registerTestMethodDefinition(String name, JavaTestMethodDefinition methodDef) {
		if (ArjunaInternal.displayLoadingInfo){
			this.logger.debug(String.format("Registering method definition for: %s", name));
		}
		allMethodsNameSet.add(name);
		testMethodDefinitions.put(name, methodDef);
		dicoveredQueue.add(name);
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

	public void setExecVarsForInstance(int instanceNumber, HashMap<String, String> execVars) throws Exception {
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(this.testClassInstanceTestVars);
			logger.debug(instanceNumber);
			logger.debug(this.testClassInstanceTestVars.get(instanceNumber));
			logger.debug(this.testClassInstanceTestVars.get(instanceNumber).execVars());
			logger.debug(execVars);
		}
		this.testClassInstanceTestVars.get(instanceNumber).rawExecVars().addAsStringValue(execVars);
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
		
		this.testVars.rawTestProps().setPriority(1);
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
	
	public JavaTestMethodDefinition getTestCreatorDefinition(String name) {
//		logger.debug(String.format("Fetching definition for test method: %s", name));
		return this.testMethodDefinitions.get(name);
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
		this.allMethodsNameSet.add(name);
	}
	
	public synchronized boolean isTestMethod(String name) {
		return this.testMethodDefinitions.containsKey(name);
	}
	
	public synchronized boolean hasMethod(String name) {
		return allMethodsNameSet.contains(name);
	}
	
	public synchronized boolean isTestMethodMarkedForSkipping(String name) throws Exception {
		if (!isTestMethod(name)){
			throw new Exception("Not a test method.");
		} else {
			return this.testMethodDefinitions.get(name).shouldBeSkipped();
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
	
	public void setPicked(){
		logger.debug(String.format("Mark Class Def picked: %s", this.getQualifiedName()));
		this.unpicked = false;
		this.unpickCode = null;
	}
	
	public void setUnpicked(UnpickedCode code){
		logger.debug(String.format("Mark Class Def Unpicked: %s", this.getQualifiedName()));
		this.unpicked = true;
		this.unpickCode = code;
	}

	public boolean shouldBeSkipped(){
		return this.skipIt;
	}
	
	public boolean isPicked(){
		return !this.unpicked;
	}
	
	public boolean isUnpicked(){
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

	public void setSkipCode(SkipCode code) {
		this.skipCode = code;
	}

	public void setDataSourceMap(Map<String, DataSourceType> map) {
		this.dsMap = map;
	}
	
	public Map<String, DataSourceType> getDataSourceMap(){
		return this.dsMap;
	}

	public JavaTestMethodDefinition getTestMethodDefinition(String qName) {
		return this.testMethodDefinitions.get(qName);
	}
	
	public void buildPickerQueueFromDiscoveredQueue() throws Exception{
		for (String name: this.dicoveredQueue){
			JavaTestMethodDefinition methodDef = testMethodDefinitions.get(name);
			if (!this.shouldBeSkipped()){
				if (!methodDef.shouldBeSkipped()){
					forPickerProcessing.add(name);
				} else {
					methodDef.setSkipped(SkipCode.SKIPPED_METHOD_ANNOTATION);
				}
			} else {
				System.out.println(this.getSkipCode());
				methodDef.setSkipped(this.getSkipCode());
				System.out.println(methodDef.getSkipCode());
			}
			
			if (methodDef.shouldBeSkipped()){
				IgnoredTestBuilder builder = new IgnoredTestBuilder();
				
				methodDef.getTestVariables().rawObjectProps().setPackage(this.testVars.rawObjectProps().pkg());
				methodDef.getTestVariables().rawObjectProps().setClass(this.getName());
				IgnoredTest it = builder
				.testVariables(methodDef.getTestVariables())
				.status(IgnoredTestStatus.SKIPPED)
				.reason(IgnoredTestReason.valueOf(methodDef.getSkipCode().toString()))
				.build();
				ArjunaInternal.getReporter().update(it);
			}
		}
	}

	public void buildProcessorQueueFromPickerQueue() throws Exception{
		for (String name: forPickerProcessing){
			JavaTestMethodDefinition methodDef = testMethodDefinitions.get(name);
			if (this.isPicked()){
				if (methodDef.isPicked()){
					forProcessor.add(name);
				} else {
					methodDef.setUnpicked(UnpickedCode.UNPICKED_METHOD);
				}
			} else {
				methodDef.setUnpicked(this.getUnpickCode());
			}
			
			if (methodDef.isUnpicked()){
				methodDef.getTestVariables().rawObjectProps().setPackage(this.testVars.rawObjectProps().pkg());
				methodDef.getTestVariables().rawObjectProps().setClass(this.getName());
				IgnoredTestBuilder builder = new IgnoredTestBuilder();
				IgnoredTest it = builder
				.testVariables(methodDef.getTestVariables())
				.status(IgnoredTestStatus.UNPICKED)
				.reason(IgnoredTestReason.valueOf(methodDef.getUnpickCode().toString()))
				.build();
				ArjunaInternal.getReporter().update(it);
			}
		}
	}

	public void setSkipped(SkipCode code) {
		this.skipIt = true;
		this.skipCode = code;
	}

}
