package com.autocognite.pvt.unitee.testobject.lib.loader.group;

import com.autocognite.pvt.unitee.runner.lib.slots.TestSlotExecutor;

public interface TestLoader {

	void load() throws Exception;

	TestSlotExecutor next() throws Exception;

	int getTestMethodCount();

}