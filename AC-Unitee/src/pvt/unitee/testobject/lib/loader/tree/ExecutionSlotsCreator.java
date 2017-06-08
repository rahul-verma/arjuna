package pvt.unitee.testobject.lib.loader.tree;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import pvt.batteries.config.Batteries;
import pvt.batteries.value.DefaultStringKeyValueContainer;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.enums.SkipCode;
import pvt.unitee.enums.TestResultCode;
import pvt.unitee.enums.UnpickedCode;
import pvt.unitee.runner.lib.slots.TestSlotExecutor;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;
import pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import pvt.unitee.testobject.lib.interfaces.TestContainer;
import pvt.unitee.testobject.lib.java.JavaTestClass;
import pvt.unitee.testobject.lib.loader.group.Group;

public class ExecutionSlotsCreator {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private HashMap<Integer,ArrayList<JavaTestMethodDefinition>> execMap = new HashMap<Integer,ArrayList<JavaTestMethodDefinition>>();
	private Map<String, TestContainer> createdContainerObjects = new HashMap<String, TestContainer>();
	private DependencyTree depTree =  null;
	private Group group = null;
	
	private List<String> scheduledMethods = new ArrayList<String>();
	private ArrayList<Integer> slots = new ArrayList<Integer>();
	private Iterator<Integer> slotIter = null;
	private Iterator<TestMethodNode> slotCreatorIter = null;
	private int currentSlotNum = 0;
	private HashMap<String,Integer> methodToSlotMap = new HashMap<String,Integer>();
	private DefaultStringKeyValueContainer utvars = new DefaultStringKeyValueContainer();
//	
	public ExecutionSlotsCreator(Group group) throws Exception{
		this.group = group;
		this.utvars.cloneAdd(group.getUTV().items());
	}
	
	public void addTestCreatorName(String name){
		scheduledMethods.add(name);
	}
	
