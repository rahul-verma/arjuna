package com.autocognite.pvt.unitee.reporter.lib;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.pvt.arjuna.interfaces.InternalReportGenerator;
import com.autocognite.pvt.unitee.reporter.lib.generator.ActivityReportGenerator;
import com.autocognite.pvt.unitee.reporter.lib.generator.FixtureReportGenerator;
import com.autocognite.pvt.unitee.reporter.lib.generator.IssueReportGenerator;
import com.autocognite.pvt.unitee.reporter.lib.generator.TestReportGenerator;

public class CentralReportGenerator {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private List<InternalReportGenerator> generators = new ArrayList<InternalReportGenerator>();
	private String reportDir = null;
	
	TestReportGenerator executionGenerator = null;
	IssueReportGenerator issueGenerator = null;
	FixtureReportGenerator fixtureGenerator = null;
	ActivityReportGenerator activityGenerator = null;
	
	public CentralReportGenerator(){
	}
	
	public synchronized void addReportGenerator(InternalReportGenerator generator) throws Exception {
		generators.add(generator);
	}
	
	public void setUp() throws Exception{
		for (InternalReportGenerator generator: this.generators){
			generator.setUp();
		}
		executionGenerator = new TestReportGenerator(generators);
		issueGenerator = new IssueReportGenerator(generators);
		fixtureGenerator = new FixtureReportGenerator(generators);
		activityGenerator = new ActivityReportGenerator(generators); 
	}
	
	
	public void tearDown() throws Exception{
		for (InternalReportGenerator generator: this.generators){
			generator.tearDown();
		}
	}

	public void generate(){		
		executionGenerator.generate();
		issueGenerator.generate();
		fixtureGenerator.generate();
		activityGenerator.generate();
	}
}
