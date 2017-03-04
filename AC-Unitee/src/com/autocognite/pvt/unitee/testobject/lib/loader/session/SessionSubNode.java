package com.autocognite.pvt.unitee.testobject.lib.loader.session;

import java.io.File;

import com.autocognite.batteries.value.StringKeyValueContainer;
import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.batteries.container.BaseContainer;
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

	StringKeyValueContainer getUDV();
}
