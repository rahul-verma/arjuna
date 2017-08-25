package pvt.unitee.testobject.lib.loader.group;

import pvt.unitee.runner.lib.slots.TestSlotExecutor;

public interface GroupTestContainerScheduler {

	void schedule() throws Exception;

	TestSlotExecutor next() throws Exception;

	int getTestMethodCount();

	void load() throws Exception;

}