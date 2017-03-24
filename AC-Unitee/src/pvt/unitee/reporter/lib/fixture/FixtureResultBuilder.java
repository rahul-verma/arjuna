package pvt.unitee.reporter.lib.fixture;

import com.arjunapro.testauto.interfaces.TestVariables;

import pvt.arjunapro.enums.FixtureResultPropertyType;
import pvt.arjunapro.enums.FixtureResultType;
import pvt.arjunapro.enums.TestClassFixtureType;
import pvt.batteries.value.EnumValue;
import pvt.batteries.value.IntValue;
import pvt.batteries.value.StringValue;

public class FixtureResultBuilder {
	private FixtureResultProperties resultProps = new FixtureResultProperties();
	private TestVariables testVars = null;

	public FixtureResultBuilder result(FixtureResultType type) throws Exception {
		this.resultProps.add(FixtureResultPropertyType.RESULT, new EnumValue<FixtureResultType>(type));
		return this;
	}	

	public FixtureResultBuilder type(TestClassFixtureType type) throws Exception {
		this.resultProps.add(FixtureResultPropertyType.FIXTURE_TYPE, new EnumValue<TestClassFixtureType>(type));
		return this;
	}	

	public FixtureResultBuilder method(String name) throws Exception {
		this.resultProps.add(FixtureResultPropertyType.FIXTURE_METHOD, new StringValue(name));
		return this;
	}
	
	public FixtureResultBuilder execPoint(String execDesc) throws Exception {
		this.resultProps.add(FixtureResultPropertyType.EXEC_POINT, new StringValue(execDesc));
		return this;
	}
	
	public FixtureResultBuilder testVariables(TestVariables vars){
		this.testVars = vars;
		return this;
	}
	
	public FixtureResultBuilder resultProps(FixtureResultProperties props){
		this.resultProps = props;
		return this;
	}
	
	public FixtureResultBuilder issueId(int id) throws Exception {
		this.resultProps.add(FixtureResultPropertyType.ISSUE_ID, new IntValue(id));
		return this;
	}	

	public FixtureResult build() throws Exception {
		if (this.testVars == null){
			throw new Exception("You can not create a result object without test vars.");
		}
		else {
			return new FixtureResult(this.resultProps, this.testVars);
		}
	}
}
