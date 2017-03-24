package pvt.unitee.reporter.lib.issue;

import com.arjunapro.testauto.interfaces.TestVariables;

import pvt.arjunapro.enums.IssueAttribute;
import pvt.arjunapro.enums.IssueSubType;
import pvt.arjunapro.enums.IssueType;
import pvt.batteries.exceptions.Problem;
import pvt.batteries.utils.ExceptionBatteries;
import pvt.batteries.value.EnumValue;
import pvt.batteries.value.IntValue;
import pvt.batteries.value.StringValue;
import pvt.unitee.validator.lib.exceptions.StepResultEvent;

public class IssueBuilder {
	private IssueProperties resultProps = new IssueProperties();
	private TestVariables testVars = null;
	private Throwable e = null;

	public IssueBuilder id(int id) throws Exception {
		this.resultProps.add(IssueAttribute.ID, new IntValue(id));
		return this;
	}
	
	public IssueBuilder stepNum(int num) throws Exception {
		this.resultProps.add(IssueAttribute.STEP_NUM, new IntValue(num));
		return this;
	}
	
	public IssueBuilder fixtureName(String name) throws Exception {
		this.resultProps.add(IssueAttribute.FNAME, new StringValue(name));
		return this;
	}
	
	public IssueBuilder type(IssueType type) throws Exception {
		this.resultProps.add(IssueAttribute.TYPE, new EnumValue<IssueType>(type));
		return this;
	}	
	
	public IssueBuilder subType(IssueSubType type) throws Exception {
		this.resultProps.add(IssueAttribute.SUB_TYPE, new EnumValue<IssueSubType>(type));
		return this;
	}	

	public IssueBuilder message(String msg) throws Exception {
		this.resultProps.add(IssueAttribute.EMSG, new StringValue(msg));
		return this;
	}	

	public IssueBuilder trace(String trace) throws Exception {
		this.resultProps.add(IssueAttribute.ETRACE, new StringValue(trace));
		return this;
	}
	
	public IssueBuilder exception(Throwable e) throws Exception {
		this.resultProps.setExcName(e.getClass().getName());
		this.message(e.getMessage());
		this.trace(ExceptionBatteries.getStackTraceAsString(e));
		this.e = e;
		return this;
	}
	
	public IssueBuilder stepEvent(StepResultEvent e) throws Exception{
		this.exception(e);
		return this;
	}
	
	public IssueBuilder javaAssertionError(AssertionError e) throws Exception{
		this.message(e.getClass().getSimpleName() + ": " + e.getMessage());
		this.trace(ExceptionBatteries.getStackTraceAsString(e));
		this.e = e;
		return this;
	}
	
	public IssueBuilder problem(Problem e) throws Exception{
		StringBuilder sb = new StringBuilder();
		sb.append(e.getMessage());

		for(Throwable t: e.getChildThrowables()){
			sb.append(t.getMessage());
		}
		this.message(sb.toString());
		this.trace(ExceptionBatteries.getStackTraceAsString(e));
		this.e = e;
		return this;
	}
	
	public IssueBuilder testVariables(TestVariables vars){
		this.testVars = vars;
		return this;
	}
	
	public IssueBuilder resultProps(IssueProperties props){
		this.resultProps = props;
		return this;
	}

	public Issue build() throws Exception {
		if (this.testVars == null){
			throw new Exception("You can not create a result object without test vars.");
		}
		else {
			return new Issue(this.resultProps, this.testVars);
		}
	}
}
