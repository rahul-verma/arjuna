package com.autocognite.pvt.unitee.testobject.lib.loader.group;

import java.util.List;

import com.autocognite.pvt.batteries.value.DefaultStringKeyValueContainer;
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

	DefaultStringKeyValueContainer getUTV();

	SessionNode getSessionNode();
	
	SessionSubNode getSessionSubNode();

	void setSessionSubNode(SessionSubNode node);

	void addClassMethodMap(String qualifiedName, List<String> scheduledCreators);

	List<String> getScheduledCreatorsForContainer(String qualifiedName);

}
