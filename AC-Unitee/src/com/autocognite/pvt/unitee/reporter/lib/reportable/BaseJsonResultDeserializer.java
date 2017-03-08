package com.autocognite.pvt.unitee.reporter.lib.reportable;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map.Entry;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.bases.DefaultDataRecord;
import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.enums.ValueType;
import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.pvt.batteries.container.BaseValueContainer;
import com.autocognite.pvt.batteries.value.DefaultStringKeyValueContainer;
import com.autocognite.pvt.batteries.value.DoubleValue;
import com.autocognite.pvt.batteries.value.EnumValue;
import com.autocognite.pvt.batteries.value.IntValue;
import com.autocognite.pvt.batteries.value.LongValue;
import com.autocognite.pvt.batteries.value.NAValue;
import com.autocognite.pvt.batteries.value.NotSetValue;
import com.autocognite.pvt.batteries.value.NullValue;
import com.autocognite.pvt.batteries.value.StringListValue;
import com.autocognite.pvt.batteries.value.StringValue;
import com.autocognite.pvt.unitee.core.lib.testvars.DefaultTestObjectProperties;
import com.autocognite.pvt.unitee.core.lib.testvars.DefaultTestProperties;
import com.autocognite.pvt.unitee.core.lib.testvars.DefaultTestVariables;
import com.autocognite.pvt.unitee.core.lib.testvars.InternalTestVariables;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public class BaseJsonResultDeserializer {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	
	protected InternalTestVariables getTestVars(JsonObject root){
		InternalTestVariables testVars = null;
		
		try{
			testVars = new DefaultTestVariables();

			//Deserialize autoProps
			JsonObject autoPropsObj = root.get("objectProps").getAsJsonObject();
			DefaultTestObjectProperties autoProps = new DefaultTestObjectProperties();
			processJsonObjectForEnumMap(autoPropsObj, autoProps);
			testVars.setObjectProps(autoProps);


			//Deserialize autoProps
			JsonObject testPropsObj = root.get("testProps").getAsJsonObject();
			DefaultTestProperties testProps = new DefaultTestProperties();
			processJsonObjectForEnumMap(testPropsObj, testProps);
			testVars.setTestProps(testProps);			


			//Deserialize customProps
			JsonObject customPropsObj = root.get("customProps").getAsJsonObject();
			DefaultStringKeyValueContainer customProps = new DefaultStringKeyValueContainer();
			processJsonObjectForEnumMap(customPropsObj, customProps);
			testVars.setCustomProps(customProps);	

			//Deserialize udv
			JsonObject udvObj = root.get("udv").getAsJsonObject();
			DefaultStringKeyValueContainer udvProps = new DefaultStringKeyValueContainer();
			processJsonObjectForEnumMap(udvObj, udvProps);
			testVars.setUdv(udvProps);	

			//Deserialize dataRecord
			JsonObject drObj = root.get("dataRecord").getAsJsonObject();
			DefaultDataRecord drProps = new DefaultDataRecord();
			processJsonObjectForEnumMap(drObj, drProps);
			testVars.setDataRecord(drProps);
		} catch (Exception e){
			e.printStackTrace();
		}		
		
		return testVars;
	}
	
	protected <T> void processJsonObjectForEnumMap(
			JsonObject jsonObj, 
			BaseValueContainer<T> propContainer
			){
		Iterator<Entry<String, JsonElement>> iter = jsonObj.entrySet().iterator();
		Entry<String, JsonElement> entry = null;
		while(iter.hasNext()){
			entry = iter.next();
			String propName = entry.getKey();
			ValueType targetType = propContainer.valueType(propName);
			propContainer.add(propContainer.key(propName), jsonElementToValue(propContainer, propName, entry.getValue(), targetType));
		}		
	}

	protected <T> Value jsonElementToValue(BaseValueContainer<T> propContainer, String propName, JsonElement element, ValueType targetType) {
		switch (targetType){
		case ENUM:
			return jsonValueToEnumValue(element, propContainer.valueEnumType(propName));
		case INTEGER:
			return jsonValueToIntValue(element);
		case STRING:
			return jsonValueToStringValue(element);		
		case STRING_LIST:
			return jsonValueToListValue(element);
		case LONG:
			return jsonValueToLongValue(element);
		case DOUBLE:
			return jsonValueToDoubleValue(element);
		}
		return new NullValue();
	}

	protected Value jsonValueToStringValue(JsonElement element){
		String val = element.getAsJsonPrimitive().getAsString();
		if (val.equals("NOT_SET")){
			return new NotSetValue();
		} else if (val.equals("NA")){
			return new NAValue();
		} else {
			return new StringValue(element.getAsJsonPrimitive().getAsString());
		}
	}

	protected Value jsonValueToIntValue(JsonElement element){
		String val = element.getAsJsonPrimitive().getAsString();
		if (val.equals("NA")){
			return new NAValue();
		} else if (val.equals("NOT_SET")){
			return new NotSetValue();
		}
		return new IntValue(element.getAsJsonPrimitive().getAsInt());
	}
	
	protected Value jsonValueToLongValue(JsonElement element){
		String val = element.getAsJsonPrimitive().getAsString();
		if (val.equals("NA")){
			return new NAValue();
		} else if (val.equals("NOT_SET")){
			return new NotSetValue();
		}
		return new LongValue(element.getAsJsonPrimitive().getAsLong());
	}
	
	protected Value jsonValueToDoubleValue(JsonElement element){
		String val = element.getAsJsonPrimitive().getAsString();
		if (val.equals("NA")){
			return new NAValue();
		} else if (val.equals("NOT_SET")){
			return new NotSetValue();
		}
		return new DoubleValue(element.getAsJsonPrimitive().getAsDouble());
	}

	protected <T extends Enum<T>> Value jsonValueToEnumValue(JsonElement element, Class<T> klass){
		String val = element.getAsJsonPrimitive().getAsString();
		if (val.equals("NOT_SET")){
			return new NotSetValue();
		} else {		
			return new EnumValue<T>(Enum.valueOf(klass, val));
		}
	}

	protected Value jsonValueToListValue(JsonElement element){
		String val = element.getAsJsonPrimitive().getAsString();
		if (val.equals("NA")){
			return new NAValue();
		}
		List<String> outArr = new ArrayList<String>();
		JsonArray arr = element.getAsJsonArray();
		for (JsonElement elem: arr){
			outArr.add(elem.getAsString());
		}
		return new StringListValue(outArr);
	}
}
