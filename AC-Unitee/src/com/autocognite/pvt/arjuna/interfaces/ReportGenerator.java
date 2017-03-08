package com.autocognite.pvt.arjuna.interfaces;

import com.autocognite.pvt.unitee.reporter.lib.event.Event;
import com.autocognite.pvt.unitee.reporter.lib.fixture.FixtureResult;
import com.autocognite.pvt.unitee.reporter.lib.issue.Issue;
import com.autocognite.pvt.unitee.reporter.lib.test.TestResult;

public interface ReportGenerator {	
	void setUp() throws Exception;
	void tearDown() throws Exception;
	
	void update(TestResult reportable) throws Exception ;
	void update(Issue reportable) throws Exception ;
	void update(Event reportable) throws Exception ;
	void update(FixtureResult reportable) throws Exception;
}
