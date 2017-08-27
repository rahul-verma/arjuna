package unitee.steps;

import pvt.unitee.enums.StepResultType;
import pvt.unitee.validator.lib.check.DefaultStep;;

public class Steps {
	
	private static void step(StepResultType type, String purpose, String checkText, String benchmark, String observation, String excMessage) throws Exception{
		DefaultStep step = new DefaultStep();
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
		}
		
		step.evaluate();
	}
	
	
	public static void pass(String purpose) throws Exception{
		step(StepResultType.PASS, purpose, null, null, null, null);
	}
	
	public static void pass(String purpose, String checkText) throws Exception{
		step(StepResultType.PASS, purpose, checkText, null, null, null);
	}
	
	public static void pass(String purpose, String checkText, String benchmark, String actual) throws Exception{
		step(StepResultType.PASS, purpose, checkText, benchmark, actual, null);
	}
	
	public static void fail(String purpose) throws Exception{
		step(StepResultType.FAIL, purpose, null, null, null, null);
	}
	
	public static void fail(String purpose, String checkText) throws Exception{
		step(StepResultType.FAIL, purpose, checkText, null, null, null);
	}
	
	public static void fail(String purpose, String checkText, String excMessage) throws Exception{
		step(StepResultType.FAIL, purpose, checkText, null, null, excMessage);
	}
	
	public static void fail(String purpose, String checkText, String benchmark, String actual) throws Exception{
		step(StepResultType.FAIL, purpose, checkText, benchmark, actual, null);
	}
	
	public static void fail(String purpose, String checkText, String benchmark, String actual, String excMessage) throws Exception{
		step(StepResultType.FAIL, purpose, checkText, benchmark, actual, excMessage);
	}
	
	public static void error(String purpose) throws Exception{
		step(StepResultType.ERROR, purpose, null, null, null, null);
	}
	
	public static void error(String purpose, String excMessage) throws Exception{
		step(StepResultType.ERROR, purpose, null, null, null, excMessage);
	}
	
}
