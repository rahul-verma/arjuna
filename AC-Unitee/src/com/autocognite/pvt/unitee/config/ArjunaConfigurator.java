package com.autocognite.pvt.unitee.config;

import java.util.ArrayList;
import java.util.HashMap;

import com.autocognite.arjuna.interfaces.Value;
import com.autocognite.arjuna.utils.SystemBatteries;
import com.autocognite.internal.arjuna.enums.TestAttribute;
import com.autocognite.internal.arjuna.enums.TestObjectAttribute;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.arjuna.enums.EventAttribute;
import com.autocognite.pvt.arjuna.enums.FixtureResultPropertyType;
import com.autocognite.pvt.arjuna.enums.IssueAttribute;
import com.autocognite.pvt.arjuna.enums.ReportFormat;
import com.autocognite.pvt.arjuna.enums.ReportMode;
import com.autocognite.pvt.arjuna.enums.ReportablePropertyType;
import com.autocognite.pvt.arjuna.enums.StepResultAttribute;
import com.autocognite.pvt.arjuna.enums.TestReportSection;
import com.autocognite.pvt.arjuna.enums.TestResultAttribute;
import com.autocognite.pvt.arjuna.enums.TestResultType;
import com.autocognite.pvt.batteries.console.Console;
import com.autocognite.pvt.batteries.ds.Message;
import com.autocognite.pvt.batteries.ds.MessagesContainer;
import com.autocognite.pvt.batteries.ds.NamesContainer;
import com.autocognite.pvt.batteries.hocon.HoconReader;
import com.autocognite.pvt.batteries.hocon.HoconResourceReader;
import com.autocognite.pvt.batteries.integration.AbstractComponentConfigurator;
import com.autocognite.pvt.batteries.property.ConfigProperty;
import com.autocognite.pvt.batteries.property.ConfigPropertyBatteries;
import com.autocognite.pvt.batteries.property.ConfigPropertyBuilder;
import com.autocognite.pvt.batteries.value.IncompatibleInputForValueException;
import com.autocognite.pvt.batteries.value.UnsupportedRepresentationException;
import com.autocognite.pvt.unitee.lib.strings.UniteeNames;
import com.autocognite.pvt.unitee.reporter.lib.config.TestReporterSingleton;

public class ArjunaConfigurator extends AbstractComponentConfigurator{
	private ConfigPropertyBuilder<ArjunaProperty> builder = new ConfigPropertyBuilder<ArjunaProperty>();
	private HashMap<String, ArjunaProperty> pathToEnumMap = new HashMap<String, ArjunaProperty>();
	private HashMap<ArjunaProperty, String> enumToPathMap = new HashMap<ArjunaProperty, String>();
	
	public ArjunaConfigurator() {
		super("Unitee");
		for (ArjunaProperty e: ArjunaProperty.class.getEnumConstants()){
			String path = ConfigPropertyBatteries.enumToPropPath(e);
			pathToEnumMap.put(path.toUpperCase(), e);
			enumToPathMap.put(e, path.toUpperCase());
		}
	}
	
	private ArjunaProperty codeForPath(String propPath){
		return pathToEnumMap.get(propPath.toUpperCase());
	}
	
