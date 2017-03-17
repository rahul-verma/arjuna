package com.autocognite.pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreator;

public class TestSlotTestContainerInstance {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private int slotNum;
	private TestContainerInstance testContainerInstance = null;
	private List<TestSlotTestContainerFragment> slotTestClassFragments = null;
	private Iterator<TestSlotTestContainerFragment> iter = null;
	
	public TestSlotTestContainerInstance (int slotNum, TestContainerInstance testContainerInstance){
		this.slotNum = slotNum;
		this.testContainerInstance = testContainerInstance;
		slotTestClassFragments = new ArrayList<TestSlotTestContainerFragment>();
		slotTestClassFragments.add(new TestSlotTestContainerFragment(slotNum, testContainerInstance.getCurrentFragment()));
		this.iter = slotTestClassFragments.iterator();
	}

	public TestContainerInstance getContainerInstance() {
		return testContainerInstance;
	}
	
	public TestSlotTestContainerFragment next() throws Exception{
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
