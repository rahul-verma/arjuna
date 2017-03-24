package pvt.unitee.runner.lib.slots;

import pvt.unitee.testobject.lib.interfaces.Test;
import pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

public class TestSlotTestCreatorInstance {
	private int slotNum;
	private TestCreatorInstance creatorInstance;

	public TestSlotTestCreatorInstance(int slotNum, TestCreatorInstance creatorInstance) {
		this.slotNum = slotNum;
		this.creatorInstance = creatorInstance;
	}

	public TestCreatorInstance getCreatorInstance() {
		return creatorInstance;
	}

	public Test next() throws Exception{
		return this.creatorInstance.next();
	}

	public int getSlotNumber() {
		return this.slotNum;
	}
}
