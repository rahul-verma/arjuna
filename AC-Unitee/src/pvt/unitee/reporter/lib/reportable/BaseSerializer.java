package pvt.unitee.reporter.lib.reportable;

import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

import com.google.gson.JsonArray;
import com.google.gson.JsonNull;
import com.google.gson.JsonObject;

import arjunasdk.interfaces.Value;
import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;

public class BaseSerializer {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	
	protected <T> JsonObject serializeEnumKeyMap(Map<T, Value> map) throws Exception{
		if (ArjunaInternal.logJsonSerializationInfo){
			logger.debug(map);
		}
		JsonObject propJsonObject = new JsonObject();
		for (T key: map.keySet()){
			this.addValueToJsonObject(propJsonObject, key.toString(), map.get(key));
		}		
		
		return propJsonObject;
	}
	
	private JsonArray getJsonArrayForStringList(List<String> l){
		JsonArray arr = new JsonArray();
		for (String s: l){
			arr.add(s);
		}
		return arr;
	}
	
	private JsonArray getJsonArrayForNumberList(List<Number> l){
		JsonArray arr = new JsonArray();
		for (Number s: l){
			arr.add(s);
		}
		return arr;
	}
		
	private void addValueToJsonObject(JsonObject obj, String key, Value value) throws Exception{
		switch(value.valueType()){
		case ANYREF:
			obj.addProperty(key, value.asString());
			break;
//		case ANYREF_LIST:
//			break;
		case BOOLEAN:
			obj.addProperty(key, value.asBoolean());
			break;
		case DOUBLE:
			obj.addProperty(key, value.asNumber());
			break;
		case ENUM:
			obj.addProperty(key, value.asString());
			break;
		case ENUM_LIST:
			obj.add(key, getJsonArrayForStringList(value.asStringList()));
			break;
		case FLOAT:
			obj.addProperty(key, value.asNumber());
			break;
		case INTEGER:
			obj.addProperty(key, value.asNumber());
			break;
		case LIST:
			obj.add(key, getJsonArrayForStringList(value.asStringList()));
			break;
		case LONG:
			obj.addProperty(key, value.asNumber());
			break;
		case NA:
			obj.addProperty(key, value.asString());
			break;
		case NOT_SET:
			obj.addProperty(key, value.asString());
			break;
		case NULL:
			obj.add(key, JsonNull.INSTANCE);
			break;
		case NUMBER:
			obj.addProperty(key, value.asNumber());
			break;
		case NUMBER_LIST:
			obj.add(key, getJsonArrayForNumberList(value.asNumberList()));
			break;
		case STRING:
			obj.addProperty(key, value.asString());
			break;
		case STRING_LIST:
			obj.add(key, getJsonArrayForStringList(value.asStringList()));
			break;
//		default:
//			break;		
		}	
	}
	
}
