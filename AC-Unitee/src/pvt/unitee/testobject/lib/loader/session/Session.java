package pvt.unitee.testobject.lib.loader.session;

import com.google.gson.JsonObject;

import pvt.batteries.value.DefaultStringKeyValueContainer;
import pvt.unitee.arjuna.TestGroupsDB;

public interface Session {

	int getTestMethodCount();

	SessionNode next() throws Exception;

	void schedule() throws Exception;

	String getName();

	JsonObject getConfigObject();

	String getSessionFilePath();

	JsonObject getExecVarObject();

	DefaultStringKeyValueContainer getExecVars();

	void setExecVars(DefaultStringKeyValueContainer execVars);

	JsonObject getUserOptionsObject();

	boolean isDefaultSession();

	TestGroupsDB getGroupsDB();

	void load() throws Exception;
}
