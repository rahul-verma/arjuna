package com.autocognite.pvt.unitee.testobject.lib.loader.session;

import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.pvt.batteries.container.BaseContainer;
import com.autocognite.pvt.batteries.value.DefaultStringKeyValueContainer;
import com.autocognite.pvt.unitee.testobject.lib.loader.group.Group;

public interface SessionNode {

	int getTestMethodCount();

	void load() throws Exception;

	String getName();

	int getGroupThreadCount();

	SessionSubNode next() throws Exception;

	int getId();

	Session getSession();

	void setName(String name);

	DefaultStringKeyValueContainer getUDV();
}
