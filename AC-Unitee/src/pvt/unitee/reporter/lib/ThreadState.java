package pvt.unitee.reporter.lib;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.arjunapro.pvt.ArjunaInternal;

import pvt.arjunapro.enums.IssueSubType;
import pvt.arjunapro.enums.IssueType;
import pvt.arjunapro.enums.StepResultType;
import pvt.batteries.config.Batteries;
import pvt.batteries.exceptions.Problem;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.issue.IssueBuilder;
import pvt.unitee.reporter.lib.step.StepResult;
import pvt.unitee.reporter.lib.step.StepResultBuilder;
import pvt.unitee.testobject.lib.interfaces.Test;
import pvt.unitee.validator.lib.exceptions.Error;
import pvt.unitee.validator.lib.exceptions.Failure;

public class ThreadState {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private Test currentTest = null;
	private List<StepResult> currentStepResults =  null;
	
	public void beginTest(Test test){
		this.currentTest =  test;
		this.currentStepResults = new ArrayList<StepResult>();
	}

	public void endTest(){
		currentTest = null;
		currentStepResults =  null;
	}

	public Test getCurrentTest() throws Exception{
		return currentTest;
	}

	public List<StepResult> getCurrentTestStepResults() throws Exception{
		return currentStepResults;
	}
	
	public void addStepResult(StepResult stepResult) {
		currentStepResults.add(stepResult);
	}
	
	private synchronized int getStepId(){
		return currentStepResults.size() + 1;
	}

	public synchronized void addStepException(Throwable e) throws Exception{
//		logger.debug("Creating step result object");
		StepResult stepResult = createStepResultForException(getStepId(), e);
		addStepResult(stepResult);
	}

	public void addStepSuccess(
			String asserterClassName,
			String asserterMethodName,
			String assertionPurpose
			) throws Exception{
		StepResult stepResult = createPassStepResult(getStepId(), asserterClassName, asserterMethodName, assertionPurpose);
		addStepResult(stepResult);	
	}
	
	private StepResult createStepResultForException(int stepNum, Throwable e) throws Exception{
		try{
			throw e;
		}
		catch (Failure f) {
//			logger.debug("Test Fail Exception.");
			return createACFailure(stepNum, f);
		} catch (AssertionError f) {
//			logger.debug("Assertion Error Exception");
			return createXUnitFailStepResult(stepNum, f);	
		} catch (java.lang.reflect.InvocationTargetException g) {
			Throwable actualException = null;
			if (g.getTargetException().getCause() == null){
				actualException = g.getTargetException();
			} else {
				actualException = g.getTargetException().getCause();
			}
			if (actualException.getClass() == Failure.class) {
//				logger.debug("Test Fail Exception in Reflected Method.");
				return createACFailure(stepNum, (Failure) actualException);
			} else if (actualException.getClass().isAssignableFrom(AssertionError.class)) {
//				logger.debug("Assertion Error in Reflected Method.");
				return createXUnitFailStepResult(stepNum, (AssertionError) g.getTargetException());
			} else if (actualException.getClass() == Error.class) {
//				logger.debug("Test Error Exception in Reflected Method.");
				return createErrorStepResult(stepNum, (Error) g.getTargetException());
			} else if (actualException.getClass() == Problem.class) {
//				logger.debug("Problem Exception in Reflected Method.");
				return createProblemStepResult(stepNum, (Problem) g.getTargetException());
			} else if (actualException.getClass() == Exception.class){
//				logger.debug("Exception in Reflected Method.");
				return createJavaExceptionStepResult(stepNum, (Exception) g.getTargetException());
			}  else if (Throwable.class.isAssignableFrom(actualException.getClass())){
//				logger.debug("Java Error in Reflected Method.");
				return createJavaErrorStepResult(stepNum, (Throwable) g.getTargetException());
			} 
		} catch (Error h) {
//			logger.debug("Test Error Exception");
			return createErrorStepResult(stepNum, h);
		} catch (Problem h) {
//			logger.debug("Problem Exception");
			return createProblemStepResult(stepNum, h);
		} catch (Exception h) {
//			logger.debug("Exception");
			return createJavaExceptionStepResult(stepNum, h);
		} catch (Throwable h) {
//			logger.debug("Java Error");
			return createJavaErrorStepResult(stepNum, h);
		}
		
		return null;
	}
	