	protected void handleStringConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createStringProperty(codeForPath(propPath), propPath, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleCoreDirPath(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createCoreDirPath(codeForPath(propPath), propPath, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleProjectDirPath(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createProjectDirPath(codeForPath(propPath), propPath, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleBooleanConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createBooleanProperty(codeForPath(propPath), propPath, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
//	protected void handleMultiDirConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
//		ConfigProperty prop = ConfigPropertyBatteries.createDirectoriesProperty(codeForPath(propPath), propPath, configValue, purpose, visible);
//		registerProperty(prop);		
//	}
	
	protected void handleStringListConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createStringListProperty(codeForPath(propPath), propPath, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleReportFormatsListConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = null;
		try{
			prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, ReportFormat.class, configValue, purpose, visible);
		} catch (IncompatibleInputForValueException e){
			Console.displayError("Error: Invalid Report Format supplied.");
			Console.displayError("Solution: Check configuration files and CLI options that you have provided. Provided value(s) should be valid ReportFormat Enum types.");
			Console.displayExceptionBlock(e);
			SystemBatteries.exit();			
		}
		registerProperty(prop);		
	}
	
	protected void handleTestObjectPropListConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, TestObjectAttribute.class, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleTestPropListConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, TestAttribute.class, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleTestResultPropListConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, TestResultAttribute.class, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleStepResultPropListConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, StepResultAttribute.class, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleIssuePropListConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, IssueAttribute.class, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleEventPropListConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, EventAttribute.class, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleFixturePropListConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, FixtureResultPropertyType.class, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleReportSectionPropList(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, ReportablePropertyType.class, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleReportMode(String propPath, Value configValue, String purpose, boolean visible) throws Exception {
		try{
			ConfigProperty prop = ConfigPropertyBatteries.createEnumProperty(codeForPath(propPath), propPath,
					ReportMode.class, configValue, purpose, visible);
			registerProperty(prop);
		} catch (UnsupportedRepresentationException e){
			Console.displayError(String.format("Unsupported report format provided in your input: %s.", configValue.asString()));
			Console.displayError("Check your config files and CLI options.");
			Console.displayError("Exiting...");
			System.exit(1);
		}
	}
	
	protected void handleReportSections(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, TestReportSection.class, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleTestResultType(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createEnumListProperty(codeForPath(propPath), propPath, TestResultType.class, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	public void processConfigProperties(HashMap<String, Value> properties) throws Exception{
		@SuppressWarnings("unchecked")
		HashMap<String, Value> tempMap = (HashMap<String, Value>) properties.clone();
		for (String propPath: tempMap.keySet()){
			String ucPropPath = propPath.toUpperCase();
			Value cValue = tempMap.get(propPath);
			if (pathToEnumMap.containsKey(ucPropPath)){
				switch(pathToEnumMap.get(ucPropPath)){
				case SESSION_NAME:
					handleStringConfig(propPath, cValue, "Test Session Name", false);
					break;
				case RUNID:
					handleStringConfig(propPath, cValue, "Test Run ID", true);
					break;
				case FAILFAST:
					handleBooleanConfig(propPath, cValue, "Stop on first failure/error?", false);
					break;
				case FIXTURE_TESTCLASS_SETUPCLASS_NAME:
					handleStringConfig(propPath, cValue, "Set Up Class Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_SETUPCLASSINSTANCE_NAME:
					handleStringConfig(propPath, cValue, "Set Up Class Instance Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_SETUPCLASSFRAGMENT_NAME:
					handleStringConfig(propPath, cValue, "Set Up Class Fragment Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_SETUPMETHOD_NAME:
					handleStringConfig(propPath, cValue, "Set Up Method Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_SETUPMETHODINSTANCE_NAME:
					handleStringConfig(propPath, cValue, "Set Up Method Instance Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_SETUPTEST_NAME:
					handleStringConfig(propPath, cValue, "Set Up Test Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_TEARDOWNCLASS_NAME:
					handleStringConfig(propPath, cValue, "Tear Down Class Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_TEARDOWNCLASSINSTANCE_NAME:
					handleStringConfig(propPath, cValue, "Tear Down Class Instance Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_TEARDOWNCLASSFRAGMENT_NAME:
					handleStringConfig(propPath, cValue, "Tear Down Class Fragment Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_TEARDOWNMETHOD_NAME:
					handleStringConfig(propPath, cValue, "Tear Down Method Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_TEARDOWNMETHODINSTANCE_NAME:
					handleStringConfig(propPath, cValue, "Tear Down Method Instance Fixture Method Name", true);
					break;
				case FIXTURE_TESTCLASS_TEARDOWNTEST_NAME:
					handleStringConfig(propPath, cValue, "Tear Down Test Fixture Method Name", true);
					break;
				case REPORT_MODE:
					this.handleReportMode(propPath, cValue, "Report Mode", true);
					break;
				case REPORT_MINIMAL_METADATA_TEST_OBJECT_TESTS:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Minimal Report - Tests", false);
					break;	
				case REPORT_MINIMAL_METADATA_TEST_OBJECT_STEPS:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Minimal Report - Steps", false);
					break;
				case REPORT_MINIMAL_METADATA_TEST_OBJECT_ISSUES:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Minimal Report - Issues", false);
					break;
				case REPORT_MINIMAL_METADATA_TEST_OBJECT_FIXTURES:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Minimal Report - Fixtures", false);
					break;
				case REPORT_BASIC_METADATA_TEST_OBJECT_TESTS:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Basic Report - Tests", false);
					break;	
				case REPORT_BASIC_METADATA_TEST_OBJECT_STEPS:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Basic Report - Steps", false);
					break;
				case REPORT_BASIC_METADATA_TEST_OBJECT_ISSUES:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Basic Report - Issues", false);
					break;
				case REPORT_BASIC_METADATA_TEST_OBJECT_FIXTURES:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Basic Report - Fixtures", false);
					break;
				case REPORT_ADVANCED_METADATA_TEST_OBJECT_TESTS:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Advanced Report - Tests", false);
					break;	
				case REPORT_ADVANCED_METADATA_TEST_OBJECT_STEPS:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Advanced Report - Steps", false);
					break;
				case REPORT_ADVANCED_METADATA_TEST_OBJECT_ISSUES:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Advanced Report - Issues", false);
					break;
				case REPORT_ADVANCED_METADATA_TEST_OBJECT_FIXTURES:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Advanced Report - Fixtures", false);
					break;
				case REPORT_DEBUG_METADATA_TEST_OBJECT_TESTS:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Debug Report - Tests", false);
					break;
				case REPORT_DEBUG_METADATA_TEST_OBJECT_STEPS:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Debug Report - Steps", false);
					break;
				case REPORT_DEBUG_METADATA_TEST_OBJECT_ISSUES:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Debug Report - Issues", false);
					break;
				case REPORT_DEBUG_METADATA_TEST_OBJECT_FIXTURES:
					handleTestObjectPropListConfig(propPath, cValue, "Test Object Properties for Debug Report - Fixtures", false);
					break;
				case REPORT_MINIMAL_SECTIONS:
					handleReportSections(propPath, cValue, "Report Sections for Minimal Report Mode", false);
					break;	
				case REPORT_BASIC_SECTIONS:
					handleReportSections(propPath, cValue, "Report Sections for Basic Report Mode", false);
					break;		
				case REPORT_ADVANCED_SECTIONS:
					handleReportSections(propPath, cValue, "Report Sections for Basic Report Mode", false);
					break;	
				case REPORT_DEBUG_SECTIONS:
					handleReportSections(propPath, cValue, "Report Sections for Basic Report Mode", false);
					break;
				case REPORT_MINIMAL_INCLUDED_RTYPE:
					handleTestResultType(propPath, cValue, "Included Test Results for Minimal Report Mode", false);
					break;	
				case REPORT_BASIC_INCLUDED_RTYPE:
					handleTestResultType(propPath, cValue, "Included Test Results for Basic Report Mode", false);
					break;		
				case REPORT_ADVANCED_INCLUDED_RTYPE:
					handleTestResultType(propPath, cValue, "Included Test Results for Basic Report Mode", false);
					break;	
				case REPORT_DEBUG_INCLUDED_RTYPE:
					handleTestResultType(propPath, cValue, "Included Test Results for Basic Report Mode", false);
					break;
				case REPORT_METADATA_TEST:
					handleTestPropListConfig(propPath, cValue, "Test Properties for Report", false);
					break;
				case REPORT_MINIMAL_TESTS_ANNOTATED_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Annotated Test Properties be included in Report?", false);
					break;						
				case REPORT_MINIMAL_TESTS_CUSTOM_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Custom Properties be included in Report?", false);
					break;			
				case REPORT_MINIMAL_TESTS_UDV_ON:
					this.handleBooleanConfig(propPath, cValue, "Should User Defined Values be included in Report?", false);
					break;	
				case REPORT_MINIMAL_TESTS_DATARECORD_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Data Record be included in Report?", false);
					break;	
				case REPORT_MINIMAL_TESTS_DATAREF_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Data References be included in Report?", false);
					break;	
				case REPORT_BASIC_TESTS_ANNOTATED_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Annotated Test Properties be included in Report?", false);
					break;	
				case REPORT_BASIC_TESTS_CUSTOM_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Custom Properties be included in Report?", false);
					break;			
				case REPORT_BASIC_TESTS_UDV_ON:
					this.handleBooleanConfig(propPath, cValue, "Should User Defined Values be included in Report?", false);
					break;	
				case REPORT_BASIC_TESTS_DATARECORD_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Data Record be included in Report?", false);
					break;	
				case REPORT_BASIC_TESTS_DATAREF_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Data References be included in Report?", false);
					break;	
				case REPORT_ADVANCED_TESTS_ANNOTATED_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Annotated Test Properties be included in Report?", false);
					break;	
				case REPORT_ADVANCED_TESTS_CUSTOM_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Custom Properties be included in Report?", false);
					break;			
				case REPORT_ADVANCED_TESTS_UDV_ON:
					this.handleBooleanConfig(propPath, cValue, "Should User Defined Values be included in Report?", false);
					break;	
				case REPORT_ADVANCED_TESTS_DATARECORD_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Data Record be included in Report?", false);
					break;	
				case REPORT_ADVANCED_TESTS_DATAREF_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Data References be included in Report?", false);
					break;	
				case REPORT_DEBUG_TESTS_ANNOTATED_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Annotated Test Properties be included in Report?", false);
					break;	
				case REPORT_DEBUG_TESTS_CUSTOM_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Custom Properties be included in Report?", false);
					break;			
				case REPORT_DEBUG_TESTS_UDV_ON:
					this.handleBooleanConfig(propPath, cValue, "Should User Defined Values be included in Report?", false);
					break;	
				case REPORT_DEBUG_TESTS_DATARECORD_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Data Record be included in Report?", false);
					break;	
				case REPORT_DEBUG_TESTS_DATAREF_ON:
					this.handleBooleanConfig(propPath, cValue, "Should Data References be included in Report?", false);
					break;	
				case REPORT_EVENTS_METADATA_REPORTABLE:
					handleEventPropListConfig(propPath, cValue, "Included Properties for Event report", false);
					break;
				case REPORT_TESTS_METADATA_REPORTABLE:
					handleTestResultPropListConfig(propPath, cValue, "Result Properties for Test Execution report", false);
					break;
				case REPORT_ISSUES_METADATA_REPORTABLE:
					handleIssuePropListConfig(propPath, cValue, "Result Properties for Issues report", false);
					break;
				case REPORT_FIXTURES_METADATA_REPORTABLE:
					handleFixturePropListConfig(propPath, cValue, "Fixtures Result Properties for Fixtures report", false);
					break;
				case REPORT_STEPS_METADATA_REPORTABLE:
					handleStepResultPropListConfig(propPath, cValue, "Result Properties for Steps report", false);
					break;
				case DIRECTORY_TESTS:
					handleProjectDirPath(propPath, cValue, "Test Directory", true);
					break;
				case DIRECTORY_REPORT:
					handleProjectDirPath(propPath, cValue, "Report Directory", false);
					break;
				case DIRECTORY_ARCHIVES:
					handleProjectDirPath(propPath, cValue, "Report Archives directory", false);
					break;
				case DIRECTORY_SESSIONS:
					handleProjectDirPath(propPath, cValue, "Session Templates directory", false);
					break;
				case DIRECTORY_GROUPS:
					handleProjectDirPath(propPath, cValue, "Group Templates directory", false);
					break;
				case DIRECTORY_RUNID_REPORT_ROOT:
					handleStringConfig(propPath, cValue, "Report Directory for the Run ID", false);
					break;
				case DIRECTORY_RUNID_REPORT_JSON_RAW_ROOT:
					handleStringConfig(propPath, cValue, "Root Raw Report Directory for JSON.", false);
					break;
				case DIRECTORY_RUNID_REPORT_JSON_RAW_TESTS:
					handleStringConfig(propPath, cValue, "Raw Report Directory for JSON Test Execution results.", false);
					break;
				case DIRECTORY_RUNID_REPORT_JSON_RAW_ISSUES:
					handleStringConfig(propPath, cValue, "Report Directory for JSON Fixture results.", false);
					break;
				case DIRECTORY_RUNID_REPORT_JSON_RAW_EVENTS:
					handleStringConfig(propPath, cValue, "Report Directory for JSON Event results.", false);
					break;
				case DIRECTORY_RUNID_REPORT_JSON_RAW_FIXTURES:
					handleStringConfig(propPath, cValue, "Report Directory for JSON Fixture results.", false);
					break;
				case REPORT_NAME_FORMAT:
					handleStringConfig(propPath, cValue, "Report Name Format", false);
					break;
				case REPORT_GENERATORS_BUILTIN:
					handleReportFormatsListConfig(propPath, cValue, "Chosen Built-in Report Generators", false);
					break;
				case REPORT_LISTENERS_BUILTIN:
					handleReportFormatsListConfig(propPath, cValue, "Chosen Built-in Report Listeners", false);
					break;
				default:
					break;
				}
				
				properties.remove(propPath);
			}
		}
		
	}

	public void processDefaults() throws Exception {
		HoconReader reader =  new HoconResourceReader(this.getClass().getResourceAsStream("/com/autocognite/pvt/text/arjuna.conf"));
		super.processDefaults(reader);
	}
	
	@Override
	public void loadComponent() throws Exception {
		TestReporterSingleton.INSTANCE.init();
	}

	@Override
	protected ArrayList<MessagesContainer> getAllMessages() {
		ArrayList<MessagesContainer> containers = new ArrayList<MessagesContainer>();
		
		MessagesContainer problemMessages = new MessagesContainer("PROBLEM_MESSAGES");
		problemMessages.add(new Message(	
			ArjunaInternal.problem.REPORT_WRONG_FORMAT,
			"!!!Wrong Report Format(s) Supplied!!!"
		));
		containers.add(problemMessages);

		MessagesContainer infoMessages = new MessagesContainer("INFO_MESSAGES");
		infoMessages.add(new Message(	
			ArjunaInternal.info.RUN_BEGIN,
			"------------ RUN: START -----------------"
		));
		
		infoMessages.add(new Message(	
			ArjunaInternal.info.RUN_FINISH,
			"------------ RUN: FINISH -----------------"
		));
				
		infoMessages.add(new Message(	
			ArjunaInternal.info.PRINT_CONFIGURATION,
			"Proceeding with the following Configuration Settings:"
		));
		
		infoMessages.add(new Message(	
				ArjunaInternal.info.TESTRUNNER_CREATE_START,
			"Create Test Runner - Start"
		));
		
		infoMessages.add(new Message(	
				ArjunaInternal.info.TESTRUNNER_CREATE_FINISH,
			"Create Test Runner - Finish"
		));
		
		infoMessages.add(new Message(	
				ArjunaInternal.info.TESTREPORTER_CREATE_START,
			"Create Test Reporter - Start"
		));
		
		infoMessages.add(new Message(	
				ArjunaInternal.info.TESTREPORTER_CREATE_FINISH,
			"Create Test Reporter - Finish"
		));
		
		infoMessages.add(new Message(	
				ArjunaInternal.info.TEST_DISCOVERY_START,
				"Discovering tests..."
			));
			
			infoMessages.add(new Message(	
					ArjunaInternal.info.TEST_DISCOVERY_FINISH,
				"Discovery completed."
			));
		
		
		infoMessages.add(new Message(	
				ArjunaInternal.info.ALLOWED_REPORT_FORMATS,
			"Allowed Formats: XML/XLS/DELIMITED/INI/CONSOLE"
		));

		containers.add(infoMessages);		
		
		return containers;
	}

	@Override
	protected ArrayList<NamesContainer> getAllNames() {
		return UniteeNames.getAllNames();
	}
	
}
