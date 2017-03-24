package pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.testobject.lib.interfaces.TestContainer;

public class TestSlot {
	private int slotNum;
	private List<TestSlotTestContainer> testSlotContainers = null;
	private Iterator<TestSlotTestContainer> iter = null;
	
	public TestSlot (int slotNum, List<TestContainer> testContainers){
		this.slotNum = slotNum;
		testSlotContainers = new ArrayList<TestSlotTestContainer>();
		for (TestContainer container: testContainers){
			testSlotContainers.add(new TestSlotTestContainer(slotNum, container));
		}
		this.iter = testSlotContainers.iterator();
		
	}
	
	public TestSlotTestContainer next() throws Exception{
		if (iter.hasNext()){
			return iter.next();
		} else {
			throw new SubTestsFinishedException("Done");
		}
	}

	public int getSlotNumber() {
		return this.slotNum;
	}
}
