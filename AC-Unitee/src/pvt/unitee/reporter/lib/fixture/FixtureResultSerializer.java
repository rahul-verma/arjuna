package pvt.unitee.reporter.lib.fixture;

import com.arjunapro.testauto.console.Console;
import com.google.gson.JsonObject;

import pvt.unitee.reporter.lib.reportable.ResultSerializer;

public class FixtureResultSerializer extends ResultSerializer<FixtureResult> {

	protected void process(FixtureResult result, JsonObject jsonObject){
		try{
			serializeTestVariables(jsonObject, result.testVars());
			jsonObject.add("resultProps", serializeEnumKeyMap(result.resultProps().items()));
		} catch (Exception e){
			jsonObject.addProperty("rType", "Error in getting string representation");
			Console.displayExceptionBlock(e);
		}
	}	
}
