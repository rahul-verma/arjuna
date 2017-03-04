package com.autocognite.pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.batteries.config.RunConfig;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreator;

public class TestSlotTestContainerInstance {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private int slotNum;
	private TestContainerInstance testContainerInstance = null;
	private List<TestSlotTestCreator> slotTestCreators = null;
	private Iterator<TestSlotTestCreator> iter = null;
	
	public TestSlotTestContainerInstance (int slotNum, TestContainerInstance testContainerInstance){
		this.slotNum = slotNum;
		this.testContainerInstance = testContainerInstance;
		slotTestCreators = new ArrayList<TestSlotTestCreator>();
		if (ArjunaInternal.displaySlotsInfo){
			logger.debug("Creators for container instance: " + testContainerInstance.getTestCreators());
		}
		for (TestCreator creator: testContainerInstance.getTestCreators()){
			slotTestCreators.add(new TestSlotTestCreator(slotNum, creator));
		}
		this.iter = slotTestCreators.iterator();
	}

	public TestContainerInstance getContainerInstance() {
		return testContainerInstance;
	}
	
	public TestSlotTestCreator next() throws Exception{
		if (iter.hasNext()){
			return this.iter.next();
		} else {
			throw new SubTestsFinishedException("Done");
		}
	}

	public int getSlotNumber() {
		return this.slotNum;
	}
}
