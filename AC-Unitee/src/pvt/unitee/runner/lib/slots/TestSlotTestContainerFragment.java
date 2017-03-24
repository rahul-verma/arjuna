package pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.log4j.Logger;

import pvt.arjunapro.ArjunaInternal;
import pvt.batteries.config.Batteries;
import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.testobject.lib.interfaces.TestContainerFragment;
import pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import pvt.unitee.testobject.lib.interfaces.TestCreator;

public class TestSlotTestContainerFragment {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private int slotNum;
	private TestContainerFragment testContainerFragment = null;
	private List<TestSlotTestCreator> slotTestCreators = null;
	private Iterator<TestSlotTestCreator> iter = null;
	
	public TestSlotTestContainerFragment (int slotNum, TestContainerFragment testContainerFragment){
		this.slotNum = slotNum;
		this.testContainerFragment = testContainerFragment;
		slotTestCreators = new ArrayList<TestSlotTestCreator>();
		if (ArjunaInternal.displaySlotsInfo){
			logger.debug("Creators for container fragment: " + testContainerFragment.getTestCreators());
		}
		for (TestCreator creator: testContainerFragment.getTestCreators()){
			slotTestCreators.add(new TestSlotTestCreator(slotNum, creator));
		}
		this.iter = slotTestCreators.iterator();
	}

	public TestContainerFragment getContainerFragment() {
		return testContainerFragment;
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
