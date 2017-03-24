package pvt.unitee.testobject.lib.loader.group;

import pvt.unitee.runner.lib.slots.TestSlotExecutor;

public interface TestLoader {

	void load() throws Exception;

	TestSlotExecutor next() throws Exception;

	int getTestMethodCount();

}