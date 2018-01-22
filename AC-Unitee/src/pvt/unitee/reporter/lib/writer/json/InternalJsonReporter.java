package pvt.unitee.reporter.lib.writer.json;

import java.util.ArrayList;
import java.util.List;

import pvt.unitee.interfaces.InternalReportableObserver;
import pvt.unitee.reporter.lib.BasePrivateCompositeReporter;
import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.fixture.FixtureResult;
import pvt.unitee.reporter.lib.ignored.IgnoredTest;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.step.StepResult;
import pvt.unitee.reporter.lib.test.TestResult;
import pvt.unitee.reporter.lib.writer.console.ConsoleEventWriter;
import pvt.unitee.reporter.lib.writer.console.ConsoleTestResultWriter;
import unitee.interfaces.Reporter;

public class InternalJsonReporter extends BasePrivateCompositeReporter {
	
	public InternalJsonReporter() throws Exception{
		this.setTestResultObserver(new JsonTestResultWriter());
		this.setIgnoredTestObserver(new JsonIgnoredTestWriter());
		this.setIssueObserver(new JsonIssueWriter());
		this.setEventObserver(new JsonEventWriter());
		this.setFixtureResultObserver(new JsonFixtureResultWriter());		
	}
}
