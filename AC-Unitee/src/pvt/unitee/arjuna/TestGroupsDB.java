package pvt.unitee.arjuna;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.io.FilenameUtils;
import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import pvt.batteries.config.Batteries;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.enums.PickerTargetType;
import pvt.unitee.enums.TestPickerProperty;
import pvt.unitee.testobject.lib.loader.group.BaseGroup;
import pvt.unitee.testobject.lib.loader.group.Group;
import pvt.unitee.testobject.lib.loader.group.GroupTestContainerScheduler;
import pvt.unitee.testobject.lib.loader.group.JavaTestClassGroupScheduler;
import pvt.unitee.testobject.lib.loader.group.Picker;
import pvt.unitee.testobject.lib.loader.group.PickerConfig;
import pvt.unitee.testobject.lib.loader.group.PickerConfigForCLI;
import pvt.unitee.testobject.lib.loader.group.UserDefinedGroup;
import pvt.unitee.testobject.lib.loader.session.Session;
import pvt.unitee.testobject.lib.loader.session.SessionSubNode;

public class TestGroupsDB {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private Map<String, Group> defaultGroups = new HashMap<String, Group>();
	private Map<String,String> customGroupFileNames = new HashMap<String,String>();
	private PickerTargetType targetForMagicGroup = null;
	private String groupsDir;
	private PickerConfig config = null;
	private Session session = null;

	public TestGroupsDB(Session session) throws Exception{
		this.session = session;
		loadAvailableGroupNames();
	}
	
	private void loadAvailableGroupNames() throws Exception{
		groupsDir = Batteries.value(ArjunaProperty.PROJECT_GROUPS_DIR).asString();
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
	
	public Group createMagicFilterGroup(SessionSubNode subNode, PickerConfig config) throws Exception{		
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
		group.setSessionSubNode(subNode);
		if (group != null){
			this.defaultGroups.put(group.getName().toUpperCase(), group);
		}
		return group;
	}
	
	public Group createAllCapturingGroup(SessionSubNode subNode) throws Exception{
		Group group = new DefaultTestGroup("magroup");
		Map<TestPickerProperty,String> options = new HashMap<TestPickerProperty,String>();
		options.put(TestPickerProperty.PACKAGE_CONSIDER_PATTERNS, ".*?");
		PickerConfig config = new PickerConfigForCLI(options);
		config.process();
		config.setGroup(group);
		Picker picker = config.createPicker();
		group.setPickers(Arrays.asList((Picker)picker));
		group.setSessionSubNode(subNode);
		this.defaultGroups.put(group.getName().toUpperCase(), group);
		return group;
	}
	
	public Group createGroup(SessionSubNode subNode, String name) throws Exception{
		Group group = null;
		String uName = name.toUpperCase();
		if (this.customGroupFileNames.containsKey(uName)){
			group = new UserDefinedGroup(subNode, uName, groupsDir + "/" + this.customGroupFileNames.get(uName));
		} else if (this.defaultGroups.containsKey(uName)){
			group = this.defaultGroups.get(uName);
			group.setSessionSubNode(subNode);
		} else {
			String sessionFile = Batteries.value(ArjunaProperty.PROJECT_SESSIONS_DIR).asString() + "/" + subNode.getSession().getName() + ".conf";
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

}

class DefaultTestGroup extends BaseGroup{

	public DefaultTestGroup(String name) throws Exception {
		super(name);
		GroupTestContainerScheduler loader = new JavaTestClassGroupScheduler(this);
		super.setLoader(loader);
	}
}