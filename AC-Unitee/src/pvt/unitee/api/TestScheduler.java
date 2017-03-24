package pvt.unitee.api;

import pvt.unitee.runner.lib.slots.TestSlotExecutor;

public interface TestScheduler{
	public TestSlotExecutor next() throws Exception;
	public int getTestMethodCount();
	public void process() throws Exception;
}
