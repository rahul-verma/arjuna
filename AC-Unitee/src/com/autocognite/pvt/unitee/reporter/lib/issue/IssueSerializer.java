package com.autocognite.pvt.unitee.reporter.lib.issue;

import com.autocognite.pvt.unitee.reporter.lib.reportable.ResultSerializer;
import com.google.gson.JsonObject;

public class IssueSerializer extends ResultSerializer<Issue> {

	protected void process(Issue result, JsonObject jsonObject){
		try{
			serializeTestVariables(jsonObject, result.testVars());
			jsonObject.add("resultProps", serializeEnumKeyMap(result.resultProps().items()));
		} catch (Exception e){
			jsonObject.addProperty("rType", "Error in getting string representation");
			e.printStackTrace();
		}
	}	
}
