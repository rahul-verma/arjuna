package pvt.unitee.reporter.lib.event;

import java.lang.reflect.Type;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;

import pvt.unitee.reporter.lib.reportable.BaseSerializer;

public class EventSerializer extends BaseSerializer implements JsonSerializer<Event>{

	protected JsonObject process(Event activity){
		try{
			return serializeEnumKeyMap(activity.infoProps().items());
		} catch (Exception e){
			JsonObject jsonObject = new JsonObject();
			jsonObject.addProperty("rType", "Error in getting string representation");
			e.printStackTrace();
			return jsonObject;
		}
	}	
	
	@Override
	public JsonElement serialize(Event activity, Type arg1, JsonSerializationContext arg2) {
		return this.process(activity);
	}
	
}
