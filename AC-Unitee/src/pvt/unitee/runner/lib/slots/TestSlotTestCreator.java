package pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.testobject.lib.interfaces.TestCreator;
import pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

public class TestSlotTestCreator {
	private int slotNum;
	private TestCreator testCreator = null;
	private List<TestSlotTestCreatorInstance> slotTestCreatorInstances = null;
	private Iterator<TestSlotTestCreatorInstance> iter = null;
	
	public TestSlotTestCreator (int slotNum, TestCreator testCreator){
		this.slotNum = slotNum;
		this.testCreator = testCreator;
		slotTestCreatorInstances = new ArrayList<TestSlotTestCreatorInstance>();
		for (TestCreatorInstance creatorInstance: testCreator.getInstances()){
			slotTestCreatorInstances.add(new TestSlotTestCreatorInstance(slotNum, creatorInstance));
		}
		this.iter = slotTestCreatorInstances.iterator();
	}

	public TestCreator getTestCreator() {
		return testCreator;
	}
	
	public TestSlotTestCreatorInstance next() throws Exception{
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
