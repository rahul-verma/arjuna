package com.autocognite.pvt.unitee.testobject.lib.loader.group;

import java.lang.reflect.Executable;
import java.util.List;

import com.autocognite.batteries.value.StringKeyValueContainer;
import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.batteries.container.BaseContainer;
import com.autocognite.pvt.unitee.runner.lib.slots.TestSlotExecutor;
import com.autocognite.pvt.unitee.testobject.lib.loader.session.SessionNode;
import com.autocognite.pvt.unitee.testobject.lib.loader.session.SessionSubNode;

public interface Group {

	String getName();

	TestSlotExecutor next() throws Exception;

	int getTestMethodCount();

	void load() throws Exception;

	String getSessionName();

	List<Picker> getPickers();

	void setPickers(List<Picker> pickerList);

	void setSessionName(String name);

	String getDefinitionFile();

	int getClassThreadCount();

	StringKeyValueContainer getUDV();

	SessionNode getSessionNode();
	
	SessionSubNode getSessionSubNode();

	void setSessionSubNode(SessionSubNode node);

}
