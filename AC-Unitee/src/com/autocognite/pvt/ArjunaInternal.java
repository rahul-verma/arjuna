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
package com.autocognite.pvt;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.interfaces.DataSource;
import com.autocognite.arjuna.utils.console.Console;
import com.autocognite.internal.arjuna.enums.TestAttribute;
import com.autocognite.internal.arjuna.enums.TestObjectAttribute;
import com.autocognite.pvt.arjuna.enums.EventAttribute;
import com.autocognite.pvt.arjuna.enums.FixtureResultPropertyType;
import com.autocognite.pvt.arjuna.enums.IssueAttribute;
import com.autocognite.pvt.arjuna.enums.NamesContainerType;
import com.autocognite.pvt.arjuna.enums.StepResultAttribute;
import com.autocognite.pvt.arjuna.enums.TestReportSection;
import com.autocognite.pvt.arjuna.enums.TestResultAttribute;
import com.autocognite.pvt.arjuna.enums.TestResultType;
import com.autocognite.pvt.batteries.cli.CLIConfigurator;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.batteries.ds.NamesContainer;
import com.autocognite.pvt.unitee.config.ArjunaSingleton;
import com.autocognite.pvt.unitee.lib.engine.TestEngine;
import com.autocognite.pvt.unitee.lib.strings.UniteeNames;
import com.autocognite.pvt.unitee.reporter.lib.CentralExecutionState;
import com.autocognite.pvt.unitee.reporter.lib.Reporter;
import com.autocognite.pvt.unitee.reporter.lib.config.TestReporterSingleton;
import com.autocognite.pvt.unitee.testobject.lib.loader.group.TestGroupsDB;
import com.autocognite.pvt.unitee.testobject.lib.loader.session.Session;

public class ArjunaInternal {
	private static Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	public static boolean displayReportPrepInfo = false;
	public static boolean displayDiscoveryInfo = false;
	public static boolean displayLoadingInfo = false;
	public static boolean displayDefProcessingInfo = false;
	public static boolean displayExecTreeLoadingInfo = false;
	public static boolean displayFixtureProcessingInfo = false;
	public static boolean logFixtureExecutionInfo = false;
	public static boolean displayInstanceProcessingInfo = false;
	public static boolean displayUTVProcessingInfo = false;
	public static boolean displayTestObjConstructionInfo = false;
	public static boolean logPropInfo = true;
	public static boolean logTestExceptionTraces = false;
	public static boolean displayDependencyDefInfo = false;
	public static boolean logIgnoreDepInfo = false;
	public static boolean logDependencyExecResolutionInfo = false;
	public static boolean logDependencyMetInfo = false;
	public static boolean displayDummiesLoadingInfo = false;
	public static boolean displaySlotsInfo = false;
	public static boolean displayReportProcessingInfo = false;
	public static boolean displayReportGenerationInfo = false;
	public static boolean logFixtureError = false;
	public static boolean logJsonSerializationInfo = false;
	public static boolean logJsonDeserializationInfo = false;
	
	public static boolean displayDataMethodProcessingInfo = false;
	
	public static boolean displayFixtureExecInfo = false;
	public static boolean displayObserverSetUpInfo = false;
	public static boolean displayObserverUpdateInfo = false;
	public static boolean displayUserTestLoadingInfo = false;
	public static boolean logExclusionInfo = false;
	public static boolean centralStateUpdateInfo = false;
	
	private static boolean setupsuccessful = false;
	private static boolean runSuccessful = false;
	private static boolean tearDownSuccessful = false;
	
	public static void setCliConfigurator(CLIConfigurator cliConfigurator){
		ArjunaSingleton.INSTANCE.setCliConfigurator(cliConfigurator);
	}
	
	public static void init(String[] args) throws Exception{
		ArjunaSingleton.INSTANCE.printUniteeHeader();
		ArjunaSingleton.INSTANCE.setCliArgs(args);
		ArjunaSingleton.INSTANCE.init();
		ArjunaSingleton.INSTANCE.freeze();
		logger = Logger.getLogger(Batteries.getCentralLogName());
	}
	
