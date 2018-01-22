package pvt.unitee.reporter.lib.writer.console;

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
import unitee.interfaces.Reporter;

public class ConsoleReporter extends BasePrivateCompositeReporter {
	
	public ConsoleReporter() throws Exception{
		this.setTestResultObserver(new ConsoleTestResultWriter());
		this.setEventObserver(new ConsoleEventWriter());
	}
}
