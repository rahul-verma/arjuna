package pvt.unitee.reporter.lib.ignored;

import pvt.batteries.exceptions.Problem;
import pvt.batteries.utils.ExceptionBatteries;
import pvt.batteries.value.EnumValue;
import pvt.batteries.value.IntValue;
import pvt.batteries.value.StringValue;
import pvt.unitee.enums.IssueAttribute;
import pvt.unitee.enums.IssueSubType;
import pvt.unitee.enums.IssueType;
import pvt.unitee.enums.IgnoredTestReason;
import pvt.unitee.enums.IgnoredTestAttribute;
import pvt.unitee.enums.IgnoredTestStatus;
import pvt.unitee.enums.TestResultCode;
import pvt.unitee.enums.TestResultType;
import pvt.unitee.reporter.lib.test.TestResult;
import pvt.unitee.reporter.lib.test.TestResultProperties;
import pvt.unitee.validator.lib.exceptions.StepResultEvent;
import unitee.interfaces.TestVariables;

public class IgnoredTestBuilder {
	private IgnoredTestProperties resultProps = new IgnoredTestProperties();
	private TestVariables testVars = null;
	private Throwable e = null;

	public IgnoredTestBuilder status(IgnoredTestStatus type) throws Exception {
		this.resultProps.add(IgnoredTestAttribute.STATUS, new EnumValue<IgnoredTestStatus>(type));
		return this;
	}	

	public IgnoredTestBuilder reason(IgnoredTestReason code) throws Exception {
		this.resultProps.add(IgnoredTestAttribute.REASON, new EnumValue<IgnoredTestReason>(code));
		return this;
	}	

	public IgnoredTestBuilder desc(String desc) throws Exception {
		this.resultProps.add(IgnoredTestAttribute.DESC, new StringValue(desc));
		return this;
	}		

	public IgnoredTestBuilder testVariables(TestVariables vars){
		this.testVars = vars;
		return this;
	}
	
	public IgnoredTestBuilder resultProps(IgnoredTestProperties props){
		this.resultProps = props;
		return this;
	}

	public IgnoredTest build() throws Exception {
		if (this.testVars == null){
			throw new Exception("You can not create a result object without test vars.");
		}
		else {
			IgnoredTest result = new IgnoredTest(this.resultProps, this.testVars);
			return result;
		}
	}
}
