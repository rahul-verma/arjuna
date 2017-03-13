package com.autocognite.pvt.unitee.testobject.lib.loader.group;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.utils.DataBatteries;
import com.autocognite.arjuna.utils.SystemBatteries;
import com.autocognite.pvt.arjuna.enums.PickerTargetType;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.batteries.console.Console;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import com.autocognite.pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import com.autocognite.pvt.unitee.testobject.lib.loader.tree.ExecutionSlotsCreator;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;

public abstract class AbstractPickerConfig implements PickerConfig {
	
	private Group group = null;
	private JsonElement elem = null;

	private PickerTargetType type = null;
	
	private List<String> PKG_CONSIDER;
	private List<String> PKG_IGNORE;
	private List<String> CLASS_CONSIDER;
	private List<String> CLASS_IGNORE;
	private List<String> METHOD_CONSIDER;
	private List<String> METHOD_IGNORE;
	private String CLASS_NAME;
	private String PACKAGE_NAME;
	
	public AbstractPickerConfig(){
		
	}
	
	public AbstractPickerConfig(Group group){
		this.setGroup(group);
		
	}

	public List<String> getConsiderPatterns(){
		switch (this.getTargetType()){
		case PACKAGES:
			return this.PKG_CONSIDER;
		case CLASSES:
			return this.CLASS_CONSIDER;
		case METHODS:
			return this.METHOD_CONSIDER;
		}
		return null;
	}
	
	public List<String> getIgnorePatterns(){
		switch (this.getTargetType()){
		case PACKAGES:
			return this.PKG_IGNORE;
		case CLASSES:
			return this.CLASS_IGNORE;
		case METHODS:
			return this.METHOD_IGNORE;
		}
		return null;
	}
	
	public void validate() throws Exception {
		if (!this.isValid()){
			throw new PickerMisConfiguration();
		}
		
	}
	
	private boolean isValid() throws Exception {
		// Validate package level
		if  ((this.isPackageConsiderOrIgnoreOptionProvided()) && (PACKAGE_NAME != null)){
			return false;			
		}
		
		// Validate class level
		if  ((this.isClassConsiderOrIgnoreOptionProvided()) && (PACKAGE_NAME == null)){
			return false;			
		}
		
		if  ((this.isPackageConsiderOrIgnoreOptionProvided()) && (this.isClassConsiderOrIgnoreOptionProvided())){
			return false;			
		}
		
		if  ((this.isPackageConsiderOrIgnoreOptionProvided()) && (this.getClassName() != null)){
			return false;			
		}
		
		if ((this.isClassConsiderOrIgnoreOptionProvided() || (this.getClassName() != null)) && (this.getPackageName() == null)){
			return false;
		}
		
		if ( ((CLASS_CONSIDER != null) && (CLASS_IGNORE != null)) || 
				((CLASS_CONSIDER != null) && (CLASS_NAME != null)) ||
					((CLASS_IGNORE != null) && (CLASS_NAME != null))){
			return false;			
		}
		
		// Validate method level
		if ((this.isMethodConsiderOrIgnoreOptionProvided()) && 
				((this.getPackageName() == null) || (this.getClassName() == null))
			){
			return false;
		}
		
		if  (((this.isPackageConsiderOrIgnoreOptionProvided()) || (this.isClassConsiderOrIgnoreOptionProvided())) 
				&& (this.isMethodConsiderOrIgnoreOptionProvided())){
			return false;			
		}
		
		if ((METHOD_CONSIDER != null) && (METHOD_IGNORE != null)){
			return false;			
		}
		
		return true;
	}
	
	private List<String> removeJavaSuffix(List<String> inList){
		List<String> outList = new ArrayList<String>();
		for (String s: inList){
			if (s.toLowerCase().endsWith(".java")){
				outList.add(s.substring(0, s.length() - 5));
			} else {
				outList.add(s);
			}
		}	
		return outList;
	}
	
