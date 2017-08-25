package pvt.unitee.testobject.lib.loader.group;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.runner.lib.slots.TestSlotExecutor;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import pvt.unitee.testobject.lib.loader.tree.ExecutionSlotsCreator;

public class JavaTestClassGroupScheduler implements GroupTestContainerScheduler {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private ExecutionSlotsCreator execSlotsCreator = null;
	private int testMethodCount = 0;
	private Group group = null;
	
	public JavaTestClassGroupScheduler(Group group) throws Exception{
		this.group = group;
		this.execSlotsCreator = new ExecutionSlotsCreator(group);
	}
	
	@Override
	public void schedule() throws Exception {
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Begin loading of tests for current test session.");
		}
		
		List<String> containerNames = TestDefinitionsDB.getClassDefQueueForDefPickerProcessing();
		logger.debug(containerNames);
		logger.debug(String.format("%s:%s: Picking containers" , group.getName(), this.getClass().getSimpleName()));
		
		int tmCount = 0;
		logger.debug(String.format("%s: Looping over pickers...", this.group.getName()));
		for (Picker picker: group.getPickers()){
			for (String containerName: containerNames){
				JavaTestClassDefinition classDef = TestDefinitionsDB.getContainerDefinition(containerName);
				// This queue already contains unskipped containers
				if (classDef.isUnpicked()){
					tmCount = picker.pick(execSlotsCreator, classDef);
					this.testMethodCount += tmCount;		
				}
			}
		}
	}
	
	@Override
	public TestSlotExecutor next() throws Exception{
		return this.execSlotsCreator.next();
	}

	@Override
	public int getTestMethodCount() {
		return testMethodCount;
	}

	@Override
	public void load() throws Exception {
		// Loading should happen 
		execSlotsCreator.load();	
	}
}