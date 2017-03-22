package com.autocognite.pvt.unitee.testobject.lib.loader.group;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.FilenameUtils;
import org.apache.log4j.Logger;

import com.autocognite.arjuna.utils.console.Console;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.arjuna.enums.PickerTargetType;
import com.autocognite.pvt.arjuna.enums.SkipCode;
import com.autocognite.pvt.arjuna.enums.TestPickerProperty;
import com.autocognite.pvt.arjuna.enums.UnpickedCode;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.unitee.runner.lib.slots.TestSlotExecutor;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import com.autocognite.pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import com.autocognite.pvt.unitee.testobject.lib.loader.session.SessionSubNode;
import com.autocognite.pvt.unitee.testobject.lib.loader.tree.ExecutionSlotsCreator;

public class TestGroupsDB {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private Map<String, Group> defaultGroups = new HashMap<String, Group>();
	private Map<String,String> customGroupFileNames = new HashMap<String,String>();
	private PickerTargetType targetForMagicGroup = null;
	private String groupsDir;
	private PickerConfig config = null;

	public TestGroupsDB() throws Exception{
		this.defaultGroups.put("MBGROUP", new MBGroup());
		this.defaultGroups.put("MLGROUP", new MLGroup());		
	}
	
	public void createPickerConfigForCLIConfig(Map<TestPickerProperty, String> options) throws Exception{
		config = new PickerConfigForCLI(options);
		config.process();
	}
	
	public void createGroupForCLIOptions(Map<TestPickerProperty, String> options) throws Exception{
		createPickerConfigForCLIConfig(options);
		if (config.getTargetType() == null){
			// No pickers provided in CLI, so magroup would be used.
			return;
		}			
		String groupName = null;
		switch (config.getTargetType()){
		case CLASSES:
			groupName = "mfcgroup";
			break;
		case METHODS:
			groupName = "mfmgroup";
			break;
		case PACKAGES:
			groupName = "mfpgroup";
			break;
		}
		
		Group group = new DefaultTestGroup(groupName);
		config.setGroup(group);
		Picker picker = config.createPicker();
		logger.debug("Picker Type for CLI Options: " + picker.getClass().getSimpleName());
		group.setPickers(Arrays.asList((Picker)picker));
		
		if (group != null){
			this.defaultGroups.put(group.getName().toUpperCase(), group);
		}
	}
	
	public void createAllCapturingGroup() throws Exception{
		Group group = new DefaultTestGroup("magroup");
		Map<TestPickerProperty,String> options = new HashMap<TestPickerProperty,String>();
		options.put(TestPickerProperty.PACKAGE_CONSIDER_PATTERNS, ".*?");
		PickerConfig config = new PickerConfigForCLI(options);
		config.process();
		config.setGroup(group);
		Picker picker = config.createPicker();
		group.setPickers(Arrays.asList((Picker)picker));	
		this.defaultGroups.put(group.getName().toUpperCase(), group);
	}
	
	public Group getGroup(SessionSubNode subNode, String name) throws Exception{
		Group group = null;
		String uName = name.toUpperCase();
		if (this.customGroupFileNames.containsKey(uName)){
			group = new UserDefinedGroup(subNode, uName, groupsDir + "/" + this.customGroupFileNames.get(uName));
		} else if (this.defaultGroups.containsKey(uName)){
			group = this.defaultGroups.get(uName);
			group.setSessionSubNode(subNode);
		} else {
			String sessionFile = Batteries.value(ArjunaProperty.DIRECTORY_SESSIONS).asString() + "/" + subNode.getSession().getName() + ".conf";
			if ((name.toUpperCase().endsWith(".CONF")) && (this.customGroupFileNames.containsKey(uName.replace(".CONF", "")))){
					Console.displayError(
							String.format(
									"Provide group name >>%s<< without the conf extension in session file: >>%s<<.",
									uName.replace(".CONF", ""),
									sessionFile
							));
			} else {
					Console.displayError(
							String.format(
									"No group template found for group name >>%s<< specified in session file: >>%s<< ", 
									uName.replace(".CONF", ""), 
									sessionFile
					));
					
					if (name.toUpperCase().endsWith(".CONF")){
						Console.displayError("Also, provide group name without the conf extension.");
					}
			}
			
			Console.displayError("Exiting...");
			System.exit(1);
		}

		return group;
	}
	
	public void createUserDefinedGroups() throws Exception{
		groupsDir = Batteries.value(ArjunaProperty.DIRECTORY_GROUPS).asString();
		File sDir = new File(groupsDir);
		if (!sDir.isDirectory()){
			return;
		}
		for (File f: sDir.listFiles()){
			if (f.isFile()){
				if (f.getName().toUpperCase().endsWith(".CONF")){
					String gName = FilenameUtils.getBaseName(f.getName());
					this.customGroupFileNames.put(gName.toUpperCase(), f.getName());
				}
			}
		}		
	}

	public PickerTargetType getTargetForMagicGroup() {
		return config.getTargetType();
	}

}

class DefaultTestGroup extends BaseGroup{

	public DefaultTestGroup(String name) throws Exception {
		super(name);
		TestLoader loader = new JavaTestClassLoader(this);
		super.setLoader(loader);
	}
}

class MBGroup extends BaseGroup{
	
