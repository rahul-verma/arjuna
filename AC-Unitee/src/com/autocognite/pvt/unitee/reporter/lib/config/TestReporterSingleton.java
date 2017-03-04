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
package com.autocognite.pvt.unitee.reporter.lib.config;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.autocognite.batteries.config.RunConfig;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.arjuna.enums.EventAttribute;
import com.autocognite.pvt.arjuna.enums.FixtureResultPropertyType;
import com.autocognite.pvt.arjuna.enums.IssueAttribute;
import com.autocognite.pvt.arjuna.enums.ReportMode;
import com.autocognite.pvt.arjuna.enums.StepResultAttribute;
import com.autocognite.pvt.arjuna.enums.TestAttribute;
import com.autocognite.pvt.arjuna.enums.TestObjectAttribute;
import com.autocognite.pvt.arjuna.enums.TestReportSection;
import com.autocognite.pvt.arjuna.enums.TestResultAttribute;
import com.autocognite.pvt.arjuna.enums.TestResultType;

public enum TestReporterSingleton {
	INSTANCE;
	
	private Map<TestObjectAttribute, String> testObjectPropNamesMap = new HashMap<TestObjectAttribute, String>();
	private Map<TestAttribute, String> testPropNamesMap = new HashMap<TestAttribute, String>();
	private Map<TestResultAttribute, String> testResultPropNamesMap = new HashMap<TestResultAttribute, String>();
	private Map<StepResultAttribute, String> stepResultPropNamesMap = new HashMap<StepResultAttribute, String>();
	private Map<IssueAttribute, String> issuePropNamesMap = new HashMap<IssueAttribute, String>();
	private Map<FixtureResultPropertyType, String> fixtureResultPropNamesMap = new HashMap<FixtureResultPropertyType, String>();
	private Map<EventAttribute, String> activityPropNamesMap = new HashMap<EventAttribute, String>();
	
	private List<TestObjectAttribute> execTestObjectPropsForTestReport = null;
	private List<TestObjectAttribute> execTestObjectPropsForStepReport = null;
	private List<TestObjectAttribute> execTestObjectPropsForIssueReport = null;
	private List<TestObjectAttribute> execTestObjectPropsForFixtureReport = null;
	private List<TestAttribute> execTestProps = null;
	private List<TestResultAttribute> execTestResultProps = null;
	private List<StepResultAttribute> execStepResultProps = null;
	private List<FixtureResultPropertyType> execFixtureResultProps = null;
	private List<IssueAttribute> execIssueProps = null;
	private List<EventAttribute> execActivityProps = null;
	
	private List<TestReportSection> allowedSections = new ArrayList<TestReportSection>();
	private Set<TestResultType> reportableTestResultTypes = new HashSet<TestResultType>();
	
	private boolean shouldIncludeAnnotatedTestProps = false;
	private boolean shouldIncludeCustomProps = false;
	private boolean shouldIncludeUdv = false;
	private boolean shouldIncludeDataRecord = false;
	private boolean shouldIncludeDataRef = false;
	
