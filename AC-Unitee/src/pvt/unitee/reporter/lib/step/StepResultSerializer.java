package pvt.unitee.reporter.lib.step;

import java.lang.reflect.Type;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;

import pvt.unitee.reporter.lib.reportable.BaseSerializer;

public class StepResultSerializer extends BaseSerializer implements JsonSerializer<StepResult> {
	
	protected JsonObject process(StepResult result){
		try{
			return serializeEnumKeyMap(result.resultProps().items());
		} catch (Exception e){
			JsonObject jsonObject = new JsonObject();
			jsonObject.addProperty("rType", "Error in getting string representation");
			e.printStackTrace();
			return jsonObject;
		}
	}	
	
	@Override
	public JsonElement serialize(StepResult result, Type arg1, JsonSerializationContext arg2) {
		return this.process(result);
	}
}
