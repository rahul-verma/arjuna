package com.autocognite.pvt.unitee.reporter.lib.reportable;

import java.lang.reflect.Type;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;

public abstract class ResultSerializer<T> extends BaseTestResultSerializer implements JsonSerializer<T> {
	
	protected abstract void process(T result, JsonObject jsonObject);

	@Override
	public JsonElement serialize(T result, Type arg1, JsonSerializationContext arg2) {
		final JsonObject jsonObject = new JsonObject();
		this.process(result, jsonObject);
		return jsonObject;
	}
	
}