	public void init() throws Exception{
		for (TestObjectAttribute e: TestObjectAttribute.class.getEnumConstants()){
			testObjectPropNamesMap.put(e, ArjunaInternal.getTestObjectAttrName(e.toString()));
		}
		
		for (TestAttribute e: TestAttribute.class.getEnumConstants()){
			testPropNamesMap.put(e, ArjunaInternal.getTestAttrName(e.toString()));
		}
		
		for (TestResultAttribute e: TestResultAttribute.class.getEnumConstants()){
			testResultPropNamesMap.put(e, ArjunaInternal.getTestResultAttrName(e.toString()));
		}
		
		for (StepResultAttribute e: StepResultAttribute.class.getEnumConstants()){
			stepResultPropNamesMap.put(e, ArjunaInternal.getStepResultAttrName(e.toString()));
		}
		
		for (FixtureResultPropertyType e: FixtureResultPropertyType.class.getEnumConstants()){
			fixtureResultPropNamesMap.put(e, ArjunaInternal.getFixtureResultAttrName(e.toString()));
		}
		
		for (IssueAttribute e: IssueAttribute.class.getEnumConstants()){
			issuePropNamesMap.put(e, ArjunaInternal.getIssueAttrName(e.toString()));
		}
		
		for (EventAttribute e: EventAttribute.class.getEnumConstants()){
			activityPropNamesMap.put(e, ArjunaInternal.getEventAttrName(e.toString()));
		}
		
		execTestProps = RunConfig.value(ArjunaProperty.REPORT_METADATA_TEST).asEnumList(TestAttribute.class);
		execTestResultProps = RunConfig.value(ArjunaProperty.REPORT_TESTS_METADATA_REPORTABLE).asEnumList(TestResultAttribute.class);;
		execStepResultProps = RunConfig.value(ArjunaProperty.REPORT_STEPS_METADATA_REPORTABLE).asEnumList(StepResultAttribute.class);;
		execIssueProps = RunConfig.value(ArjunaProperty.REPORT_ISSUES_METADATA_REPORTABLE).asEnumList(IssueAttribute.class);;
		execFixtureResultProps = RunConfig.value(ArjunaProperty.REPORT_FIXTURES_METADATA_REPORTABLE).asEnumList(FixtureResultPropertyType.class);
		execActivityProps = RunConfig.value(ArjunaProperty.REPORT_EVENTS_METADATA_REPORTABLE).asEnumList(EventAttribute.class);;
				
		ReportMode mode = RunConfig.value(ArjunaProperty.REPORT_MODE).asEnum(ReportMode.class);
		
		switch (mode){
		case MINIMAL:
			execTestObjectPropsForTestReport = RunConfig.value(ArjunaProperty.REPORT_MINIMAL_METADATA_TEST_OBJECT_TESTS).asEnumList(TestObjectAttribute.class);
			execTestObjectPropsForStepReport = RunConfig.value(ArjunaProperty.REPORT_MINIMAL_METADATA_TEST_OBJECT_STEPS).asEnumList(TestObjectAttribute.class);;
			execTestObjectPropsForIssueReport = RunConfig.value(ArjunaProperty.REPORT_MINIMAL_METADATA_TEST_OBJECT_ISSUES).asEnumList(TestObjectAttribute.class);;
			execTestObjectPropsForFixtureReport = RunConfig.value(ArjunaProperty.REPORT_MINIMAL_METADATA_TEST_OBJECT_FIXTURES).asEnumList(TestObjectAttribute.class);;
			allowedSections.addAll(RunConfig.value(ArjunaProperty.REPORT_MINIMAL_SECTIONS).asEnumList(TestReportSection.class));
			reportableTestResultTypes.addAll(RunConfig.value(ArjunaProperty.REPORT_MINIMAL_INCLUDED_RTYPE).asEnumList(TestResultType.class));
			shouldIncludeAnnotatedTestProps = RunConfig.value(ArjunaProperty.REPORT_MINIMAL_TESTS_ANNOTATED_ON).asBoolean();
			shouldIncludeCustomProps = RunConfig.value(ArjunaProperty.REPORT_MINIMAL_TESTS_CUSTOM_ON).asBoolean();
			shouldIncludeUdv = RunConfig.value(ArjunaProperty.REPORT_MINIMAL_TESTS_UDV_ON).asBoolean();
			shouldIncludeDataRecord = RunConfig.value(ArjunaProperty.REPORT_MINIMAL_TESTS_DATARECORD_ON).asBoolean();
			shouldIncludeDataRef = RunConfig.value(ArjunaProperty.REPORT_MINIMAL_TESTS_DATAREF_ON).asBoolean();
			break;
		case BASIC:
			execTestObjectPropsForTestReport = RunConfig.value(ArjunaProperty.REPORT_BASIC_METADATA_TEST_OBJECT_TESTS).asEnumList(TestObjectAttribute.class);
			execTestObjectPropsForStepReport = RunConfig.value(ArjunaProperty.REPORT_BASIC_METADATA_TEST_OBJECT_STEPS).asEnumList(TestObjectAttribute.class);;
			execTestObjectPropsForIssueReport = RunConfig.value(ArjunaProperty.REPORT_BASIC_METADATA_TEST_OBJECT_ISSUES).asEnumList(TestObjectAttribute.class);;
			execTestObjectPropsForFixtureReport = RunConfig.value(ArjunaProperty.REPORT_BASIC_METADATA_TEST_OBJECT_FIXTURES).asEnumList(TestObjectAttribute.class);;
			allowedSections.addAll(RunConfig.value(ArjunaProperty.REPORT_BASIC_SECTIONS).asEnumList(TestReportSection.class));
			reportableTestResultTypes.addAll(RunConfig.value(ArjunaProperty.REPORT_BASIC_INCLUDED_RTYPE).asEnumList(TestResultType.class));
			shouldIncludeAnnotatedTestProps = RunConfig.value(ArjunaProperty.REPORT_BASIC_TESTS_ANNOTATED_ON).asBoolean();
			shouldIncludeCustomProps = RunConfig.value(ArjunaProperty.REPORT_BASIC_TESTS_CUSTOM_ON).asBoolean();
			shouldIncludeUdv = RunConfig.value(ArjunaProperty.REPORT_BASIC_TESTS_UDV_ON).asBoolean();
			shouldIncludeDataRecord = RunConfig.value(ArjunaProperty.REPORT_BASIC_TESTS_DATARECORD_ON).asBoolean();
			shouldIncludeDataRef = RunConfig.value(ArjunaProperty.REPORT_BASIC_TESTS_DATAREF_ON).asBoolean();
			break;
		case ADVANCED:
			execTestObjectPropsForTestReport = RunConfig.value(ArjunaProperty.REPORT_ADVANCED_METADATA_TEST_OBJECT_TESTS).asEnumList(TestObjectAttribute.class);
			execTestObjectPropsForStepReport = RunConfig.value(ArjunaProperty.REPORT_ADVANCED_METADATA_TEST_OBJECT_STEPS).asEnumList(TestObjectAttribute.class);;
			execTestObjectPropsForIssueReport = RunConfig.value(ArjunaProperty.REPORT_ADVANCED_METADATA_TEST_OBJECT_ISSUES).asEnumList(TestObjectAttribute.class);;
			execTestObjectPropsForFixtureReport = RunConfig.value(ArjunaProperty.REPORT_ADVANCED_METADATA_TEST_OBJECT_FIXTURES).asEnumList(TestObjectAttribute.class);;
			allowedSections.addAll(RunConfig.value(ArjunaProperty.REPORT_ADVANCED_SECTIONS).asEnumList(TestReportSection.class));
			reportableTestResultTypes.addAll(RunConfig.value(ArjunaProperty.REPORT_ADVANCED_INCLUDED_RTYPE).asEnumList(TestResultType.class));
			shouldIncludeAnnotatedTestProps = RunConfig.value(ArjunaProperty.REPORT_ADVANCED_TESTS_ANNOTATED_ON).asBoolean();
			shouldIncludeCustomProps = RunConfig.value(ArjunaProperty.REPORT_ADVANCED_TESTS_CUSTOM_ON).asBoolean();
			shouldIncludeUdv = RunConfig.value(ArjunaProperty.REPORT_ADVANCED_TESTS_UDV_ON).asBoolean();
			shouldIncludeDataRecord = RunConfig.value(ArjunaProperty.REPORT_ADVANCED_TESTS_DATARECORD_ON).asBoolean();
			shouldIncludeDataRef = RunConfig.value(ArjunaProperty.REPORT_ADVANCED_TESTS_DATAREF_ON).asBoolean();
			break;
		case DEBUG:
			execTestObjectPropsForTestReport = RunConfig.value(ArjunaProperty.REPORT_DEBUG_METADATA_TEST_OBJECT_TESTS).asEnumList(TestObjectAttribute.class);
			execTestObjectPropsForStepReport = RunConfig.value(ArjunaProperty.REPORT_DEBUG_METADATA_TEST_OBJECT_STEPS).asEnumList(TestObjectAttribute.class);;
			execTestObjectPropsForIssueReport = RunConfig.value(ArjunaProperty.REPORT_DEBUG_METADATA_TEST_OBJECT_ISSUES).asEnumList(TestObjectAttribute.class);;
			execTestObjectPropsForFixtureReport = RunConfig.value(ArjunaProperty.REPORT_DEBUG_METADATA_TEST_OBJECT_FIXTURES).asEnumList(TestObjectAttribute.class);;
			allowedSections.addAll(RunConfig.value(ArjunaProperty.REPORT_DEBUG_SECTIONS).asEnumList(TestReportSection.class));
			reportableTestResultTypes.addAll(RunConfig.value(ArjunaProperty.REPORT_DEBUG_INCLUDED_RTYPE).asEnumList(TestResultType.class));
			shouldIncludeAnnotatedTestProps = RunConfig.value(ArjunaProperty.REPORT_DEBUG_TESTS_ANNOTATED_ON).asBoolean();
			shouldIncludeCustomProps = RunConfig.value(ArjunaProperty.REPORT_DEBUG_TESTS_CUSTOM_ON).asBoolean();
			shouldIncludeUdv = RunConfig.value(ArjunaProperty.REPORT_DEBUG_TESTS_UDV_ON).asBoolean();
			shouldIncludeDataRecord = RunConfig.value(ArjunaProperty.REPORT_DEBUG_TESTS_DATARECORD_ON).asBoolean();
			shouldIncludeDataRef = RunConfig.value(ArjunaProperty.REPORT_DEBUG_TESTS_DATAREF_ON).asBoolean();
			break;
		default:
			break;
		}
		
	}
	
