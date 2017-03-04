package com.autocognite.pvt.unitee.reporter.lib;

import com.autocognite.pvt.arjuna.interfaces.InternlReportableObserver;
import com.autocognite.pvt.unitee.reporter.lib.event.Event;
import com.autocognite.pvt.unitee.reporter.lib.fixture.FixtureResult;
import com.autocognite.pvt.unitee.reporter.lib.issue.Issue;
import com.autocognite.pvt.unitee.reporter.lib.test.TestResult;

public interface Reporter {

	void update(TestResult reportable) throws Exception ;
	void update(Issue reportable) throws Exception ;
	void update(Event reportable) throws Exception;
	void update(FixtureResult reportable) throws Exception;

	void setUp();
	void tearDown() throws Exception;

	void addTestResultObserver(InternlReportableObserver<TestResult> observer) throws Exception;
	void addIssueObserver(InternlReportableObserver<Issue> observer) throws Exception;
	void addEventObserver(InternlReportableObserver<Event> observer) throws Exception;
	void addFixtureResultObserver(InternlReportableObserver<FixtureResult> observer) throws Exception;

}