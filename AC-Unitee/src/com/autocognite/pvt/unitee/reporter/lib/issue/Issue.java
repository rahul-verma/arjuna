package com.autocognite.pvt.unitee.reporter.lib.issue;

import java.util.List;

import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.pvt.arjuna.enums.IssueAttribute;
import com.autocognite.pvt.unitee.reporter.lib.reportable.TestRelatedResult;
import com.google.gson.JsonObject;

public class Issue extends TestRelatedResult{
	IssueProperties resultProps = null;
	
	public Issue(
			IssueProperties resultProps,
			TestVariables testVars) throws Exception{
		super(testVars);
		this.resultProps = resultProps;
	}
	
	public IssueProperties resultProps(){
		return this.resultProps;
	}

	public List<String> resultPropStrings(List<IssueAttribute> props) throws Exception {
		return this.resultProps().strings(props);
	}
	
	public JsonObject asJsonObject() throws Exception{
		JsonObject obj =  new JsonObject();
		IssueSerializer serializer = new IssueSerializer();
		serializer.process(this, obj);
		return obj;
	}
}