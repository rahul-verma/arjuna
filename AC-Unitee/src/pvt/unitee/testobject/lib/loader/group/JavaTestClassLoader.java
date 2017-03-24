package pvt.unitee.testobject.lib.loader.group;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import pvt.arjunapro.ArjunaInternal;
import pvt.batteries.config.Batteries;
import pvt.unitee.runner.lib.slots.TestSlotExecutor;
import pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import pvt.unitee.testobject.lib.loader.tree.ExecutionSlotsCreator;

public class JavaTestClassLoader implements TestLoader {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private ExecutionSlotsCreator execSlotsCreator = null;
	private int testMethodCount = 0;
	private Group group = null;
	
	public JavaTestClassLoader(Group group) throws Exception{
		this.group = group;
		this.execSlotsCreator = new ExecutionSlotsCreator(group);
	}
	
	@Override
	public void load() throws Exception {
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Begin loading of tests for current test session.");
		}
		
		List<String> unpickedContainers;
		
		int tmCount = 0;
		logger.debug(String.format("%s: Looping over pickers...", this.group.getName()));
		for (Picker picker: group.getPickers()){
			unpickedContainers = new ArrayList<String>();
			unpickedContainers.addAll(TestDefinitionsDB.getClassNameList());
			tmCount = picker.load(execSlotsCreator, unpickedContainers);
			this.testMethodCount += tmCount;
		}
//		List<String> unpickedContainers = TestDefinitionsDB.getUnscheduledContainers();
//
//		List<String> containers = new ArrayList<String>();
//		for (String className: TestDefinitionsDB.getUnscheduledContainers()){
//			logger.debug(String.format("Group: %s, Evaluating: %s", this.group.getName(), className)) ;
//			JavaTestClassDefinition classDef = TestDefinitionsDB.getContainerDefinition(className);
//			
//			if (!Unitee.getTestFilterForDiscovery().shouldIncludeClass(className)){
//				continue;
//			}
//			logger.debug(String.format("Group: %s, Including: %s", this.group.getName(), className)) ;			
////			logger.debug(String.format("Included Class Loader: %s", classDef.getQualifiedName()));
//			
//			List<String> methodNames = classDef.getTestMethodQueue();
//			List<String> scheduledCreators = new ArrayList<String>();
//			for (String methodName: methodNames){
//				logger.debug(String.format("Group: %s, Evaluating: %s", this.group.getName(), methodName)) ;
//				JavaTestMethodDefinition methodDef = classDef.getTestCreatorDefinition(methodName);	
//				if ((methodDef.shouldBeSkipped()) || (Unitee.getTestFilterForDiscovery().shouldIncludeMethod(methodName))){
//					logger.debug(String.format("Group: %s, Including: %s", this.group.getName(), methodName)) ;
//					scheduledCreators.add(methodName);
//					execSlotsCreator.addTestCreatorName(methodDef.getQualifiedName());
//					testMethodCount += 1;
//					methodDef.setPicked();
//				} else {
//					continue;
//				}
//			}
//			classDef.markScheduled(group.getSessionName(), group.getName(), scheduledCreators);
//			for (String methodName: classDef.getUnscheduledCreators()){
//				logger.debug(String.format("Group: %s, Unpicked: %s", this.group.getName(), methodName)) ;
//				JavaTestMethodDefinition methodDef = classDef.getTestCreatorDefinition(methodName);
//				methodDef.setUnpicked(UnpickedCode.UNPICKED_METHOD);
//				execSlotsCreator.addTestCreatorName(methodDef.getQualifiedName());
//				testMethodCount += 1;
//			}
//			containers.add(className);
//			classDef.setPicked();
//		}
//		
//		TestDefinitionsDB.markScheduled(group.getSessionName(), group.getName(), containers);
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