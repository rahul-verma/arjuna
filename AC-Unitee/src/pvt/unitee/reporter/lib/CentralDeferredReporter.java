package pvt.unitee.reporter.lib;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import pvt.batteries.config.Batteries;
import pvt.unitee.reporter.lib.generator.ActivityReportGenerator;
import pvt.unitee.reporter.lib.generator.FixtureReportGenerator;
import pvt.unitee.reporter.lib.generator.IgnoredTestReportGenerator;
import pvt.unitee.reporter.lib.generator.IssueReportGenerator;
import pvt.unitee.reporter.lib.generator.TestReportGenerator;
import unitee.interfaces.Reporter;

public class CentralDeferredReporter {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private List<Reporter> generators = new ArrayList<Reporter>();
	private String reportDir = null;
	
	TestReportGenerator executionGenerator = null;
	IgnoredTestReportGenerator ignoredGenerator = null;
	IssueReportGenerator issueGenerator = null;
	FixtureReportGenerator fixtureGenerator = null;
	ActivityReportGenerator activityGenerator = null;
	
	public CentralDeferredReporter(){
	}
	
	public synchronized void addReporter(Reporter generator) throws Exception {
		generators.add(generator);
	}
	
	public void setUp() throws Exception{
		for (Reporter generator: this.generators){
			generator.setUp();
		}
		executionGenerator = new TestReportGenerator(generators);
		ignoredGenerator = new IgnoredTestReportGenerator(generators);
		issueGenerator = new IssueReportGenerator(generators);
		fixtureGenerator = new FixtureReportGenerator(generators);
		activityGenerator = new ActivityReportGenerator(generators); 
	}
	
	
	public void tearDown() throws Exception{
		for (Reporter generator: this.generators){
			generator.tearDown();
		}
	}

	public void generate(){		
		issueGenerator.generate();
		executionGenerator.generate();
		ignoredGenerator.generate();
		fixtureGenerator.generate();
		activityGenerator.generate();
	}
}