	public List<TestObjectAttribute> getTestObjectAttrListForTestReport(){
		return this.execTestObjectPropsForTestReport;
	}
	
	public List<TestObjectAttribute> getTestObjectAttrListForStepReport() {
		return this.execTestObjectPropsForStepReport;
	}
	
	public List<TestObjectAttribute> getTestObjectAttrListForIssueReport() {
		return this.execTestObjectPropsForIssueReport;
	}
	
	public List<TestObjectAttribute> getTestObjectAttrListForFixtureReport() {
		return this.execTestObjectPropsForFixtureReport;
	}
	
	public List<TestAttribute> getTestAttrList(){
		return this.execTestProps;
	}
	
	public List<TestResultAttribute> getTestResultAttrList(){
		return this.execTestResultProps;
	}
	
	public List<StepResultAttribute> getStepResultAttrList(){
		return this.execStepResultProps;
	}
	
	public List<FixtureResultPropertyType> getFixtureResultAttrList() {
		return this.execFixtureResultProps;
	}
	
	public List<IssueAttribute> getIssueAttrList(){
		return this.execIssueProps;
	}
	
	public List<EventAttribute> getEventAttrList(){
		return this.execActivityProps;
	}
	
	public List<TestReportSection> getReportSections(){
		return this.allowedSections;
	}
	
