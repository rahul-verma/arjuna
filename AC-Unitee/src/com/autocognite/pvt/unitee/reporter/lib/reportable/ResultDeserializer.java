package com.autocognite.pvt.unitee.reporter.lib.reportable;

import java.lang.reflect.Type;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public abstract class ResultDeserializer<T> extends BaseJsonResultDeserializer implements JsonDeserializer<T> {
	
	protected abstract T process(JsonObject root);

	@Override
	public T deserialize(final JsonElement jsonElement, Type arg1, JsonDeserializationContext arg2) {
		JsonObject root = jsonElement.getAsJsonObject();
		return this.process(root);
	}

}
