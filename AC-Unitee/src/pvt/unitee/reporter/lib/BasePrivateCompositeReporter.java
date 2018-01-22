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

public class BasePrivateCompositeReporter implements Reporter {
	private InternalReportableObserver<TestResult> testResultObserver = null;
	private InternalReportableObserver<IgnoredTest> ignoredTestObserver = null;
	private InternalReportableObserver<Issue> issueObserver = null;
	private InternalReportableObserver<Event> eventObserver = null;
	private InternalReportableObserver<FixtureResult> fixtureResultObserver = null;	

	@Override
	public void setUp() throws Exception {
		if (getTestResultObserver() != null){
			getTestResultObserver().setUp();
		}
		if (getIgnoredTestObserver() != null){
			getIgnoredTestObserver().setUp();
		}
		if (getIssueObserver() != null){
			getIssueObserver().setUp();
		}
		if (getEventObserver() != null){
			getEventObserver().setUp();
		}
		if (getFixtureResultObserver() != null){
			getFixtureResultObserver().setUp();
		}
	}

	@Override
	public void tearDown() throws Exception {
		if (getTestResultObserver() != null){
			getTestResultObserver().tearDown();
		}
		if (getIgnoredTestObserver() != null){
			getIgnoredTestObserver().tearDown();
		}
		if (getIssueObserver() != null){
			getIssueObserver().tearDown();
		}
		if (getEventObserver() != null){
			getEventObserver().tearDown();
		}
		if (getFixtureResultObserver() != null){
			getFixtureResultObserver().tearDown();
		}
	}

	@Override
	public synchronized void update(TestResult reportable) throws Exception {
		if (getTestResultObserver() != null){
			getTestResultObserver().update(reportable);
		}
	}

	@Override
	public synchronized void update(IgnoredTest reportable) throws Exception {
		if (getIgnoredTestObserver() != null){
			this.getIgnoredTestObserver().update(reportable);
		}
	}

	@Override
	public synchronized void update(Issue reportable) throws Exception {
		if (getIssueObserver() != null){
			this.getIssueObserver().update(reportable);
		}
	}

	@Override
	public synchronized void update(Event reportable) throws Exception {
		if (getEventObserver() != null){
			this.getEventObserver().update(reportable);
		}
	}

	@Override
	public synchronized void update(FixtureResult reportable) throws Exception {
		if (getFixtureResultObserver() != null){
			this.getFixtureResultObserver().update(reportable);
		}
	}

	protected InternalReportableObserver<TestResult> getTestResultObserver() {
		return testResultObserver;
	}

	protected void setTestResultObserver(InternalReportableObserver<TestResult> testResultObserver) {
		this.testResultObserver = testResultObserver;
	}

	protected InternalReportableObserver<IgnoredTest> getIgnoredTestObserver() {
		return ignoredTestObserver;
	}

	protected void setIgnoredTestObserver(InternalReportableObserver<IgnoredTest> ignoredTestObserver) {
		this.ignoredTestObserver = ignoredTestObserver;
	}

	protected InternalReportableObserver<Issue> getIssueObserver() {
		return issueObserver;
	}

	protected void setIssueObserver(InternalReportableObserver<Issue> issueObserver) {
		this.issueObserver = issueObserver;
	}

	protected InternalReportableObserver<Event> getEventObserver() {
		return eventObserver;
	}

	protected void setEventObserver(InternalReportableObserver<Event> eventObserver) {
		this.eventObserver = eventObserver;
	}

	protected InternalReportableObserver<FixtureResult> getFixtureResultObserver() {
		return fixtureResultObserver;
	}

	protected void setFixtureResultObserver(InternalReportableObserver<FixtureResult> fixtureResultObserver) {
		this.fixtureResultObserver = fixtureResultObserver;
	}

}
