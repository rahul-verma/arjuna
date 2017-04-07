package pvt.unitee.reporter.lib.step;

import java.lang.reflect.Type;

import com.arjunapro.testauto.console.Console;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import pvt.unitee.reporter.lib.reportable.BaseJsonResultDeserializer;

public class StepResultDeserializer extends BaseJsonResultDeserializer implements JsonDeserializer<StepResult> {
	
	public StepResult process(JsonObject resultPropsObj){
		StepResultBuilder builder = null;
		StepResult outResult = null;

		try{
			builder = new StepResultBuilder();
			//Deserialize autoProps
			StepResultProperties resultProps = new StepResultProperties();
			processJsonObjectForEnumMap(resultPropsObj, resultProps);
	
			outResult = builder.resultProps(resultProps).build();
		} catch (Exception e){
			Console.displayExceptionBlock(e);
		}

		return outResult;		
	}
	
	@Override
	public StepResult deserialize(final JsonElement jsonElement, Type arg1, JsonDeserializationContext arg2) {
		JsonObject root = jsonElement.getAsJsonObject();
		return this.process(root);
	}

}
