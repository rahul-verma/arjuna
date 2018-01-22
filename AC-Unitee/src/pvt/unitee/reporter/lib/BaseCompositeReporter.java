package pvt.unitee.reporter.lib;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.IgnoredTestStatus;
import pvt.unitee.enums.TestReportSection;
import pvt.unitee.enums.TestResultType;
import pvt.unitee.interfaces.InternalReportableObserver;
import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.fixture.FixtureResult;
import pvt.unitee.reporter.lib.ignored.IgnoredTest;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.step.StepResult;
import pvt.unitee.reporter.lib.test.TestResult;
import unitee.interfaces.Reporter;

public class BaseCompositeReporter extends BasePrivateCompositeReporter {	
	private Set<TestResultType> allowedRTypes = null;
	private Set<IgnoredTestStatus> allowedIgnoreRTypes = null;
	
	public BaseCompositeReporter(){
		super();
		this.allowedRTypes = ArjunaInternal.getReportableTestTypes();
		this.allowedIgnoreRTypes = ArjunaInternal.getReportableIgnoredTestTypes();		
	}

	@Override
	public synchronized void update(TestResult reportable) throws Exception {
		if (allowedRTypes.contains(reportable.resultProps().result())){
				super.update(reportable);
		}
	}

	@Override
	public synchronized void update(IgnoredTest reportable) throws Exception {
		if (allowedIgnoreRTypes.contains(reportable.resultProps().status())){
			this.getIgnoredTestObserver().update(reportable);
		}
	}

	protected void setTestResultObserver(InternalReportableObserver<TestResult> testResultObserver) {
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.TESTS)){
			super.setTestResultObserver(testResultObserver);
		}
	}

	protected void setIgnoredTestObserver(InternalReportableObserver<IgnoredTest> ignoredTestObserver) {
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.IGNORED_TESTS)){
			super.setIgnoredTestObserver(ignoredTestObserver);
		}
	}

	protected void setIssueObserver(InternalReportableObserver<Issue> issueObserver) {
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.ISSUES)){
			super.setIssueObserver(issueObserver);
		}
	}

	protected void setEventObserver(InternalReportableObserver<Event> eventObserver) {
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.EVENTS)){
			super.setEventObserver(eventObserver);
		}
	}

	protected void setFixtureResultObserver(InternalReportableObserver<FixtureResult> fixtureResultObserver) {
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.FIXTURES)){
			super.setFixtureResultObserver(fixtureResultObserver);
		}
	}

}
