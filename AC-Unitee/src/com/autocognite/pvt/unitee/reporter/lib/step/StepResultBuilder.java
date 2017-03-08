package com.autocognite.pvt.unitee.reporter.lib.step;

import com.autocognite.arjuna.exceptions.Problem;
import com.autocognite.pvt.arjuna.enums.StepResultAttribute;
import com.autocognite.pvt.arjuna.enums.StepResultType;
import com.autocognite.pvt.batteries.value.EnumValue;
import com.autocognite.pvt.batteries.value.IntValue;
import com.autocognite.pvt.batteries.value.StringValue;
import com.autocognite.pvt.unitee.validator.lib.exceptions.StepResultEvent;

public class StepResultBuilder {
	private StepResultProperties resultProps = new StepResultProperties();
	private Throwable e = null;
	
	public StepResultBuilder result(StepResultType type) throws Exception {
		this.resultProps.add(StepResultAttribute.RESULT, new EnumValue<StepResultType>(type));
		return this;
	}	

	public StepResultBuilder number(int i) throws Exception {
		this.resultProps.add(StepResultAttribute.NUM, new IntValue(i));
		return this;
	}	

	public StepResultBuilder purpose(String purpose) throws Exception {
		this.resultProps.add(StepResultAttribute.PURPOSE, new StringValue(purpose));
		return this;
	}	
	
	public StepResultBuilder checkInfo(String checkText, String checkBenchmark, String checkObservation) throws Exception {
		this.resultProps.add(StepResultAttribute.CTEXT, new StringValue(checkText));
		this.resultProps.add(StepResultAttribute.CBENCH, new StringValue(checkBenchmark));
		this.resultProps.add(StepResultAttribute.COBSERVE, new StringValue(checkObservation));
		return this;
	}
	
	public StepResultBuilder stepEvent(StepResultEvent e) throws Exception{
		this.purpose(e.getPurpose());
		this.checkInfo(e.getCheckText(), e.getBenchmark(), e.getActualObservation());
		return this;
	}
	
	public StepResultBuilder problem(Problem e) throws Exception{
		this.purpose(e.getProblemText());
//		if (e.containsScreenshot()){
//		this.appendScreenshotPath(e.getScreenshotPath());
//	}
		return this;
	}
	
	public StepResultBuilder resultProps(StepResultProperties props){
		this.resultProps = props;
		return this;
	}

	public StepResult build() throws Exception {
		StepResult result = new StepResult(this.resultProps);
		if (e != null){
			result.resultProps().setException(this.e);
		}
		return result;
	}

	public StepResultBuilder issueId(int issueId) {
		resultProps.setIssueId(issueId);
		return this;
	}

	public StepResultBuilder stepNum(int stepNum) {
		resultProps.setStepNum(stepNum);
		return this;
	}
}
