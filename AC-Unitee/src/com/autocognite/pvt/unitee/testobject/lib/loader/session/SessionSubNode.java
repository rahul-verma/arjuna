package com.autocognite.pvt.unitee.testobject.lib.loader.session;

import com.autocognite.pvt.batteries.value.DefaultStringKeyValueContainer;
import com.autocognite.pvt.unitee.runner.lib.slots.TestSlotExecutor;
import com.autocognite.pvt.unitee.testobject.lib.loader.group.Group;

public interface SessionSubNode {

	int getTestMethodCount();

	void load() throws Exception;

	Group getGroup() throws Exception;

	int getId();

	String getName();

	TestSlotExecutor next() throws Exception;

	Session getSession();

	SessionNode getSessionNode();

	DefaultStringKeyValueContainer getUDV();
}
