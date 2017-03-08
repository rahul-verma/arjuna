package com.autocognite.pvt.unitee.reporter.lib.reportable;

import java.util.List;
import java.util.Map;

import com.autocognite.arjuna.interfaces.TestObjectProperties;
import com.autocognite.arjuna.interfaces.TestProperties;
import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.pvt.arjuna.enums.TestAttribute;
import com.autocognite.pvt.arjuna.enums.TestObjectAttribute;
import com.autocognite.pvt.batteries.container.ReadOnlyContainer;

public class TestRelatedResult {
	private TestVariables testVars = null;
	
	public TestRelatedResult(TestVariables testVars) throws Exception{
		this.testVars = testVars;
	}
	
	public TestVariables testVars() throws Exception {
		return this.testVars;
	}
	
	public TestObjectProperties objectProps() throws Exception {
		return this.testVars.objectProps();
	}
	
	public TestProperties testProps() throws Exception {
		return this.testVars.testProps();
	}
	
	public ReadOnlyContainer<String, Value> customProps() throws Exception {
		return this.testVars.customProps();
	}
	
	public ReadOnlyContainer<String, Value> udv() throws Exception {
		return this.testVars.udv();
	}

	public void setTestVariables(TestVariables testVars) {
		this.testVars = testVars;
	}
	
	public List<String> objectPropStrings(List<TestObjectAttribute> props) throws Exception {
		return this.objectProps().strings(props);
	}
	
	public Map<String,String> objectPropStrItems(List<TestObjectAttribute> props) throws Exception {
		return this.objectProps().strItems(props);
	}
	
	public List<String> testPropStrings(List<TestAttribute> props) throws Exception {
		return this.testProps().strings(props);
	}
	
	public Map<String,String> testPropStrItems(List<TestAttribute> props) throws Exception {
		return this.testProps().strItems(props);
	}	
	
	public List<String> customPropStrings(List<String> props) throws Exception {
		return this.customProps().strings(props);
	}
	
	public Map<String,String> customPropStrItems(List<String> props) throws Exception {
		return this.customProps().strItems(props);
	}
}