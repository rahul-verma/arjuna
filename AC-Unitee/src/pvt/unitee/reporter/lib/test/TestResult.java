package pvt.unitee.reporter.lib.test;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

import com.arjunapro.testauto.config.RunConfig;
import com.arjunapro.testauto.interfaces.TestVariables;
import com.google.gson.JsonObject;

import pvt.arjunapro.ArjunaInternal;
import pvt.arjunapro.enums.StepResultAttribute;
import pvt.arjunapro.enums.StepResultType;
import pvt.arjunapro.enums.TestResultAttribute;
import pvt.arjunapro.enums.TestResultCode;
import pvt.arjunapro.enums.TestResultType;
import pvt.unitee.reporter.lib.reportable.TestRelatedResult;
import pvt.unitee.reporter.lib.step.StepResult;

public class TestResult extends TestRelatedResult {
	private static Logger logger = RunConfig.logger();
	private TestResultProperties resultProps = null;
	private List<StepResult> stepResults = new ArrayList<StepResult>();
	
	public TestResult(
			TestResultProperties resultProps,
			TestVariables testVars) throws Exception{
		super(testVars);
		this.resultProps = resultProps;
	}
	
	public TestResultProperties resultProps(){
		return this.resultProps;
	}
	
	public List<String> resultPropStrings(List<TestResultAttribute> props) throws Exception {
		return this.resultProps().strings(props);
	}
	
	public Map<String,String> resultPropStrItems(List<TestResultAttribute> props) throws Exception {
		return this.resultProps().strItems(props);
	}
	
	public JsonObject asJsonObject() throws Exception{
		JsonObject obj =  new JsonObject();
		TestResultSerializer serializer = new TestResultSerializer();
		serializer.process(this, obj);
		return obj;
	}
	
	public void addStepResults(List<StepResult> stepResults){
		this.stepResults.addAll(stepResults);
	}
	
	public List<StepResult> stepResults(){
		return this.stepResults;
	}
	
	private static void updatePassInfo(TestResultProperties testProps) throws Exception{
		testProps.setResult(TestResultType.PASS);
		testProps.setResultCode(TestResultCode.ALL_STEPS_PASS);
		testProps.setDescription("Passed");
	}
	
	@SuppressWarnings("incomplete-switch")
	private void updateResult(StepResult stepResult, TestResultType type, TestResultCode code) throws Exception{
		resultProps.setResult(type);
		resultProps.setResultCode(code);
		resultProps.setIssueId(stepResult.issueId());
		switch (type){
		case PASS: 	resultProps.setDescription("Passed");
		break;
		case FAIL:	resultProps.setDescription(String.format("Failure in Test Step: %d.", stepResult.resultProps().stepId()));
		break;
		case ERROR: resultProps.setDescription(String.format("Error in Test Step: %d.", stepResult.resultProps().stepId()));
		break;
		}
	}

	@SuppressWarnings("incomplete-switch")
	public void buildFromStepResults(List<StepResult> stepResults) throws Exception{
		this.addStepResults(stepResults);
		if (ArjunaInternal.displayReportProcessingInfo){
			logger.debug("Now processing test result for " +  this.objectProps().qualifiedName());
		}

		// Flag to check whether the result is updated because of a check issue. 
		// Useful when check error overrides fixture error.
		boolean checkIssue = false;

		if (stepResults.size() == 0){
			updatePassInfo(resultProps);
			return;
		}
		

		for (StepResult stepResult: stepResults){
			StepResultType stepResultType = stepResult.resultProps().value(StepResultAttribute.RESULT).asEnum(StepResultType.class);
			if (ArjunaInternal.displayReportProcessingInfo){
				logger.debug("Result Type: " + stepResultType);
			}
			
			switch(stepResultType){
			case PASS:
				if (resultProps.result() == null){
					updateResult(stepResult, TestResultType.PASS, TestResultCode.ALL_STEPS_PASS);
				}
				break;
			case ERROR:
				if ((resultProps.result() == null)|| (resultProps.result() == TestResultType.PASS) || (!checkIssue)){
					checkIssue = true;
					updateResult(stepResult, TestResultType.ERROR, TestResultCode.STEP_ERROR);
				}
				break;
			case FAIL:
				if ((resultProps.result() == null) || (!checkIssue)){
					checkIssue = true;
					updateResult(stepResult, TestResultType.FAIL, TestResultCode.STEP_FAILURE);
				}	
				break;
			}

//			ArrayList<String> sPaths = stepResult.getScreenshotPaths();
//			if(sPaths != null){
//				result.getScreenshotPaths().addAll(sPaths);
//			}
		}
	}

}