	public static Map<TestObjectAttribute, String> getTestObjectAttrNameMap(){
		return TestReporterSingleton.INSTANCE.getTestObjectAttrNameMap();
	}
	
	public static Map<TestAttribute, String> getTestAttrNameMap(){
		return TestReporterSingleton.INSTANCE.getTestAttrNameMap();
	}
	
	public static Map<TestResultAttribute, String> getTestResultAttrNameMap(){
		return TestReporterSingleton.INSTANCE.getTestResultAttrNameMap();
	}
	
	public static Map<StepResultAttribute, String> getStepResultAttrNameMap(){
		return TestReporterSingleton.INSTANCE.getStepResultAttrNameMap();
	}
	
	public static Map<IssueAttribute, String> getIssueAttrNameMap(){
		return TestReporterSingleton.INSTANCE.getIssueAttrNameMap();
	}
	
	
	public static Map<FixtureResultPropertyType, String> getFixtureResultAttrNameMap(){
		return TestReporterSingleton.INSTANCE.getFixtureResultAttrNameMap();
	}
	
	public static Map<EventAttribute, String> getEventAttrNameMap(){
		return TestReporterSingleton.INSTANCE.getEventAttrNameMap();
	}
	
	public static String getTestObjectTypeName(String name) throws Exception {
		return Batteries.getConfiguredName(NamesContainerType.TEST_OBJECT_TYPE_NAMES.toString(), name);
	}
	
	public static String getTestObjectAttrName(String name) throws Exception {
		return Batteries.getConfiguredName(NamesContainerType.TEST_OBJECT.toString(), name);
	}
	
	public static String getTestAttrName(String name) throws Exception{
		return Batteries.getConfiguredName(NamesContainerType.TEST.toString(), name);
	}
	
	public static String getStepResultAttrName(String name) throws Exception{
		return Batteries.getConfiguredName(NamesContainerType.STEP_RESULT.toString(), name);
	}
	
	public static String getTestResultAttrName(String name) throws Exception{
		return Batteries.getConfiguredName(NamesContainerType.TEST_RESULT.toString(), name);
	}
	
	public static String getExcludedTestResultAttrName(String name) throws Exception{
		return Batteries.getConfiguredName(NamesContainerType.EXCLUDED_TEST_RESULT.toString(), name);
	}
	
	public static String getIssueAttrName(String name) throws Exception{
		return Batteries.getConfiguredName(NamesContainerType.ISSUE.toString(), name);
	}
	
	public static String getFixtureResultAttrName(String name) throws Exception{
		return Batteries.getConfiguredName(NamesContainerType.FIXTURE_RESULT.toString(), name);
	}
	
	public static String getEventAttrName(String name) throws Exception{
		return Batteries.getConfiguredName(NamesContainerType.EVENT.toString(), name);
	}
	
	public static ArrayList<NamesContainer> getAllNames(){
		return UniteeNames.getAllNames();
	}
	
	public static void processNonTestClass(Class<?> klass) throws Exception {
		ArjunaSingleton.INSTANCE.processNonTestClass(klass);
	}
	
	public static Method getDataGeneratorMethod(String containerName, String dgName) throws Exception {
		return ArjunaSingleton.INSTANCE.getDataGeneratorMethod(containerName, dgName);
	}
	
	public static Method getDataGeneratorMethod(Class<?> containerClass, String dgName) throws Exception {
		return ArjunaSingleton.INSTANCE.getDataGeneratorMethod(containerClass, dgName);
	}
	
	public static DataSource getDataSourceFromDataGenName(String dataGenName) throws Exception {
		return ArjunaSingleton.INSTANCE.getDataSourceFromDataGenName(dataGenName);
	}
	