	private int createIssue(int stepNum, Throwable e, StepResultType rType) throws Exception{
		int issueId = ArjunaInternal.getCentralExecState().getIssueId();
		IssueBuilder builder = new IssueBuilder();
		Issue issue = builder
		.testVariables(this.currentTest.getTestVariables())
		.exception(e)
		.type(IssueType.TEST_STEP)
		.subType(getIssueSubTypeForStep(rType))
		.id(issueId)
		.stepNum(stepNum)
		.build();
		ArjunaInternal.getReporter().update(issue);		
		return issueId;
	}
	
	private IssueSubType getIssueSubTypeForStep(StepResultType stepResultType) throws Exception{
		switch (stepResultType){
		case ERROR:
			return IssueSubType.STEP_ERROR;
		case FAIL:
			return IssueSubType.STEP_FAILURE;
		}
		return null;
	}
	
	private StepResult createACFailure(int stepNum, Failure e) throws Exception{
		int issueId = createIssue(stepNum, e, StepResultType.FAIL);
		StepResultBuilder builder = new StepResultBuilder();
		
		return builder
		.stepEvent(e)
		.result(StepResultType.FAIL)
		.issueId(issueId)
		.stepNum(stepNum)
		.build();
	}
	
	private StepResult createXUnitFailStepResult(int stepNum, AssertionError e) throws Exception{
		int issueId = createIssue(stepNum, e, StepResultType.FAIL);
		StepResultBuilder builder = new StepResultBuilder();
		
		return builder
		.result(StepResultType.FAIL)
		.issueId(issueId)
		.stepNum(stepNum)
		.build();
	}
	
	private StepResult createErrorStepResult(int stepNum, Error e) throws Exception{
		int issueId = createIssue(stepNum, e, StepResultType.ERROR);
		StepResultBuilder builder = new StepResultBuilder();
		
		return builder
		.stepEvent(e)
		.result(StepResultType.ERROR)
		.issueId(issueId)
		.stepNum(stepNum)
		.build();
	}
	
	private StepResult createProblemStepResult(int stepNum, Problem e) throws Exception{
		int issueId = createIssue(stepNum, e, StepResultType.ERROR);
		StepResultBuilder builder = new StepResultBuilder();
		
		return builder
		.problem(e)
		.result(StepResultType.ERROR)
		.issueId(issueId)
		.stepNum(stepNum)
		.build();
	}
	
	private StepResult createJavaExceptionStepResult(int stepNum, Exception e) throws Exception{
		int issueId = createIssue(stepNum, e, StepResultType.ERROR);
		StepResultBuilder builder = new StepResultBuilder();
		
		return builder
		.result(StepResultType.ERROR)
		.issueId(issueId)
		.stepNum(stepNum)
		.build();
	}
	
	private StepResult createJavaErrorStepResult(int stepNum, Throwable e) throws Exception{
		int issueId = createIssue(stepNum, e, StepResultType.ERROR);
		StepResultBuilder builder = new StepResultBuilder();
		
		return builder
		.result(StepResultType.ERROR)
		.issueId(issueId)
		.stepNum(stepNum)
		.build();
	}
	
	private static StepResult createPassStepResult(
			int stepNum,
			String asserterClassName,
			String asserterMethodName,
			String assertionPurpose
			) throws Exception{
		StepResultBuilder builder = new StepResultBuilder();
		
		return builder
		.result(StepResultType.PASS)
		.stepNum(stepNum)
		.build();
	}
}