	private boolean areAllEdgesScheduledForNode(TestNode node){
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Check whether all edge dependencies are met: " + node.getName());
		}
		if (node.getEdges().size() == 0){
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("No scheduling dependencies");
			}
			return true;
		} else {		
			Iterator<TestNode> iter = node.getEdges().iterator();
			while(iter.hasNext()){
				TestNode edge = iter.next();
				if (edge == null) continue;
				if (ArjunaInternal.logDependencyExecResolutionInfo){
					logger.debug(edge.getName());
				}
				if (this.depTree.doesMethodDepExist(edge.getName())){
					if (ArjunaInternal.logDependencyExecResolutionInfo){
						logger.debug("Still Exists: " + edge.getName());
					}
					return false;
				} else {
					if (ArjunaInternal.logDependencyExecResolutionInfo){
						logger.debug("Method dep does not exist now: " + edge.getName());
					}
					if (this.methodToSlotMap.get(edge.getName()) == this.currentSlotNum){
						return false;
					}
				}
			}
		
		}
		
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("All schedule dependencies met: " + node.getName());
		}
		return true;
	}
	
	public void load() throws Exception {
		depTree = TestDefinitionsDB.getDependencyTreeBuilder().getDepenencyTree(this.scheduledMethods);
		if (ArjunaInternal.displayDependencyDefInfo){
			logger.debug("Begin dependency tree processing");
		}
		this.currentSlotNum = 1;
		while(!this.depTree.isEmpty()){
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("Building creator queue for slot#: " + this.currentSlotNum);
			}
			slots.add(currentSlotNum);
			execMap.put(currentSlotNum, new ArrayList<JavaTestMethodDefinition>());
			Iterator<String> iter = this.depTree.iterator();
			ArrayList<String> scheduled = new ArrayList<String>();
			while(iter.hasNext()){
				TestMethodNode node = this.depTree.getNode(iter.next());
				boolean depMet = false;
				if (ArjunaInternal.displayLoadingInfo){
					logger.debug("Checking eligibility for scheduling: " + node.getName());
				}
				depMet = areAllEdgesScheduledForNode(node); 
				if (depMet){		
					if (ArjunaInternal.displayLoadingInfo){
						logger.debug(String.format("Adding to Slot# %d, Creator: %s", this.currentSlotNum, node.getName()));
					}

					this.execMap.get(currentSlotNum).add(node.getCreatorDefinition());
					methodToSlotMap.put(node.getName(), this.currentSlotNum);
					if (ArjunaInternal.displayDependencyDefInfo){
						logger.debug("Removing from dependencies: " + node.getName());
					}
					this.depTree.removeMethodDependency(node.getName());
					scheduled.add(node.getName());	
				} else {
					if (ArjunaInternal.displayDependencyDefInfo){
						logger.debug("Scheduling dependencies not met.");
					}					
				}
			}
			
			this.depTree.removeFromQueue(scheduled);

			currentSlotNum += 1;
		}

		if (ArjunaInternal.displaySlotsInfo){
			for (int slot: slots){
				logger.debug("Slot#" + slot);
				for (JavaTestMethodDefinition creator: this.execMap.get(slot)){
					String cName = creator.getQualifiedName();
					logger.debug(cName);
				}
			}
		}
		this.slotIter = slots.iterator();
	}

	public List<TestContainer> getContainerList (int slotNum, ArrayList<JavaTestMethodDefinition> methodDefQueue) throws Exception{
		// From Slot 2, onwards, the executor names must be reset if the container was already created in previous slots
		for (String name: this.createdContainerObjects.keySet()){
			this.createdContainerObjects.get(name).resetExecutorCreatorQueue();
		}
		
		List<TestContainer> containers =  new ArrayList<TestContainer>();
		JavaTestClassDefinition currentClassDef = null; 
		TestContainer currentContainer = null;
		for (JavaTestMethodDefinition methodDef: methodDefQueue){
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("Loading method: " + methodDef.getQualifiedName());
			}
			if (methodDef.getClassDefinition() != currentClassDef){
				if (currentClassDef != null){
					containers.add(currentContainer);
				} 
				
				String className = methodDef.getClassDefinition().getUserTestClass().getName();
				
				currentClassDef = methodDef.getClassDefinition();
				if (this.createdContainerObjects.containsKey(className)){
					if (ArjunaInternal.displayLoadingInfo){
						logger.debug("Using existing container with name: " + className);
					}
					currentContainer =  this.createdContainerObjects.get(className);
				} else {
					if (ArjunaInternal.displayLoadingInfo){
						logger.debug("Creating new container with name: " + className);
					}
					JavaTestClassDefinition classDef = methodDef.getClassDefinition();
					currentContainer = new JavaTestClass(classDef);
					currentContainer.setGroup(this.group);
					currentContainer.setAllScheduledCreators(this.group.getScheduledCreatorsForContainer(currentContainer.getQualifiedName()));
					logger.debug(classDef.getQualifiedName());
					 if (classDef.shouldBeSkipped()){
							logger.debug("Should be Skipped.");
							currentContainer.markSkipped(
									  TestResultCode.valueOf(SkipCode.SKIPPED_CLASS_ANNOTATION.toString()),
									  String.format("%s has @Skip.", classDef.getQualifiedName())
							);							
					} else if (classDef.isUnpicked()){
						logger.debug("Was Filtered.");
						currentContainer.markUnSelected(
								  TestResultCode.valueOf(UnpickedCode.UNPICKED_CLASS.toString()),
								  String.format("%s not selected.", classDef.getQualifiedName())
						);						
					} 
					this.createdContainerObjects.put(className, currentContainer);
				}
			} else {
				if (ArjunaInternal.displayLoadingInfo){
					logger.debug("Creator would be added to same container: " + currentClassDef.getQualifiedName());
				}
			}
			if (ArjunaInternal.displayLoadingInfo){
				logger.debug("Add creator to container: " + methodDef.getMethod().getName());
			}
			currentContainer.addExecutableCreatorName(methodDef.getMethod().getName());
		}
		
		//Adding last one to the Queue
		if (currentContainer != null){
			containers.add(currentContainer);
		}
		
		List<TestContainer> consideredContainers = new ArrayList<TestContainer>();
		Iterator<TestContainer> iter = containers.iterator();
		TestContainer lContainer = null;
		while(iter.hasNext()){
			lContainer = iter.next();
			try{
				// For container already present in previous slots, instances would have been loaded.
				if (ArjunaInternal.displayLoadingInfo){
					logger.debug("Are container instances already created? " + lContainer.areInstancesCreated());
				}
				if (!lContainer.areInstancesCreated()){
					if (ArjunaInternal.displayLoadingInfo){
						logger.debug("No. Loading now.");
					}
					lContainer.load();
				}
				lContainer.loadInstances();
				consideredContainers.add(lContainer);
			} catch (Throwable e){
				Console.displayExceptionBlock(e);
				consideredContainers.add(lContainer);				
			}
		}
		if (ArjunaInternal.displaySlotsInfo){
			logger.debug("Total test container units in slot# " + slotNum + ": " + containers.size());
		}
		return consideredContainers;
	}

	public TestSlotExecutor next() throws Exception{
		if (ArjunaInternal.displaySlotsInfo){
			logger.debug("Fetch next slot executor...");
		}
		if (this.slotIter.hasNext()){
			int slotNum = this.slotIter.next();
			return new TestSlotExecutor(slotNum, group.getClassThreadCount(), this.getContainerList(slotNum, this.execMap.get(slotNum)));
		} else {
			throw new SubTestsFinishedException("Done");
		}	
	}

}

