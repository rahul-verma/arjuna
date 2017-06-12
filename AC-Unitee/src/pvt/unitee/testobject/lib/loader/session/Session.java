package pvt.unitee.testobject.lib.loader.session;

import com.google.gson.JsonObject;

import pvt.batteries.value.DefaultStringKeyValueContainer;

public interface Session {

	int getTestMethodCount();

	SessionNode next() throws Exception;

	void load() throws Exception;

	String getName();

	JsonObject getConfigObject();

	String getSessionFilePath();

	JsonObject getExecVarObject();

	DefaultStringKeyValueContainer getExecVars();

	void setExecVars(DefaultStringKeyValueContainer execVars);

	JsonObject getUserOptionsObject();
}
