package com.autocognite.pvt.unitee.testobject.lib.loader.session;

import java.util.HashMap;

import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.pvt.batteries.value.DefaultStringKeyValueContainer;
import com.google.gson.JsonObject;
import com.typesafe.config.ConfigObject;

public interface Session {

	int getTestMethodCount();

	SessionNode next() throws Exception;

	void load() throws Exception;

	String getName();

	JsonObject getConfigObject();

	String getSessionFilePath();

	JsonObject getUDVObject();

	DefaultStringKeyValueContainer getUDV();

	void setUDVs(DefaultStringKeyValueContainer udvs);
}
