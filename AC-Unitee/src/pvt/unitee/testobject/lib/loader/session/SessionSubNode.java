package pvt.unitee.testobject.lib.loader.session;

import pvt.batteries.value.DefaultStringKeyValueContainer;
import pvt.unitee.runner.lib.slots.TestSlotExecutor;
import pvt.unitee.testobject.lib.loader.group.Group;

public interface SessionSubNode {

	int getTestMethodCount();

	void load() throws Exception;

	Group getGroup() throws Exception;

	int getId();

	String getName();

	TestSlotExecutor next() throws Exception;

	Session getSession();

	SessionNode getSessionNode();

	DefaultStringKeyValueContainer getUTV();
}
