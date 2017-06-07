package pvt.unitee.interfaces;

import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.fixture.FixtureResult;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.test.TestResult;

public interface ReportGenerator {	
	void setUp() throws Exception;
	void tearDown() throws Exception;
	
	void update(TestResult reportable) throws Exception ;
	void update(Issue reportable) throws Exception ;
	void update(Event reportable) throws Exception ;
	void update(FixtureResult reportable) throws Exception;
}
