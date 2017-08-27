package unitee.steps;

import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.StepResultType;
import pvt.unitee.validator.lib.check.DefaultStep;;

public class MTSteps {
	String parentTestThreadName = null;
	
	public MTSteps() throws Exception{
		if (!ArjunaInternal.getCentralExecState().getThreadState(parentTestThreadName).isTestThread()){
			throw new Exception("You can not declare a multi-threaded steps object outside of test context. Declare it either in setUpTest or test method.");
		}
		this.parentTestThreadName = Thread.currentThread().getName();
		
	}
	
	private void step(StepResultType type, String purpose, String checkText, String benchmark, String observation, String excMessage) throws Exception{
		DefaultStep step = new DefaultStep(this.parentTestThreadName);
		step.setPurpose(purpose);
		if (checkText != null){
			step.setText(checkText);
		}
		if ((benchmark != null) && (observation != null)){
			step.setBenchmark(benchmark);
			step.setActualObservation(observation);
		} else if ((benchmark == null) && (observation == null)){
			// do nothing
		} else {
			throw new Exception("Benchmark and Actual observation should be provided or ignored together.");
		}

		switch(type){
		case PASS:
			break;
		case FAIL:
			step.setFailure();
			break;
		case ERROR:
			step.setError();
			break;
		}
		
		if (excMessage != null){
			step.setExceptionMessage(excMessage);
		} else {
			switch(type){
			case FAIL:
				if (checkText == null){
					step.setExceptionMessage(String.format("Failure: %s", purpose));
				} else {
					step.setExceptionMessage(String.format("Failure: %s", checkText));
				}
				break;
			case ERROR:
				step.setExceptionMessage(String.format("Error: %s", purpose));
				break;
			}
		}		
		step.evaluate();
	}
	
	
	public void pass(String purpose) throws Exception{
		step(StepResultType.PASS, purpose, null, null, null, null);
	}
	
	public void pass(String purpose, String checkText) throws Exception{
		step(StepResultType.PASS, purpose, checkText, null, null, null);
	}
	
	public void pass(String purpose, String checkText, String benchmark, String actual) throws Exception{
		step(StepResultType.PASS, purpose, checkText, benchmark, actual, null);
	}
	
	public void fail(String purpose) throws Exception{
		step(StepResultType.FAIL, purpose, null, null, null, null);
	}
	
	public void fail(String purpose, String checkText) throws Exception{
		step(StepResultType.FAIL, purpose, checkText, null, null, null);
	}
	
	public void fail(String purpose, String checkText, String excMessage) throws Exception{
		step(StepResultType.FAIL, purpose, checkText, null, null, excMessage);
	}
	
	public void fail(String purpose, String checkText, String benchmark, String actual) throws Exception{
		step(StepResultType.FAIL, purpose, checkText, benchmark, actual, null);
	}
	
	public void fail(String purpose, String checkText, String benchmark, String actual, String excMessage) throws Exception{
		step(StepResultType.FAIL, purpose, checkText, benchmark, actual, excMessage);
	}
	
	public void error(String purpose) throws Exception{
		step(StepResultType.ERROR, purpose, null, null, null, null);
	}
	
	public void error(String purpose, String excMessage) throws Exception{
		step(StepResultType.ERROR, purpose, null, null, null, excMessage);
	}
	
}
