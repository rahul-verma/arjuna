package pvt.unitee.reporter.lib.ignored;

import com.google.gson.JsonObject;

import arjunasdk.console.Console;
import pvt.unitee.reporter.lib.reportable.ResultSerializer;

public class IgnoredTestSerializer extends ResultSerializer<IgnoredTest> {

	protected void process(IgnoredTest result, JsonObject jsonObject){
		try{
			serializeTestVariables(jsonObject, result.testVars());
			jsonObject.add("resultProps", serializeEnumKeyMap(result.resultProps().items()));
		} catch (Exception e){
			jsonObject.addProperty("rType", "Error in getting string representation");
			Console.displayExceptionBlock(e);
		}
	}	
}
