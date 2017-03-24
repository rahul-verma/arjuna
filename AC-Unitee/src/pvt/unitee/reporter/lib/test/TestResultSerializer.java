package pvt.unitee.reporter.lib.test;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import pvt.unitee.reporter.lib.reportable.ResultSerializer;
import pvt.unitee.reporter.lib.step.StepResult;

public class TestResultSerializer extends ResultSerializer<TestResult> {

	protected void process(TestResult result, JsonObject jsonObject){
		try{
			serializeTestVariables(jsonObject, result.testVars());
			jsonObject.add("resultProps", serializeEnumKeyMap(result.resultProps().items()));
			JsonArray stepArray = new JsonArray();
			for (StepResult sr: result.stepResults()){
				stepArray.add(sr.asJsonObject());
			}
			jsonObject.add("steps", stepArray);
		} catch (Exception e){
			jsonObject.addProperty("rType", "Error in getting string representation");
			e.printStackTrace();
		}
	}	
}
