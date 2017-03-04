package com.autocognite.pvt.unitee.testobject.lib.loader.session;

import java.util.HashMap;

import com.autocognite.batteries.value.StringKeyValueContainer;
import com.autocognite.batteries.value.Value;
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

	StringKeyValueContainer getUDV();

	void setUDVs(StringKeyValueContainer udvs);
}