	protected void configureClassConsiderPatterns(List<String> patterns){
		CLASS_CONSIDER = removeJavaSuffix(patterns);		
	}
	
	protected void configureClassIgnorePatterns(List<String> patterns){
		CLASS_IGNORE = removeJavaSuffix(patterns);		
	}
	
	protected void configureMethodConsiderPatterns(List<String> patterns){
		METHOD_CONSIDER = patterns;	
	}
	
	protected void configureMethodIgnorePatterns(List<String> patterns){
		METHOD_IGNORE = patterns;	
	}
	
	protected void configurePackageConsiderPatterns(List<String> patterns){
		PKG_CONSIDER = patterns;
	}
	
	protected void configurePackageIgnorePatterns(List<String> patterns){
		PKG_IGNORE = patterns;
	}
	
	protected void configurePackageName(String name){
		PACKAGE_NAME = name;
	}
	
	protected void configureClassName(String name){
		CLASS_NAME = name;
	}
	
	protected boolean isMethodConsiderOrIgnoreOptionProvided(){
		return (this.METHOD_CONSIDER != null) || (this.METHOD_IGNORE != null);
	}
	
	protected boolean isClassConsiderOrIgnoreOptionProvided(){
		return (this.CLASS_CONSIDER != null) || (this.CLASS_IGNORE != null);
	}
	
