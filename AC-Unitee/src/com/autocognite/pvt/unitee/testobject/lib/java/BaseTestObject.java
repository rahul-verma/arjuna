package com.autocognite.pvt.unitee.testobject.lib.java;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.internal.arjuna.enums.TestObjectType;
import com.autocognite.pvt.arjuna.enums.TestResultCode;
import com.autocognite.pvt.unitee.core.lib.metadata.TestVarsHandler;
import com.autocognite.pvt.unitee.core.lib.testvars.InternalTestVariables;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestObject;

public abstract class BaseTestObject implements TestObject {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private String objectId = null;
	private TestObjectType objectType = null;
	private TestVarsHandler testVarsHandler = null;
	private String qualifiedName = null;
	private boolean excluded = false;
	private TestResultCode exType = null;
	private String exclusionDesc = null;
	private int issueId;
	
	private boolean notSelected = false;
	private TestResultCode notSelectedType = null;
	private String notSelectedDesc = null;
	
	private boolean skipped = false;
	private TestResultCode skipType = null;
	private String skipDesc = null;
	
	public BaseTestObject(String objectId, TestObjectType objectType) throws Exception{
		this.setObjectId(objectId);
		this.setObjectType(objectType);
	}

	public String getObjectId() {
		return objectId;
	}

	private void setObjectId(String objectId) {
		this.objectId = objectId;
	}

	public TestObjectType getObjectType() {
		return objectType;
	}

	private void setObjectType(TestObjectType objectType) {
		this.objectType = objectType;
	}

	public InternalTestVariables getTestVariables() {
		return testVarsHandler.getTestVariables();
	}

	protected void setTestVarsHandler(TestVarsHandler testVarsHandler) throws Exception {
		this.testVarsHandler = testVarsHandler;
		this.testVarsHandler.populate();
	}

	public String getQualifiedName() {
		return qualifiedName;
	}

	public void setQualifiedName(String qualifiedName) {
		this.qualifiedName = qualifiedName;
	}
	
	@Override
	public void markExcluded(TestResultCode exType, String desc, int issueId) {
		this.excluded = true;
		this.exType = exType;
		this.exclusionDesc = desc;
		this.issueId = issueId;
	}

	@Override
	public boolean wasExcluded() {
		return this.excluded;
	}

	@Override
	public TestResultCode getExclusionType() {
		return this.exType;
	}

	@Override
	public String getExclusionDesc() {
		return this.exclusionDesc;
	}

	@Override
	public int getExclusionIssueId() {
		return this.issueId;
	}

	@Override
	public void markUnSelected(TestResultCode type, String desc) {
		this.notSelected = true;
		this.notSelectedType = type;
		this.notSelectedDesc = desc;
	}

	@Override
	public boolean wasUnSelected() {
		return this.notSelected;
	}

	@Override
	public TestResultCode getUnSelectedType() {
		return this.notSelectedType;
	}

	@Override
	public String getUnSelectedDesc() {
		return this.notSelectedDesc;
	}
	
	@Override
	public void markSkipped(TestResultCode type, String desc) {
		this.skipped = true;
		this.skipType = type;
		this.skipDesc = desc;
	}

	@Override
	public boolean wasSkipped() {
		return this.skipped;
	}

	@Override
	public TestResultCode getSkipType() {
		return this.skipType;
	}

	@Override
	public String getSkipDesc() {
		return this.skipDesc;
	}
	
	public boolean shouldExecuteSetupSessionFixture(){
		return !(this.excluded || this.notSelected || this.skipped);
	}
	
	public boolean shouldExecuteSetupClassFixture(){
		return !(this.excluded || this.notSelected || this.skipped);
	}

	public boolean shouldExecuteSetupClassInstanceFixture(){
		return !(this.excluded || this.notSelected || this.skipped);
	}
	
	public boolean shouldExecuteSetupClassFragmentFixture(){
		return !(this.excluded || this.notSelected || this.skipped);
	}
	
	public boolean shouldExecuteSetupMethodFixture(){
		return !(this.excluded || this.notSelected || this.skipped);
	}
	
	public boolean shouldExecuteSetupMethodInstanceFixture(){
		return !(this.excluded || this.notSelected || this.skipped);
	}
	
	public boolean shouldExecuteSetupTestFixture(){
		return !(this.excluded || this.notSelected || this.skipped);
	}
	
	@Override
	public void setThreadId(String id) throws Exception{
		this.getTestVariables().rawObjectProps().setThreadId(id);
	}
	
	@Override
	public void initTimeStamp() throws Exception {
		this.getTestVariables().rawObjectProps().setBeginTstamp();
	}

	@Override
	public void endTimeStamp() throws Exception {
		this.getTestVariables().rawObjectProps().setEndTstamp();
	}
}
