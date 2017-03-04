package com.autocognite.pvt.unitee.reporter.lib.event;

import java.lang.reflect.Type;

import com.autocognite.pvt.unitee.reporter.lib.reportable.BaseJsonResultDeserializer;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public class EventDeserializer extends BaseJsonResultDeserializer implements JsonDeserializer<Event> {
	
	public Event process(JsonObject resultPropsObj){
		EventBuilder builder = null;
		Event outResult = null;

		try{
			builder = new EventBuilder();

			//Deserialize autoProps
			EventProperties resultProps = new EventProperties();
			processJsonObjectForEnumMap(resultPropsObj, resultProps);
	
			outResult = builder.props(resultProps).build();
		} catch (Exception e){
			e.printStackTrace();
		}

		return outResult;		
	}
	
	@Override
	public Event deserialize(final JsonElement jsonElement, Type arg1, JsonDeserializationContext arg2) {
		JsonObject root = jsonElement.getAsJsonObject();
		return this.process(root);
	}

}