	protected boolean isPackageConsiderOrIgnoreOptionProvided(){
		return (this.PKG_CONSIDER != null) || (this.PKG_IGNORE != null);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.dev.testobject.lib.loader.group.IPickerConfig#getTargetType()
	 */
	@Override
	public PickerTargetType getTargetType() {
		return type;
	}

	protected void setTargetType(PickerTargetType type) {
		this.type = type;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.dev.testobject.lib.loader.group.IPickerConfig#createPicker()
	 */
	@Override
	public Picker createPicker() throws Exception{
		switch(this.getTargetType()){
		case CLASSES:
			return new ClassPicker(group, this);
		case METHODS:
			return new MethodPicker(group, this);
		case PACKAGES:
			return new PackagePicker(group, this);
		}
		return null;
	}

	@Override
	public Group getGroup() {
		return this.group;
	}
	
	@Override
	public void setGroup(Group group) {
		this.group = group;
	}

	public static void displayError(JsonElement pickerElement) throws IOException {
		Console.displayError("Your picker config: ");
		Gson gson = new GsonBuilder().setPrettyPrinting().create();

        String json = gson.toJson(pickerElement);
        List<String> parts = DataBatteries.split(json, SystemBatteries.getLineSeparator());
        for (String s: parts){
        	Console.displayError(s);
        }
		Console.displayError("Check your picker json w.r.t. the following rules:");
		BufferedReader txtReader = new BufferedReader(new InputStreamReader(AbstractPickerConfig.class.getResourceAsStream("/com/autocognite/pvt/text/pickers.help")));
		String line = null;
		while ((line = txtReader.readLine()) != null) {
			Console.displayError(line);
		}
		txtReader.close();
	}

	public String getPackageName() {
		return this.PACKAGE_NAME;
	}

	public String getClassName() {
		return this.CLASS_NAME;
	}
}


abstract class BasePicker implements Picker {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private List<String> considerPatterns = null;
	private List<String> ignorePatterns = null;
	private Group group;
	private AbstractPickerConfig config = null;
	
	public BasePicker(){
		
	}
	
	public BasePicker(Group group) { 
		this.group = group;
	}
	
	protected void init(){
		this.setConsiderPatterns(getPickerConfig().getConsiderPatterns());
		this.setIgnorePatterns(getPickerConfig().getIgnorePatterns());		
	}
	
	@Override
	public void setConsiderPatterns(List<String> patterns){
		this.considerPatterns = patterns;
	}
	
	@Override
	public void setIgnorePatterns(List<String> patterns){
		this.ignorePatterns = patterns;
	}

	public List<String> getConsiderPatterns() {
		return considerPatterns;
	}
	
	public List<String> getIgnorePatterns() {
		return ignorePatterns;
	}
	
	public Group getTestGroup(){
		return this.group;
	}

	protected boolean matched(String targetString){
		logger.debug("Target Object Name String: " + targetString);
		logger.debug("Ignore Pattern: " + this.getIgnorePatterns());
		logger.debug("Consider Pattern: " + this.getConsiderPatterns());
		boolean ignore = false;
		if (this.getIgnorePatterns() != null){
			logger.debug("Check ignore pattern match.");
			for (String m: this.getIgnorePatterns()){
				ignore = targetString.matches(m);
				if (ignore == true) {
					return false;
				}
			}
		}

		boolean consider = false;
		if (this.getConsiderPatterns() != null){
			logger.debug("Check consider pattern match.");
			for (String m: this.getConsiderPatterns()){
				if (m.startsWith("ARJUNANRX::")){
					consider = targetString.equals(m.replace("ARJUNANRX::", ""));
				} else {
					consider = targetString.matches(m);
				}
				if (consider == true) {
					return true;
				}
			}
		} else {
			return true;
		}
		
		return false;		
	}
	
	@Override
	public void setGroup(Group group) {
		this.group = group;
	}
	
	@Override
	public int load(ExecutionSlotsCreator execSlotsCreator, List<String> unpickedContainers) throws Exception {
		logger.debug(unpickedContainers);
		logger.debug(String.format("%s:%s: Picking containers" , this.getTestGroup().getName(), this.getClass().getSimpleName()));
		int testMethodCount = 0;
		Group group = this.getTestGroup();
		List<String> containers = new ArrayList<String>();
		for (String className: unpickedContainers){
			logger.debug(this.considerPatterns);
			logger.debug(String.format("Group: %s, Evaluating: %s", group.getName(), className)) ;
			JavaTestClassDefinition classDef = TestDefinitionsDB.getContainerDefinition(className);

			logger.debug("Check package name: " + classDef.getPackageName());
			if (!this.shouldIncludePackage(classDef.getPackageName())){
				continue;
			}
			
			logger.debug("Check class name: " + classDef.getName());
			if (!this.shouldIncludeContainer(classDef.getName())){
				continue;
			}
			
			logger.debug(String.format("Group: %s, Including: %s", group.getName(), className)) ;			
//			logger.debug(String.format("Included Class Loader: %s", classDef.getQualifiedName()));
			
			List<String> methodNames = classDef.getTestMethodQueue();
			logger.debug(methodNames) ;
			List<String> scheduledCreators = new ArrayList<String>();
			for (String methodName: methodNames){
				logger.debug(String.format("Group: %s, Evaluating: %s", group.getName(), methodName)) ;
				JavaTestMethodDefinition methodDef = classDef.getTestCreatorDefinition(methodName);	
				if ((methodDef.shouldBeSkipped()) || shouldIncludeMethod(methodName)){
					logger.debug(String.format("Group: %s, Including: %s", group.getName(), methodName)) ;
					scheduledCreators.add(methodName);
					execSlotsCreator.addTestCreatorName(methodDef.getQualifiedName());
					testMethodCount += 1;
					methodDef.setPicked();
				} else {
					continue;
				}
			}
			classDef.markScheduled(group.getSessionName(), scheduledCreators);
			classDef.markScheduledNonSkipped(group.getSessionName(), scheduledCreators);
			containers.add(className);
			classDef.setPicked();
			group.addClassMethodMap(classDef.getQualifiedName(), scheduledCreators);
		}
		
		TestDefinitionsDB.markScheduled(group.getSessionName(), containers);
		TestDefinitionsDB.markScheduledNonSkipped(group.getSessionName(), containers);
		return testMethodCount;
	}
	
	protected abstract boolean shouldIncludePackage(String packageName);
	
	protected abstract boolean shouldIncludeContainer(String containerName);
	
	protected abstract boolean shouldIncludeMethod(String methodName);

	public void setPickerConfig(AbstractPickerConfig config) {
		this.config = config;
	}
	
	public AbstractPickerConfig getPickerConfig() {
		return this.config;
	}
}

class PackagePicker extends BasePicker {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	
	public PackagePicker(Group group, AbstractPickerConfig config) throws Exception {
		super(group);
		this.setPickerConfig(config);
		init();
	}
	
	public PackagePicker(AbstractPickerConfig config){
		super();
		this.setPickerConfig(config);
		init();
	}
	
	protected boolean shouldIncludePackage(String packageName){
		return matched(packageName);		
	}
	
	protected boolean shouldIncludeContainer(String containerName){
		return true;
	}
	
	protected boolean shouldIncludeMethod(String methodName){
		return true;
	}
	
	public PickerTargetType getTargetType(){
		return PickerTargetType.PACKAGES;
	}
}

class ClassPicker extends BasePicker{
	private String pkg = null;
	private String lPkg = null;
	
	public ClassPicker(Group group, AbstractPickerConfig config) throws Exception {
		super(group);
		this.setPackageName(config.getPackageName());
		this.setPickerConfig(config);
		init();
	}
	
	protected boolean shouldIncludePackage(String packageName){
		return packageName.toLowerCase().equals(lPkg);		
	}
	
	protected boolean shouldIncludeContainer(String containerName){
		return this.matched(containerName);
	}
	
	protected boolean shouldIncludeMethod(String methodName){
		return true;
	}
	
	public void setPackageName(String name) {
		this.pkg = name;
		lPkg = pkg.toLowerCase();
	}
	
	public String getPackageName(){
		return this.pkg;
	}
	
	public PickerTargetType getTargetType(){
		return PickerTargetType.CLASSES;
	}

}

class MethodPicker extends BasePicker {
	private String pkg = null;
	private String lPkg = null;
	private String klass = null;
	private String lKlass = null;
	
	public MethodPicker(Group group, AbstractPickerConfig config) throws Exception {
		super(group);
		this.setPackageName(config.getPackageName());
		this.setClassName(config.getClassName());
		this.setPickerConfig(config);
		init();
	}
	
	protected boolean shouldIncludePackage(String packageName){
		return packageName.toLowerCase().equals(lPkg);		
	}
	
	protected boolean shouldIncludeContainer(String containerName){
		return containerName.toLowerCase().equals(lKlass);	
	}
	
	protected boolean shouldIncludeMethod(String methodName){
		return this.matched(methodName);
	}

	public void setPackageName(String name) {
		this.pkg = name;
		lPkg = pkg.toLowerCase();
	}
	
	public String getPackageName(){
		return this.pkg;
	}
	
	public void setClassName(String name) {
		this.klass = name;
		lKlass = klass.toLowerCase();	
	}
	
	public String getClassName(){
		return this.klass;
	}
	
	public PickerTargetType getTargetType(){
		return PickerTargetType.METHODS;
	}
}

/*
 * Allowed
cp
ip
cp ip
pn

pn cc
pn ic

pn cn cm
pn cn im

* When a session is passed, none of the picker options is allowed.
* msession should not be allowed as a name.
* magroup should be allowed as a name
* Other magic groups should not be allowed as names.
* BeginNode = mbnode, name should not be allowed for use.
* EndNode = mlnode, name should not be allowed for use.

Check for invalid:
------------------
cp pn (cli and conf) - Done
ip pn (cli and conf) - Done
No cp/ip/pn for packages target (conf)

cc - Done
ic - Done
cp cc - Done
cp cn - Done
cp ic - Done
ip cc - Done
ip cn - Done
ip ic - Done
pn cc ic - Done
pn cc cn - Done
pn ic cn - Done
No pn for classes target
No cp/ic/cn for classes target

cm
im
pn cc cm
pn cc im
pn ic cm
pn ic im
pn cn cm im
No pn for methods target
No cn for methods target
No cm/im for methods target

*/