	public static Reporter getReporter(){
		return ArjunaSingleton.INSTANCE.getReporter();
	}
	
	public static CentralExecutionState getCentralExecState(){
		return ArjunaSingleton.INSTANCE.getCentralExecState();
	}
	
	public static class problem{
		public static final String REPORT_WRONG_FORMAT = "problem.report.wrong.format";
	}
	
	private static boolean headerPrinted = false;
	
	public static void execute(TestEngine tee){
		try{
			logger.debug("Setting up Test Engine");
			tee.setUp();
			setupsuccessful = true;
		} catch (Throwable e){
			e.printStackTrace();
			setupsuccessful = false;
			Console.display("Critical: Exception in Test Engine set up.");
			Console.displayExceptionBlock(e);
			Console.display("Would attempt Test engine teardown before exiting.");
		}
		
		if (setupsuccessful){
			ArjunaInternal.discover(tee);
			ArjunaInternal.loadSession(tee);
			ArjunaInternal.initReporter(tee);
			ArjunaInternal.run(tee);
		}
		
		ArjunaInternal.report(tee);
		
		try {
			logger.debug("Tearing down Test Engine");
			tee.tearDown();
			tearDownSuccessful = true;
		} catch (Throwable e){
			tearDownSuccessful = false;
			Console.display("Critical: Exception in Test Engine tear down.");
			Console.displayExceptionBlock(e);
		}
		
		Console.display("All Done. Exiting.");
		if ((!runSuccessful) || (!tearDownSuccessful)){
			System.exit(1);
		}
		System.exit(0);		
	}
	
	public static String getVersion() {
		return ArjunaSingleton.INSTANCE.getVersion();
	}
	
	public static class info{
		public static final String EXIT_ON_ERROR = "message.exit.on.error";
		public static final String RUN_BEGIN = "message.run.begin";
		public static final String RUN_FINISH = "message.run.finish";
		public static final String PRINT_CONFIGURATION = "message.print.configuration";
		public static final String TEST_DISCOVERY_START = "message.test.discovery.start";
		public static final String TEST_DISCOVERY_FINISH = "message.test.discovery.finish";
		public static final String TESTRUNNER_CREATE_START = "message.testrunner.create.start";
		public static final String TESTRUNNER_CREATE_FINISH = "message.testrunner.create.finish";
		public static final String TESTREPORTER_CREATE_START = "message.testreporter.create.start";
		public static final String TESTREPORTER_CREATE_FINISH = "message.testreporter.create.finish";
		public static final String ALLOWED_REPORT_FORMATS = "message.reporter.allowed.formats";
	}
	
	public static void discover(TestEngine tee){
		try{
			logger.debug("Loading test definitions...");
			tee.discover();
			runSuccessful = true;
		} catch (Throwable e){
			runSuccessful = false;
			Console.display("Critical: Exception in Test Engine run.");
			Console.displayExceptionBlock(e);
			Console.display("Exiting...");
			System.exit(1);
		}
	}
	
	public static void initReporter(TestEngine tee) {
		try{
			logger.debug("Running Test Engine");
			tee.initReporter();
		} catch (Throwable e){
			e.printStackTrace();
			runSuccessful = false;
			Console.display("Critical: Exception in Test Engine run.");
			Console.displayExceptionBlock(e);
			Console.display("Would attempt Test engine teardown before exiting.");
		}
	}
	
	public static void report(TestEngine tee) {
		try{
			logger.debug("Generating reports");
			tee.report();
		} catch (Throwable e){
			e.printStackTrace();
			runSuccessful = false;
			Console.display("Critical: Exception in Test Engine run.");
			Console.displayExceptionBlock(e);
			Console.display("Would attempt Test engine teardown before exiting.");
		}
	}
	
