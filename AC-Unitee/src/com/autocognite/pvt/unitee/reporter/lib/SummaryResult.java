package com.autocognite.pvt.unitee.reporter.lib;

import java.util.HashMap;

import org.apache.log4j.Logger;

import com.autocognite.batteries.config.RunConfig;
import com.autocognite.pvt.arjuna.enums.TestResultType;

public class SummaryResult {
	private static Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private static HashMap<TestResultType, Integer> template = null;
	private HashMap<TestResultType, Integer> summary = new HashMap<TestResultType, Integer>();
	
	public static void init(){
		if (template == null){
			template = new HashMap<TestResultType, Integer>();
			for (TestResultType type: TestResultType.class.getEnumConstants()){
				template.put(type, 0);
			}
		}
			
	}
	
	public SummaryResult(){
		summary = (HashMap<TestResultType, Integer>) template.clone();
	}

	public void incrementCount(TestResultType type) {
		this.summary.put(type, this.summary.get(type) + 1);
	}

	public boolean succeeded() {
		return ((this.summary.get(TestResultType.PASS) > 0) &&
				(this.summary.get(TestResultType.FAIL) == 0) &&
				(this.summary.get(TestResultType.ERROR) == 0));
	}

}

