package com.autocognite.pvt.unitee.reporter.lib.test;

import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.pvt.arjuna.enums.TestResultAttribute;
import com.autocognite.pvt.arjuna.enums.TestResultCode;
import com.autocognite.pvt.arjuna.enums.TestResultType;
import com.autocognite.pvt.batteries.value.EnumValue;
import com.autocognite.pvt.batteries.value.IntValue;
import com.autocognite.pvt.batteries.value.StringValue;

public class TestResultBuilder {
	private TestResultProperties resultProps = new TestResultProperties();
	private TestVariables testVars = null;
	private Throwable e;

	public TestResultBuilder result(TestResultType type) throws Exception {
		this.resultProps.add(TestResultAttribute.RESULT, new EnumValue<TestResultType>(type));
		return this;
	}	

	public TestResultBuilder code(TestResultCode code) throws Exception {
		this.resultProps.add(TestResultAttribute.CODE, new EnumValue<TestResultCode>(code));
		return this;
	}	

	public TestResultBuilder desc(String desc) throws Exception {
		this.resultProps.add(TestResultAttribute.DESC, new StringValue(desc));
		return this;
	}		
	
	public TestResultBuilder issueId(int id) throws Exception {
		this.resultProps.add(TestResultAttribute.ISSUE_ID, new IntValue(id));
		return this;
	}	
	
	public TestResultBuilder testVariables(TestVariables vars){
		this.testVars = vars;
		return this;
	}
	
	public TestResultBuilder resultProps(TestResultProperties props){
		this.resultProps = props;
		return this;
	}

	public TestResult build() throws Exception {
		if (this.testVars == null){
			throw new Exception("You can not create a result object without test vars.");
		}
		else {
			TestResult result = new TestResult(this.resultProps, this.testVars);
			return result;
		}
	}
}
