package pvt.unitee.testobject.lib.java;

import org.apache.log4j.Logger;

import pvt.batteries.config.Batteries;
import pvt.unitee.core.lib.metadata.TestVarsHandler;
import pvt.unitee.core.lib.testvars.InternalTestVariables;
import pvt.unitee.enums.FixtureResultType;
import pvt.unitee.enums.TestClassFixtureType;
import pvt.unitee.enums.TestResultCode;
import pvt.unitee.testobject.lib.fixture.Fixture;
import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.interfaces.TestObject;
import unitee.enums.TestObjectType;

public abstract class BaseTestObject implements TestObject {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
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
	
	private Fixture setUpFixture = null;
	private Fixture tearDownFixture = null;
	private TestResultCode ignoreExclusionCode = null;
	
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

	@Override
	public Fixture getSetUpFixture() throws Exception {
		return this.setUpFixture;
	}

	protected void setSetUpFixture(Fixture fixture) throws Exception {
		this.setUpFixture = fixture;
	}

	public Fixture getTearDownFixture() throws Exception {
		return this.tearDownFixture;
	}

	protected void setTearDownFixture(Fixture fixture) throws Exception {
		this.tearDownFixture = fixture;
	}
	
	protected void setIgnoreExclusionTestResultCode(TestResultCode code){
		this.ignoreExclusionCode = code;
	}
	
	protected TestResultCode getIgnoreExclusionTestResultCode(){
		return this.ignoreExclusionCode;
	}
	
	public boolean shouldExecuteSetUp(){
		return !(this.excluded || this.notSelected || this.skipped);
	}
	
	public boolean shouldExecuteTearDown(){
		if (this.wasUnSelected() || this.wasSkipped()){
			return false;
		} else if (this.wasExcluded() && (this.getExclusionType() != this.getIgnoreExclusionTestResultCode())){
			return false;
		}
		
		return true;
	}
	
	@Override
	public void setUp() throws Exception{
		if (this.getSetUpFixture() != null){
			boolean success = this.getSetUpFixture().execute();
			if (!success){
				this.markExcluded(
						this.getSetUpFixture().getTestResultCodeForFixtureError(),
						String.format("Error in \"%s.%s\" fixture", this.getSetUpFixture().getFixtureClassName(), this.getSetUpFixture().getName()),
						this.getSetUpFixture().getIssueId());
			}
		}
	}

	@Override
	public void tearDown() throws Exception {
		if (this.getTearDownFixture() != null){
			boolean success = getTearDownFixture().execute();
			if (!success){
				this.markExcluded(
						this.getTearDownFixture().getTestResultCodeForFixtureError(),
						String.format("Error in \"%s.%s\" fixture", this.getTearDownFixture().getFixtureClassName(), this.getTearDownFixture().getName()),
				this.getTearDownFixture().getIssueId());
			}
		}
	}
	
	@Override
	public boolean wasSetUpExecuted() throws Exception{
		if (this.getSetUpFixture() != null){
			return this.getSetUpFixture().wasExecuted();
		} else {
			return true;
		}
	}
	
	@Override
	public boolean wasTearDownExecuted() throws Exception{
		if (this.getTearDownFixture() != null){
			return this.getTearDownFixture().wasExecuted();
		} else {
			return true;
		}
	}
	
	@Override
	public boolean wasSetUpSuccessful() throws Exception{
		if (this.getSetUpFixture() != null){
			return this.getSetUpFixture().wasSuccessful();
		} else {
			return true;
		}
	}
	
	@Override
	public boolean wasTearDownSuccessful() throws Exception{
		if (this.getTearDownFixture() != null){
			return this.getTearDownFixture().wasSuccessful();
		} else {
			return true;
		}
	}
	
	@Override
	public FixtureResultType getSetUpResult() throws Exception {
		if (this.getSetUpFixture() != null){
			return this.getSetUpFixture().getResultType();
		} else {
			return FixtureResultType.SUCCESS;
		}
	}

	@Override
	public FixtureResultType getTearDownResult() throws Exception {
		if (this.getTearDownFixture() != null){
			return this.getTearDownFixture().getResultType();
		} else {
			return FixtureResultType.SUCCESS;
		}
	}
	
	protected void initFixtures(TestClassFixtureType sFixType, TestClassFixtureType tFixType) throws Exception{
		Fixture sFix = this.getTestFixtures().getFixture(sFixType);
		if (sFix != null){
			sFix.setTestObject(this);
			this.setSetUpFixture(sFix);
		}
		
		Fixture tFix = this.getTestFixtures().getFixture(tFixType);
		if (tFix != null){
			tFix.setTestObject(this);
			this.setTearDownFixture(tFix);	
		}
	}
	
	public abstract TestFixtures getTestFixtures();
	
	public boolean hasCompleted(){
		return true;
	}
	
	@Override
	public void populateUserProps() throws Exception {
		this.testVarsHandler.populateUserProps();
	}
}
