package pvt.unitee.reporter.lib.fixture;

import com.arjunapro.testauto.console.Console;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonObject;

import pvt.unitee.core.lib.testvars.InternalTestVariables;
import pvt.unitee.reporter.lib.reportable.ResultDeserializer;

public class FixtureResultDeserializer extends ResultDeserializer<FixtureResult> implements JsonDeserializer<FixtureResult> {
	
	public FixtureResult process(JsonObject root){
		FixtureResultBuilder builder = null;
		InternalTestVariables testVars = getTestVars(root);
		FixtureResult outResult = null;

		try{
			builder = new FixtureResultBuilder();

			//Deserialize autoProps
			JsonObject resultPropsObj = root.get("resultProps").getAsJsonObject();
			FixtureResultProperties resultProps = new FixtureResultProperties();
			processJsonObjectForEnumMap(resultPropsObj, resultProps);
	
			outResult = builder.resultProps(resultProps).testVariables(testVars).build();
		} catch (Exception e){
			Console.displayExceptionBlock(e);
		}

		return outResult;		
	}

}
