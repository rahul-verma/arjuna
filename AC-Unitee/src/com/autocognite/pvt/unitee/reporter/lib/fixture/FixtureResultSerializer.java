package com.autocognite.pvt.unitee.reporter.lib.fixture;

import com.autocognite.pvt.unitee.reporter.lib.reportable.ResultSerializer;
import com.google.gson.JsonObject;

public class FixtureResultSerializer extends ResultSerializer<FixtureResult> {

	protected void process(FixtureResult result, JsonObject jsonObject){
		try{
			serializeTestVariables(jsonObject, result.testVars());
			jsonObject.add("resultProps", serializeEnumKeyMap(result.resultProps().items()));
		} catch (Exception e){
			jsonObject.addProperty("rType", "Error in getting string representation");
			e.printStackTrace();
		}
	}	
}