	public boolean shouldIncludedReportSection(TestReportSection section) {
		return this.allowedSections.contains(section);
	}
	
	public Set<TestResultType> getReportableTestTypes(){
		return this.reportableTestResultTypes;
	}
	
	public boolean isReportableResultType(TestResultType type){
		return this.reportableTestResultTypes.contains(type);
	}
	
	public boolean shouldIncludeAnnotatedTestPropsInReport(){
		return this.shouldIncludeAnnotatedTestProps;
	}
	
	public boolean shouldIncludeCustomPropsInReport(){
		return this.shouldIncludeCustomProps;
	}
	
	public boolean shouldIncludeUdvInReport(){
		return this.shouldIncludeUdv;
	}
	
	public boolean shouldIncludeDataRecordInReport(){
		return this.shouldIncludeDataRecord;
	}
	
	public boolean shouldIncludeDataRefInReport(){
		return this.shouldIncludeDataRef;
	}
	
	public Map<TestObjectAttribute, String> getTestObjectAttrNameMap(){
		return this.testObjectPropNamesMap;
	}
	
	public Map<TestAttribute, String> getTestAttrNameMap(){
		return this.testPropNamesMap;
	}
	
	public Map<TestResultAttribute, String> getTestResultAttrNameMap(){
		return this.testResultPropNamesMap;
	}
	
	public Map<StepResultAttribute, String> getStepResultAttrNameMap(){
		return this.stepResultPropNamesMap;
	}
	
	public Map<IssueAttribute, String> getIssueAttrNameMap(){
		return this.issuePropNamesMap;
	}
	
	public Map<FixtureResultPropertyType, String> getFixtureResultAttrNameMap(){
		return this.fixtureResultPropNamesMap;
	}
	
	public Map<EventAttribute, String> getEventAttrNameMap(){
		return this.activityPropNamesMap;
	}

}
