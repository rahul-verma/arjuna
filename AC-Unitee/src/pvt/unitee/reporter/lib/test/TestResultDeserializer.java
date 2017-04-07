package pvt.unitee.reporter.lib.test;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import com.arjunapro.testauto.console.Console;
import com.google.gson.JsonArray;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import pvt.unitee.core.lib.testvars.InternalTestVariables;
import pvt.unitee.reporter.lib.reportable.ResultDeserializer;
import pvt.unitee.reporter.lib.step.StepResult;
import pvt.unitee.reporter.lib.step.StepResultDeserializer;

public class TestResultDeserializer extends ResultDeserializer<TestResult> implements JsonDeserializer<TestResult> {
	private static StepResultDeserializer deserializer = new StepResultDeserializer();
	
	public TestResult process(JsonObject root){
		TestResultBuilder builder = null;
		InternalTestVariables testVars = getTestVars(root);
		TestResult outResult = null;

		try{
			builder = new TestResultBuilder();

			//Deserialize autoProps
			JsonObject resultPropsObj = root.get("resultProps").getAsJsonObject();
			TestResultProperties resultProps = new TestResultProperties();
			processJsonObjectForEnumMap(resultPropsObj, resultProps);
			outResult = builder.resultProps(resultProps).testVariables(testVars).build();
			
			JsonArray stepArray = root.get("steps").getAsJsonArray();
			Iterator<JsonElement> iter = stepArray.iterator();
			List<StepResult> stepResults = new ArrayList<StepResult>();
			while(iter.hasNext()){
				stepResults.add(deserializer.process(iter.next().getAsJsonObject()));
			}
			
			outResult.addStepResults(stepResults);
						
		} catch (Exception e){
			Console.displayExceptionBlock(e);
		}

		return outResult;		
	}

}