	public MBGroup() throws Exception {
		super("mbgroup");
		TestLoader loader = new SkippedJavaTestClassLoader(this);
		super.setLoader(loader);
	}
}

class MLGroup extends BaseGroup{

	public MLGroup() throws Exception {
		super("mlgroup");
		TestLoader loader = new UnselectedJavaTestClassLoader(this);
		super.setLoader(loader);
	}

}

class SkippedJavaTestClassLoader implements TestLoader {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private ExecutionSlotsCreator execSlotsCreator = null;
	private int testMethodCount = 0;
	private Group group = null;
	
	public SkippedJavaTestClassLoader(Group group) throws Exception{
		this.group = group;
		execSlotsCreator = new ExecutionSlotsCreator(group);
	}
	
	@Override
	public void load() throws Exception {
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Begin loading of tests for current test session.");
		}
		List<String> containers = new ArrayList<String>();
		for (String className: TestDefinitionsDB.getClassNameList()){
			logger.debug(String.format("Group: %s, Evaluating: %s", this.group.getName(), className)) ;
			JavaTestClassDefinition classDef = TestDefinitionsDB.getContainerDefinition(className);
			logger.debug("Should skip?" +  classDef.shouldBeSkipped());
			if (!classDef.shouldBeSkipped()){
				continue;
			}			
			logger.debug(String.format("Group: %s, Including: %s", this.group.getName(), className)) ;
//			logger.debug(String.format("Skip Class Loader: %s", classDef.getQualifiedName()));
			
			List<String> methodNames = classDef.getTestMethodQueue();
			for (String methodName: methodNames){
				JavaTestMethodDefinition methodDef = classDef.getTestCreatorDefinition(methodName);
				methodDef.setSkipped(SkipCode.SKIPPED_CLASS_ANNOTATION);
				if (ArjunaInternal.displayLoadingInfo){
					logger.debug("Included: " + methodName);
					logger.debug("Send to execution scheduler.");
				}
				execSlotsCreator.addTestCreatorName(methodDef.getQualifiedName());
				testMethodCount += 1;
			}
			containers.add(className);
		}
		TestDefinitionsDB.markScheduled(group.getSessionName(), containers);
		execSlotsCreator.load();	
		TestDefinitionsDB.removeAsSkipped(containers);
	}
	
	@Override
	public TestSlotExecutor next() throws Exception{
		return this.execSlotsCreator.next();
	}

	@Override
	public int getTestMethodCount() {
		return testMethodCount;
	}
}

class UnselectedJavaTestClassLoader implements TestLoader {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private ExecutionSlotsCreator execSlotsCreator = null;
	private int testMethodCount = 0;
	private Group group = null;
	
	public UnselectedJavaTestClassLoader(Group group) throws Exception{
		this.group = group;
		execSlotsCreator = new ExecutionSlotsCreator(group);
	}
	
	@Override
	public void load() throws Exception {
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Begin loading of tests for current test session.");
		}
		
		List<String> containers = new ArrayList<String>();
		for (String className: TestDefinitionsDB.getUnscheduledContainers()){
			logger.debug(String.format("Group: %s, Evaluating: %s", this.group.getName(), className)) ;
			JavaTestClassDefinition classDef = TestDefinitionsDB.getContainerDefinition(className);
			
//			logger.debug(String.format("Unselected Class Loader: %s", classDef.getQualifiedName()));
			
			List<String> methodNames = classDef.getTestMethodQueue();
			for (String methodName: methodNames){
				JavaTestMethodDefinition methodDef = classDef.getTestCreatorDefinition(methodName);
				methodDef.setUnpicked(UnpickedCode.UNPICKED_CLASS);
				if (ArjunaInternal.displayLoadingInfo){
					logger.debug("Included: " + methodName);
					logger.debug("Send to execution scheduler.");
				}
				execSlotsCreator.addTestCreatorName(methodDef.getQualifiedName());
				testMethodCount += 1;
			}
			classDef.setUnpicked(UnpickedCode.UNPICKED_CLASS);
			containers.add(className);
		}
		
		TestDefinitionsDB.markScheduled(group.getSessionName(), containers);

		logger.debug("Looking for unpicked methods");
		logger.debug(TestDefinitionsDB.getScheduledContainers());
		for (String className: TestDefinitionsDB.getScheduledContainers()){
			logger.debug(String.format("Group: %s, Evaluating: %s", this.group.getName(), className)) ;
			JavaTestClassDefinition classDef = TestDefinitionsDB.getContainerDefinition(className);
			
//			logger.debug(String.format("Unselected Class Loader: %s", classDef.getQualifiedName()));
			
			for (String methodName: classDef.getUnscheduledCreators()){
				logger.debug(String.format("Group: %s, Unpicked: %s", group.getName(), methodName)) ;
				JavaTestMethodDefinition methodDef = classDef.getTestCreatorDefinition(methodName);
				methodDef.setUnpicked(UnpickedCode.UNPICKED_METHOD);
				execSlotsCreator.addTestCreatorName(methodDef.getQualifiedName());
				testMethodCount += 1;
			}
			containers.add(className);
		}
		
		execSlotsCreator.load();	
	}
	
	@Override
	public TestSlotExecutor next() throws Exception{
		return this.execSlotsCreator.next();
	}

	@Override
	public int getTestMethodCount() {
		return testMethodCount;
	}
}