	public static void loadSession(TestEngine tee) {
		try{
			logger.debug("Loading session...");
			ArjunaSingleton.INSTANCE.loadSession();
		} catch (Throwable e){
			runSuccessful = false;
			Console.display("Critical: Exception in Test Engine run.");
			e.printStackTrace();
			Console.displayExceptionBlock(e);
			Console.display("Would attempt Test engine teardown before exiting.");
		}
	}
	
	public static void run(TestEngine tee) {
		try{
			logger.debug("Running Test Engine");
			tee.run();
		} catch (Throwable e){
			runSuccessful = false;
			Console.display("Critical: Exception in Test Engine run.");
			Console.displayExceptionBlock(e);
			Console.display("Would attempt Test engine teardown before exiting.");
		}
	}

	public static TestGroupsDB getGroupLoader() {
		return ArjunaSingleton.INSTANCE.getTestGroupDB();
	}
	
	public static List<TestObjectAttribute> getTestObjectAttrListForTestReport(){
		return TestReporterSingleton.INSTANCE.getTestObjectAttrListForTestReport();
	}
	
	public static List<TestObjectAttribute> getTestObjectAttrListForStepReport() {
		return TestReporterSingleton.INSTANCE.getTestObjectAttrListForStepReport();
	}
	
	public static List<TestObjectAttribute> getTestObjectAttrListForIssueReport() {
		return TestReporterSingleton.INSTANCE.getTestObjectAttrListForIssueReport();
	}
	
	public static List<TestObjectAttribute> getTestObjectAttrListForFixtureReport() {
		return TestReporterSingleton.INSTANCE.getTestObjectAttrListForFixtureReport();
	}
	
	public static List<TestAttribute> getTestAttrList(){
		return TestReporterSingleton.INSTANCE.getTestAttrList();
	}
	
	public static List<TestResultAttribute> getTestResultAttrList(){
		return TestReporterSingleton.INSTANCE.getTestResultAttrList();
	}
	
	public static List<StepResultAttribute> getStepResultAttrList(){
		return TestReporterSingleton.INSTANCE.getStepResultAttrList();
	}
	
	public static List<IssueAttribute> getIssueAttrList(){
		return TestReporterSingleton.INSTANCE.getIssueAttrList();
	}
	
	public static List<FixtureResultPropertyType> getFixtureResultAttrList() {
		return TestReporterSingleton.INSTANCE.getFixtureResultAttrList();
	}
	
	public static List<EventAttribute> getEventAttrList(){
		return TestReporterSingleton.INSTANCE.getEventAttrList();
	}
	
	public static List<TestReportSection> getReportSections(){
		return TestReporterSingleton.INSTANCE.getReportSections();
	}
	
	public static boolean shouldIncludedReportSection(TestReportSection section){
		return TestReporterSingleton.INSTANCE.shouldIncludedReportSection(section);
	}
	
	public static Set<TestResultType> getReportableTestTypes(){
		return TestReporterSingleton.INSTANCE.getReportableTestTypes();
	}
	
	public static boolean isReportableResultType(TestResultType type){
		return TestReporterSingleton.INSTANCE.isReportableResultType(type);
	}
	
	public static boolean shouldIncludeAnnotatedTestPropsInReport(){
		return TestReporterSingleton.INSTANCE.shouldIncludeAnnotatedTestPropsInReport();
	}
	
	public static boolean shouldIncludeCustomPropsInReport(){
		return TestReporterSingleton.INSTANCE.shouldIncludeCustomPropsInReport();
	}
	
	public static boolean shouldIncludeUtvInReport(){
		return TestReporterSingleton.INSTANCE.shouldIncludeUtvInReport();
	}
	
	public static boolean shouldIncludeDataRecordInReport(){
		return TestReporterSingleton.INSTANCE.shouldIncludeDataRecordInReport();
	}
	
	public static boolean shouldIncludeDataRefInReport(){
		return TestReporterSingleton.INSTANCE.shouldIncludeDataRefInReport();
	}

	public static Session getSession() {
		return ArjunaSingleton.INSTANCE.getSession();
	}

}
