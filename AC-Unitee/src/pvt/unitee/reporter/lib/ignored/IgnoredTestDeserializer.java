package pvt.unitee.reporter.lib.ignored;

import com.google.gson.JsonDeserializer;
import com.google.gson.JsonObject;

import arjunasdk.console.Console;
import pvt.unitee.core.lib.testvars.InternalTestVariables;
import pvt.unitee.reporter.lib.reportable.ResultDeserializer;

public class IgnoredTestDeserializer extends ResultDeserializer<IgnoredTest> implements JsonDeserializer<IgnoredTest> {
	
	public IgnoredTest process(JsonObject root){
		IgnoredTestBuilder builder = null;
		InternalTestVariables testVars = getTestVars(root);
		IgnoredTest outResult = null;

		try{
			builder = new IgnoredTestBuilder();

			//Deserialize autoProps
			JsonObject resultPropsObj = root.get("resultProps").getAsJsonObject();
			IgnoredTestProperties resultProps = new IgnoredTestProperties();
			processJsonObjectForEnumMap(resultPropsObj, resultProps);
	
			outResult = builder.resultProps(resultProps).testVariables(testVars).build();
		} catch (Exception e){
			Console.displayExceptionBlock(e);
		}

		return outResult;		
	}

}
