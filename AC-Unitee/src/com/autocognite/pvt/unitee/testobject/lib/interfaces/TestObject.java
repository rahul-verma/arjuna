package com.autocognite.pvt.unitee.testobject.lib.interfaces;

import com.autocognite.arjuna.enums.TestObjectType;
import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.pvt.arjuna.enums.TestResultCode;

public interface TestObject {
	
	TestVariables getTestVariablesDefinition();

	String getObjectId();

	String getQualifiedName();

	TestVariables getTestVariables();

	TestObjectType getObjectType();
	
	void markExcluded(TestResultCode exType, String desc, int issueId);
	
	boolean wasExcluded();
	
	TestResultCode getExclusionType();
	
	String getExclusionDesc();
	
	int getExclusionIssueId();

	void markUnSelected(TestResultCode type, String desc);

	boolean wasUnSelected();

	TestResultCode getUnSelectedType();

	String getUnSelectedDesc();
	
	void markSkipped(TestResultCode type, String desc);

	boolean wasSkipped();

	TestResultCode getSkipType();

	String getSkipDesc();

	void setThreadId(String id) throws Exception;
	
	void initTimeStamp() throws Exception;
	
	void endTimeStamp() throws Exception;

}
