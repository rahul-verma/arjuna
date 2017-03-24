package pvt.unitee.testobject.lib.definitions;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import com.arjunapro.ddt.interfaces.DataReference;
import com.arjunapro.ddt.interfaces.DataSource;
import com.arjunapro.testauto.interfaces.TestVariables;

import pvt.arjunapro.enums.DependencyTarget;
import pvt.arjunapro.enums.SkipCode;
import pvt.arjunapro.enums.UnpickedCode;
import pvt.batteries.databroker.DataReferenceFactory;
import pvt.unitee.core.lib.datasource.DataSourceBuilder;
import pvt.unitee.core.lib.datasource.DummyDataSource;
import pvt.unitee.core.lib.dependency.DependencyHandler;
import pvt.unitee.core.lib.testvars.DefaultTestVariables;
import pvt.unitee.core.lib.testvars.InternalTestVariables;
import pvt.unitee.testobject.lib.loader.MethodSignatureType;
import pvt.unitee.testobject.lib.loader.TestPropertyAnnotationsProcessor;

public class JavaTestMethodDefinition {
	private boolean dataRefPresent = false;
	private String dataRefPath = null;
	private int instanceCount = 1;
	private int instanceThreadCount = 1;
	private InternalTestVariables testVars = null;
	private HashMap<Integer, InternalTestVariables> testMethodInstanceTestVars = new HashMap<Integer, InternalTestVariables>();
	private JavaTestClassDefinition parentClassDefinition = null;
	private Method method = null;
	private Set<String> methodDependencies = new HashSet<String>();
	private Set<String> classDependencies = new HashSet<String>();
	private int testThreadCount = 1;
	private MethodSignatureType methodSignatureType = null;
	private boolean hasDataAssociation = false;
	private DataSourceBuilder dsBuilder;
	private String name = null;
	private String qualifiedName;
	private boolean selectable = false;
	private boolean skipIt = false;
	private SkipCode skipCode = null;
	private boolean selected = false;
	private boolean unpicked = true;
	private UnpickedCode unpickCode = null;
	private boolean consumed = false;
	
	public JavaTestMethodDefinition() throws Exception{
		this.testVars = new DefaultTestVariables();
		this.testMethodInstanceTestVars.put(1, new DefaultTestVariables());
	}

	public void setDataRefPresent(boolean flag) {
		this.dataRefPresent = flag;
	}

	public boolean isDataRefPresent() {
		return this.dataRefPresent;
	}
	
	public void addFileDataRefWithPath(String name, String path) throws Exception {
		DataReference dataRef = DataReferenceFactory.getReference(path);
		this.testVars.addDataReference(name, dataRef);
	}

	public int getInstanceCount() {
		return instanceCount;
	}

	public void setInstanceCount(int instanceCount) throws Exception {
		this.instanceCount = instanceCount;
		for (int i=1; i <= instanceCount; i++){
			this.testMethodInstanceTestVars.put(i, new DefaultTestVariables());
		}
	}

	public void setUtvForInstance(int instanceNumber, HashMap<String, String> utv) throws Exception {
		this.testMethodInstanceTestVars.get(instanceNumber).rawUtv().addAsStringValue(utv);
	}
	
	public TestVariables getTestCreatorInstanceDefinition(int instanceNumber) {
		return this.testMethodInstanceTestVars.get(instanceNumber);
	}
	
	public JavaTestClassDefinition getClassDefinition() {
		return this.parentClassDefinition;
	}

	public void setClassDefinition(JavaTestClassDefinition classDef) {
		parentClassDefinition = classDef;
	}

	public void setMethod(Method m) throws Exception {
		this.method = m;
		this.name = m.getName();
		this.qualifiedName = getClassDefinition().getQualifiedName() + "." + getName();	
		this.testVars.rawObjectProps().setName(name);
		this.testVars.rawObjectProps().setMethod(name);
		TestPropertyAnnotationsProcessor.populateTestProps(this, this.testVars);
	}
	
	public Method getMethod() {
		return this.method;
	}
	
	public void addDependencyMethodNames(List<String> names){
		this.methodDependencies.addAll(names);
	}
	
	public void addDependencyClassNames(List<String> names){
		this.classDependencies.addAll(names);
	}

	public String getQualifiedName() {
		return this.qualifiedName;
	}
	
	public String getName() {
		return name;
	}

	public TestVariables getTestVariables() {
		return this.testVars;
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

	public int getTestThreadCount() {
		return this.testThreadCount;
	}
	
	public void setTestThreadCount(int count) {
		this.testThreadCount = count;
	}

	public void setMethodSignatureType(MethodSignatureType type) {
		this.methodSignatureType  = type;
	}
	
	public MethodSignatureType getMethodSignatureType() {
		return this.methodSignatureType;
	}

	public boolean hasDataAssociation() {
		return hasDataAssociation;
	}

	public void enableDataAssociation() {
		this.hasDataAssociation = true;
	}

	public void setDataSourceBuilder(DataSourceBuilder builder) {
		this.dsBuilder = builder;
	}

	public synchronized DataSource getDataSource() throws Exception {
		if (this.dsBuilder!=null){
			return this.dsBuilder.build();
		} else {
			return new DummyDataSource();
		}
	}
	
	public int getInstanceThreadCount(){
		return this.instanceThreadCount;
	}
	
	public void setInstanceThreadCount(int instanceThreadCount) {
		this.instanceThreadCount = instanceThreadCount;
	}
	
	public void updateSessionInfo(String sessionName) throws Exception{
		this.testVars.rawObjectProps().setSessionName(sessionName);
	}
	
	public void setPicked() throws Exception{
		this.unpicked = false;
		this.unpickCode = null;
	}
	
	public void setUnpicked(UnpickedCode code) throws Exception{
		this.unpicked = true;
		this.unpickCode = code;
	}
	
	public void setSkipped(SkipCode code){
		this.skipIt = true;
		this.selectable = false;
		this.skipCode = code;
		this.unpicked = false;
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
}
