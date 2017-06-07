/*******************************************************************************
 * Copyright 2015-16 AutoCognite Testing Research Pvt Ltd
 * 
 * Website: www.AutoCognite.com
 * Email: support [at] autocognite.com
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/
package pvt.unitee.lib.strings;

import java.util.ArrayList;

import pvt.batteries.ds.Name;
import pvt.batteries.ds.NamesContainer;
import pvt.unitee.enums.EventAttribute;
import pvt.unitee.enums.FixtureResultPropertyType;
import pvt.unitee.enums.IssueAttribute;
import pvt.unitee.enums.NamesContainerType;
import pvt.unitee.enums.StepResultAttribute;
import pvt.unitee.enums.TestResultAttribute;
import pvt.unitee.enums.UniteeComponent;
import unitee.enums.TestAttribute;
import unitee.enums.TestObjectAttribute;
import unitee.enums.TestObjectType;

public class UniteeNames {
	
	public static ArrayList<NamesContainer> getAllNames(){
		ArrayList<NamesContainer> containers = new ArrayList<NamesContainer>();
		
		NamesContainer testObjectProperties = new NamesContainer(NamesContainerType.TEST_OBJECT.toString());
		testObjectProperties.add(new Name(TestObjectAttribute.OTYPE.toString(), "Test Object Enum Type"));
		testObjectProperties.add(new Name(TestObjectAttribute.ONAME.toString(), "Test Object Type"));
		testObjectProperties.add(new Name(TestObjectAttribute.PNAME.toString(), "Test Package"));
		testObjectProperties.add(new Name(TestObjectAttribute.CNAME.toString(), "Test Class"));
		testObjectProperties.add(new Name(TestObjectAttribute.CIN.toString(), "Test Class Instance Number"));
		testObjectProperties.add(new Name(TestObjectAttribute.CFN.toString(), "Test Class Instance Fragment Number"));
		testObjectProperties.add(new Name(TestObjectAttribute.MNAME.toString(), "Test Method"));
		testObjectProperties.add(new Name(TestObjectAttribute.MIN.toString(), "Test Method Instance Number"));
		testObjectProperties.add(new Name(TestObjectAttribute.TN.toString(), "Test Number")); // E.g DDT
		testObjectProperties.add(new Name(TestObjectAttribute.SN.toString(), "Test Session Name"));
		testObjectProperties.add(new Name(TestObjectAttribute.NNAME.toString(), "Session Node Name"));
		testObjectProperties.add(new Name(TestObjectAttribute.NID.toString(), "Session Node Number"));
		testObjectProperties.add(new Name(TestObjectAttribute.SNID.toString(), "Session Sub Node Number"));
		testObjectProperties.add(new Name(TestObjectAttribute.GN.toString(), "Test Group Name"));
		testObjectProperties.add(new Name(TestObjectAttribute.BTSTAMP.toString(), "Begin Timestamp"));
		testObjectProperties.add(new Name(TestObjectAttribute.ETSTAMP.toString(), "End Timestamp"));
		testObjectProperties.add(new Name(TestObjectAttribute.TTIME.toString(), "Test Time (seconds)"));
		testObjectProperties.add(new Name(TestObjectAttribute.TID.toString(), "Execution Thread ID"));
		
		containers.add(testObjectProperties);
		
		NamesContainer testObjectTypeNames = new NamesContainer(NamesContainerType.TEST_OBJECT_TYPE_NAMES.toString());
		testObjectTypeNames.add(new Name(TestObjectType.TEST_CLASS.toString(), "Test Class"));
		testObjectTypeNames.add(new Name(TestObjectType.TEST_CLASS_INSTANCE.toString(), "Test Class Instance"));
		testObjectTypeNames.add(new Name(TestObjectType.TEST_CLASS_FRAGMENT.toString(), "Test Class Instance Fragment"));
		testObjectTypeNames.add(new Name(TestObjectType.TEST_METHOD.toString(), "Test Method"));
		testObjectTypeNames.add(new Name(TestObjectType.TEST_METHOD_INSTANCE.toString(), "Test Method Instance"));
		testObjectTypeNames.add(new Name(TestObjectType.TEST.toString(), "Test"));
		containers.add(testObjectTypeNames);

		NamesContainer testProperties = new NamesContainer(NamesContainerType.TEST.toString());		
		testProperties.add(new Name(TestAttribute.ID.toString(), "Test Id"));
		testProperties.add(new Name(TestAttribute.NAME.toString(), "Test Name"));
		testProperties.add(new Name(TestAttribute.IDEA.toString(), "Test Idea"));
		testProperties.add(new Name(TestAttribute.PRIORITY.toString(), "Test Priority"));
		containers.add(testProperties);	
		
		NamesContainer testResultProperties = new NamesContainer(NamesContainerType.TEST_RESULT.toString());
		testResultProperties.add(new Name(TestResultAttribute.RESULT.toString(), "Test Result"));
		testResultProperties.add(new Name(TestResultAttribute.CODE.toString(), "Result Code"));
		testResultProperties.add(new Name(TestResultAttribute.DESC.toString(), "Result Description"));
		testResultProperties.add(new Name(TestResultAttribute.ISSUE_ID.toString(), "Issue Id"));
		containers.add(testResultProperties);
		
		NamesContainer stepResultProperties = new NamesContainer(NamesContainerType.STEP_RESULT.toString());
		stepResultProperties.add(new Name(StepResultAttribute.RESULT.toString(), "Step Result"));
		stepResultProperties.add(new Name(StepResultAttribute.NUM.toString(), "Step Number"));
		stepResultProperties.add(new Name(StepResultAttribute.PURPOSE.toString(), "Step Purpose"));
		stepResultProperties.add(new Name(StepResultAttribute.CTEXT.toString(), "Check Text"));
		stepResultProperties.add(new Name(StepResultAttribute.CBENCH.toString(), "Check Benchmark"));
		stepResultProperties.add(new Name(StepResultAttribute.COBSERVE.toString(), "Actual Value/Observation"));
		stepResultProperties.add(new Name(StepResultAttribute.SCR.toString(), "Screenshot Paths"));
		stepResultProperties.add(new Name(StepResultAttribute.ISSUE_ID.toString(), "Issue Id"));
		containers.add(stepResultProperties);
		
		NamesContainer fixtureResultProperties = new NamesContainer(NamesContainerType.FIXTURE_RESULT.toString());
		fixtureResultProperties.add(new Name(FixtureResultPropertyType.RESULT.toString(), "Fixture Result"));
		fixtureResultProperties.add(new Name(FixtureResultPropertyType.FIXTURE_TYPE.toString(), "Fixture Type"));
		fixtureResultProperties.add(new Name(FixtureResultPropertyType.FIXTURE_METHOD.toString(), "Fixture Method"));
		fixtureResultProperties.add(new Name(FixtureResultPropertyType.EXEC_POINT.toString(), "Fixture Execution Point"));
		fixtureResultProperties.add(new Name(FixtureResultPropertyType.ISSUE_ID.toString(), "Fixture Issue Id"));
		containers.add(fixtureResultProperties);
		
		NamesContainer issueProps = new NamesContainer(NamesContainerType.ISSUE.toString());
		issueProps.add(new Name(IssueAttribute.STEP_NUM.toString(), "Test Step#"));
		issueProps.add(new Name(IssueAttribute.FNAME.toString(), "Fixture Method"));
		issueProps.add(new Name(IssueAttribute.DSNAME.toString(), "Data Source"));
		issueProps.add(new Name(IssueAttribute.ID.toString(), "Issue Id"));
		issueProps.add(new Name(IssueAttribute.TYPE.toString(), "Issue Type"));
		issueProps.add(new Name(IssueAttribute.SUB_TYPE.toString(), "Issue Sub-Type"));
		issueProps.add(new Name(IssueAttribute.ENAME.toString(), "Exception Name"));
		issueProps.add(new Name(IssueAttribute.EMSG.toString(), "Exception Message"));
		issueProps.add(new Name(IssueAttribute.ETRACE.toString(), "Exception Trace"));
		containers.add(issueProps);
		
		NamesContainer alertProps = new NamesContainer(NamesContainerType.EVENT.toString());	
		alertProps.add(new Name(EventAttribute.TEXT.toString(), "Event Message"));
		alertProps.add(new Name(EventAttribute.COMPONENT.toString(), "Component"));
		alertProps.add(new Name(EventAttribute.SUCCESS.toString(), "Successful?"));
		alertProps.add(new Name(EventAttribute.REMARKS.toString(), "Remarks"));
		alertProps.add(new Name(EventAttribute.EXC_MSG.toString(), "Exception Message"));
		alertProps.add(new Name(EventAttribute.EXC_TRACE.toString(), "Exception Trace"));
		containers.add(alertProps);	
		
		NamesContainer objectNames = new NamesContainer(NamesContainerType.COMPONENT_NAMES.toString());			
		objectNames.add(new Name(UniteeComponent.TEST_RUNNER.toString(), "Test Runner"));
		objectNames.add(new Name(UniteeComponent.TEST_FILTER.toString(), "Test Filter"));
		objectNames.add(new Name("TEST_REPORTER", "Test Reporter"));
		objectNames.add(new Name("TEST_RUNNER", "Test Runner"));
		containers.add(objectNames);		
		
		return containers;
	}
}
