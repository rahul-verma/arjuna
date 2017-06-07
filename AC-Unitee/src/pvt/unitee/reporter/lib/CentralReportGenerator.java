package pvt.unitee.reporter.lib;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import pvt.batteries.config.Batteries;
import pvt.unitee.interfaces.ReportGenerator;
import pvt.unitee.reporter.lib.generator.ActivityReportGenerator;
import pvt.unitee.reporter.lib.generator.FixtureReportGenerator;
import pvt.unitee.reporter.lib.generator.IssueReportGenerator;
import pvt.unitee.reporter.lib.generator.TestReportGenerator;

public class CentralReportGenerator {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private List<ReportGenerator> generators = new ArrayList<ReportGenerator>();
	private String reportDir = null;
	
	TestReportGenerator executionGenerator = null;
	IssueReportGenerator issueGenerator = null;
	FixtureReportGenerator fixtureGenerator = null;
	ActivityReportGenerator activityGenerator = null;
	
	public CentralReportGenerator(){
	}
	
	public synchronized void addReportGenerator(ReportGenerator generator) throws Exception {
		generators.add(generator);
	}
	
	public void setUp() throws Exception{
		for (ReportGenerator generator: this.generators){
			generator.setUp();
		}
		executionGenerator = new TestReportGenerator(generators);
		issueGenerator = new IssueReportGenerator(generators);
		fixtureGenerator = new FixtureReportGenerator(generators);
		activityGenerator = new ActivityReportGenerator(generators); 
	}
	
	
	public void tearDown() throws Exception{
		for (ReportGenerator generator: this.generators){
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
