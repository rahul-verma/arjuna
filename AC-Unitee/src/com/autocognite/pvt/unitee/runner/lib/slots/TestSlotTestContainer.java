package com.autocognite.pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainer;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;

public class TestSlotTestContainer {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private int slotNum;
	private TestContainer testContainer = null;
	private List<TestSlotTestContainerInstance> testSlotContainerInstances = null;
	private Iterator<TestSlotTestContainerInstance> iter = null;
	
	public TestSlotTestContainer (int slotNum, TestContainer testContainer){
		if (ArjunaInternal.displaySlotsInfo){
			logger.info(String.format("Test Slot # %d", slotNum));
			logger.debug(String.format("Preparing Test Container %s in Execution Slot# %d", testContainer.getQualifiedName(), slotNum));
		}
		this.slotNum = slotNum;
		this.testContainer = testContainer;
		testSlotContainerInstances = new ArrayList<TestSlotTestContainerInstance>();
		for (TestContainerInstance containerInstance: testContainer.getInstances()){
			testSlotContainerInstances.add(new TestSlotTestContainerInstance(slotNum, containerInstance));
		}
		this.iter = testSlotContainerInstances.iterator();
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Number of container instances: %d", testSlotContainerInstances.size()));
		}
		
	}

	public TestContainer getTestContainer() {
		return testContainer;
	}
	
	public TestSlotTestContainerInstance next() throws Exception{
		if (iter.hasNext()){
			return this.iter.next();
		} else {
			throw new SubTestsFinishedException("Done");
		}
	}

	public void ignoreFurtherInstances() {
		// TODO Auto-generated method stub
		
	}

	public int getSlotNumber() {
		return this.slotNum;
	}
}
