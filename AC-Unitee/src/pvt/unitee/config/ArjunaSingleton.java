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
package pvt.unitee.config;

import java.io.File;
import java.lang.reflect.Method;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.io.FileUtils;

import com.typesafe.config.ConfigException;
import com.typesafe.config.ConfigObject;

import arjunasdk.console.Console;
import arjunasdk.ddauto.interfaces.DataSource;
import arjunasdk.interfaces.Value;
import arjunasdk.sysauto.batteries.FileSystemBatteries;
import arjunasdk.sysauto.batteries.SystemBatteries;
import pvt.arjunasdk.enums.BatteriesPropertyType;
import pvt.arjunasdk.integration.UiAutoIntegrator;
import pvt.arjunasdk.property.ConfigPropertyBatteries;
import pvt.batteries.cli.CLIConfigurator;
import pvt.batteries.config.Batteries;
import pvt.batteries.hocon.HoconConfigObjectReader;
import pvt.batteries.hocon.HoconFileReader;
import pvt.batteries.hocon.HoconReader;
import pvt.batteries.hocon.HoconResourceReader;
import pvt.batteries.hocon.HoconStringReader;
import pvt.batteries.lib.ComponentIntegrator;
import pvt.batteries.logging.Log;
import pvt.batteries.utils.ResourceStreamBatteries;
import pvt.batteries.value.StringValue;
import pvt.unitee.arjuna.SessionCreator;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.enums.TestPickerProperty;
import pvt.unitee.reporter.lib.GlobalState;
import pvt.unitee.reporter.lib.Reporter;
import pvt.unitee.testobject.lib.definitions.TestDefinitionsDB;
import pvt.unitee.testobject.lib.loader.session.Session;
import unitee.annotations.DataGenerator;
import unitee.annotations.DataMethodContainer;

public enum ArjunaSingleton {
	INSTANCE;
	private String version = "1.1.0-b";

	private Map<String,String> cliHashMap = null;
	private Map<String, HashMap<String,String>> testBucketProps = new HashMap<String, HashMap<String,String>>();

	private String[] cliArgs;
	
	boolean lazyAssertions = false;
	boolean lazyAssertionProcessed = false;
	
	private DataMethodContainerMap dataMethodContainers =  new DataMethodContainerMap();
	private DataGeneratorMap dataGenerators =  new DataGeneratorMap();
	private Reporter reporter = null;

	private GlobalState execState;
	private CLIConfigurator cliConfigurator = null;
	private Session session = null;
	private boolean initUiAuto = false;
	
	private String edition = "Arjuna Pro Platform Edition";
	
	ComponentIntegrator integrator;
	
	private Map<TestPickerProperty,String> cliPickerOptions = null;

	public void setEdition(String edition){
		this.edition = edition;
	}
	
	public void setVersion(String version){
		this.version = version;
	}
	

	public void shouldInitUiAutomator(boolean flag) {
		initUiAuto = flag;
	}
	
	public void setCliConfigurator(CLIConfigurator cliConfigurator) {
		this.cliConfigurator = cliConfigurator;
	}
	
	public void init() throws Exception{
		String customTestDir = null;
		String refPath = FileSystemBatteries.getAbsolutePathFromJar(FileSystemBatteries.getJarFilePathForObject(this), "./../../../..");
//		System.out.println(refPath);
		Batteries.init(refPath);
		Batteries.addConfigurator(UiAutoIntegrator.getComponentConfigurator());
		ArjunaConfigurator uConf = new ArjunaConfigurator();
		Batteries.addConfigurator(uConf);
		Batteries.processArjunaDefaults();
		integrator = uConf.getIntegrator();
		//integrator.enumerate();
		HoconReader reader = new HoconResourceReader(this.getClass().getResourceAsStream("/com/testmile/pvt/text/arjuna_visible.conf"));
		reader.process();		
		integrator.setProjectDir(Batteries.getBaseDir());
		Batteries.processArjunaOptions(reader.getProperties());
		//integrator.enumerate();
		
		// arjuna file
		String arjunaConfPath = integrator.value(BatteriesPropertyType.CONFIG_DIR).asString() + "/" + integrator.value(BatteriesPropertyType.CONFIG_CENTRAL_FILE_NAME).asString();
//		System.out.println(integrator.value(BatteriesPropertyType.DIRECTORY_CONFIG).asString());
//		System.out.println(arjunaConfPath);
		HoconReader reader2 = new HoconFileReader(arjunaConfPath);
		reader2.process();
		
		try{
			ConfigObject arjunaOptObj = reader2.getConfig().getObject("arjunaOptions");
			HoconReader arjunaOptReader = new HoconConfigObjectReader(arjunaOptObj);
			arjunaOptReader.process();
//			System.out.println(configReader.getProperties());
			try{
				Batteries.processArjunaOptions(arjunaOptReader.getProperties());
			} catch (Exception e){
				Console.display("Fatal Error in processing of Arjuna options in central configuration file");
				Console.display("Please check the following exception details and modify the configuration.");
				Console.displayExceptionBlock(e);
				SystemBatteries.exit();
				System.exit(1);
			}
		} catch (ConfigException e){
			// config may not be defined. It's ok. It's optional
		}
		
		try{
			ConfigObject execVarObj = reader2.getConfig().getObject("execVars");
			HoconReader execVarReader = new HoconConfigObjectReader(execVarObj);
			execVarReader.process();
			Batteries.processCentralExecVars(execVarReader.getProperties());
		} catch (ConfigException e){
			// execVars may not be defined. It's ok. It's optional
		}
		
		try{
			ConfigObject userOptions = reader2.getConfig().getObject("userOptions");
			HoconReader userOptionsReader = new HoconConfigObjectReader(userOptions);
			userOptionsReader.process();
			Batteries.processCentralUserOptions(userOptionsReader.getProperties());
		} catch (ConfigException e){
			// userOptions may not be defined. It's ok. It's optional
		}
		
		if (!integrator.value(ArjunaProperty.PROJECT_TESTS_DIR).isNull()){
			customTestDir = integrator.value(ArjunaProperty.PROJECT_TESTS_DIR).asString();
		}
		
		//CLI
		cliConfigurator.setIntegrator(integrator);
		cliConfigurator.setArgs(cliArgs);
		cliConfigurator.processUserOptions();
		Map<String,Value> options = cliConfigurator.getUserOptions();
		try{
			Batteries.processArjunaOptions(options);
		} catch (Exception e){
			Console.display("Fatal Error in processing of CLI Options");
			Console.display("Please check the following exception details and provide the correct CLI options.");
			Console.displayExceptionBlock(e);
			SystemBatteries.exit();
			System.exit(1);
		}
		
		if (!integrator.value(ArjunaProperty.PROJECT_TESTS_DIR).isNull()){
			customTestDir = integrator.value(ArjunaProperty.PROJECT_TESTS_DIR).asString();
		}

//		HashMap<String, Value> updateOptions = new HashMap<String, Value>();
//		String reportDir = integrator.value(ArjunaProperty.DIRECTORY_PROJECT_REPORT).asString();
//		String runID =  integrator.value(ArjunaProperty.RUNID).asString();
//		String timestampedRunID = new SimpleDateFormat("yyyy.MM.dd-HH.mm.ss").format(new Date()) + "-" + runID;
//		String runIDReportDir = integrator.value(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_ROOT).asString()
//				.replace("%%slugREPORT_DIR", reportDir)
//				.replace("%%slugRUNID", timestampedRunID);
//		updateOptions.put(
//				ConfigPropertyBatteries.enumToPropPath(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_ROOT),
//				new StringValue(runIDReportDir)
//		);
//		
//		String rawJsonReportDir = integrator.value(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_ROOT).asString()
//				.replace("%%slugRUNID_RPT_DIR", runIDReportDir);
//		updateOptions.put(
//				ConfigPropertyBatteries.enumToPropPath(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_ROOT),
//				new StringValue(rawJsonReportDir)
//		);
//		
//		updateOptions.put(
//				ConfigPropertyBatteries.enumToPropPath(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_EVENTS),
//				new StringValue(integrator.value(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_EVENTS).asString()
//						.replace("%%slugRAW_DIR", rawJsonReportDir))
//		);
//		
//		updateOptions.put(
//				ConfigPropertyBatteries.enumToPropPath(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_TESTS),
//				new StringValue(integrator.value(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_TESTS).asString()
//						.replace("%%slugRAW_DIR", rawJsonReportDir))
//		);
//		
//		updateOptions.put(
//				ConfigPropertyBatteries.enumToPropPath(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_ISSUES),
//				new StringValue(integrator.value(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_ISSUES).asString()
//						.replace("%%slugRAW_DIR", rawJsonReportDir))
//		);
//		
//		updateOptions.put(
//				ConfigPropertyBatteries.enumToPropPath(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_FIXTURES),
//				new StringValue(integrator.value(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_FIXTURES).asString()
//						.replace("%%slugRAW_DIR", rawJsonReportDir))
//		);
//		
//		updateOptions.put(
//				ConfigPropertyBatteries.enumToPropPath(ArjunaProperty.SESSION_NAME),
//				new StringValue("msession")
//		);
//		
//		Batteries.processConfigProperties(updateOptions);
		// Would deal with projects in Arjuna Pro.
		// For now project directory is same as root
		//String projDir = integrator.value(BatteriesPropertyType.DIRECTORY_PROJECT_ROOT).asString();
		String projDir = Batteries.getBaseDir();
		String runID =  integrator.value(ArjunaProperty.RUNID).asString();
		String md5Suffix = createFileID();
		String internalRunID = String.format("%s-%s", runID, md5Suffix);
//		String timestampedRunID = new SimpleDateFormat("yyyy.MM.dd-HH.mm.ss").format(new Date()) + "-" + runID;
		String updates = ResourceStreamBatteries.streamToString(ArjunaSingleton.class.getResourceAsStream("/com/testmile/pvt/text/arjuna_invisible.conf"));
		String replaced = updates.replace("%%slugProjDir", projDir).replace("%%slugRUNID", internalRunID).replace("%%slugInternalRunID", internalRunID);
		HoconReader uReader = new HoconStringReader(replaced);
		uReader.process();
		Batteries.processArjunaOptions(uReader.getProperties());
		createReportDir();
		//integrator.enumerate();
		
//		Log log = new Log();
//		log.configure(
//				Level.toLevel(integrator.value(BatteriesPropertyType.LOGGING_CONSOLE_LEVEL).asString()),
//				Level.toLevel(integrator.value(BatteriesPropertyType.LOGGING_FILE_LEVEL).asString()),
//				integrator.value(BatteriesPropertyType.LOGGING_NAME).asString(),
//				integrator.value(BatteriesPropertyType.DIRECTORY_PROJECT_LOG).asString()
//		);
		
		if (customTestDir != null){
			if (!(FileSystemBatteries.isAbsolutePath(customTestDir))){
				Console.displayError("Test Directory Path should be an absolute path.");
				Console.displayError("You have provided: " + customTestDir);
				Console.displayError("Please check your CLI usage/configurations");
				Console.displayError("Exiting...");
				Console.displayError("");
				System.exit(1);					
			} else if (!FileSystemBatteries.isDir(customTestDir)){
				Console.displayError("Test Directory Path should be an existing directory.");
				Console.displayError("You have provided: " + customTestDir);
				Console.displayError("Please check your CLI usage/configurations");
				Console.displayError("Exiting...");
				Console.displayError("");
				System.exit(1);	
			} else if (!(new File(customTestDir)).exists()){
				Console.displayError("Test Directory Path provided by you does not exist.");
				Console.displayError("You have provided: " + customTestDir);
				Console.displayError("Please check your CLI usage/configurations");
				Console.displayError("Exiting...");
				Console.displayError("");
				System.exit(1);					
			}
			Map<String, Value> testOptions = new HashMap<String, Value>();
			testOptions.put(
			ConfigPropertyBatteries.enumToPropPath(ArjunaProperty.PROJECT_TESTS_DIR),
			new StringValue(customTestDir)
			);
			Batteries.processArjunaOptions(testOptions);
		}
	}
	
	private String createFileID() throws NoSuchAlgorithmException{

        MessageDigest md = MessageDigest.getInstance("MD5");
        md.update(new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss.SSS").format(new Date()).getBytes());

        byte byteData[] = md.digest();

        //convert the byte to hex format method 1
        StringBuffer sb = new StringBuffer();
        //sb.append(new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss.SSS").format(new Date()));
        for (int i = 0; i < byteData.length; i++) {
         sb.append(Integer.toString((byteData[i] & 0xff) + 0x100, 16).substring(1));
        }	
 
        return sb.toString();
	}
	
	private void createReportDir() throws Exception {
		String centralReportDirPath = integrator.value(ArjunaProperty.PROJECT_REPORT_DIR).asString(); 
		
		File centralDirObj = new File(centralReportDirPath);
		//FileUtils.forceMkdir(arg0 );
		if (!centralDirObj.exists()){
			FileUtils.forceMkdir(centralDirObj);
			//dirObj.mkdirs();
		} else {
			FileSystemBatteries.deleteDirectory(centralReportDirPath);
		}
		
		String dirPath = integrator.value(ArjunaProperty.PROJECT_RUN_REPORT_DIR).asString(); 
		
		File dirObj = new File(dirPath);
		//FileUtils.forceMkdir(arg0 );
		if (!dirObj.exists()){
			FileUtils.forceMkdir(dirObj);
			//dirObj.mkdirs();
		}
		
		String coreTemplateFilePath = integrator.value(ArjunaProperty.PROJECT_CORE_DB_TEMPLATE_RUN_DBFILE).asString(); 
		String coreDBTargetFilePath = integrator.value(ArjunaProperty.PROJECT_CORE_DB_RUN_DBFILE).asString(); 
		
		File coreTemplateFile = new File(coreTemplateFilePath);
		//FileUtils.forceMkdir(arg0 );
		if (!coreTemplateFile.exists()){
			Console.display("Critical: Exception in Test Engine run.");
			Console.display("The data template file for run was not found. Check your Arjuna structure or reinstall.");
			SystemBatteries.exit();
		}
		
		FileSystemBatteries.copyFile(coreTemplateFilePath, coreDBTargetFilePath);
	}
	
	public void freeze() throws Exception{
		// Post processing
		Batteries.freezeCentralConfig();
		integrator.enumerate();
		initlogger();
	}
	
	public void loadSession() throws Exception{
		// Make definitions queu ready for pickers. Report Skip and unpicked
		TestDefinitionsDB.buildPickerQueueFromDiscoveredQueue();
		String sessionName = integrator.value(ArjunaProperty.SESSION_NAME).asString();
		
		SessionCreator sCreator = null;
		sCreator = new SessionCreator(integrator, this.cliPickerOptions, sessionName);
		
		session = sCreator.getSession();
		if (session.getConfigObject() != null){
			HoconReader cReader = new HoconStringReader(session.getConfigObject().toString());
			cReader.process();
			try{
				Batteries.processArjunaOptions(cReader.getProperties());
			} catch (Exception e){
				Console.display("Fatal Error in processing of Arjuna options in session file: " + session.getSessionFilePath());
				Console.display("Please check the following exception details and modify the configuration.");
				Console.displayExceptionBlock(e);
				SystemBatteries.exit();
				System.exit(1);
			}
		}
		
		if (session.getExecVarObject() != null){
			HoconReader sessionExecVarReader = new HoconStringReader(session.getExecVarObject().toString());
			sessionExecVarReader.process();
			Batteries.processCentralExecVars(sessionExecVarReader.getProperties());
		}
		
		if (session.getUserOptionsObject() != null){
			HoconReader sessionUserOptionsReader = new HoconStringReader(session.getUserOptionsObject().toString());
			sessionUserOptionsReader.process();
			Batteries.processCentralUserOptions(sessionUserOptionsReader.getProperties());
		}		
		
		session.setExecVars(Batteries.cloneCentralExecVars());
		session.schedule();
		TestDefinitionsDB.buildProcessorQueueFromPickerQueue();
		session.load();
	}

	public String getVersion() {
		return version;
	}
	
	private void initlogger() throws Exception {
		Log log = new Log();
		log.configure(
				Batteries.getDisplayLevel(),
				Batteries.getLogLevel(),
				Batteries.getCentralLogName(),
				Batteries.getLogDir()
					);
	}
	
	public void printArjunaHeader(){
		Console.display("   ___         _                      ");
		Console.display("  / _ \\       (_)                     ");
		Console.display(" / /_\\ \\ _ __  _  _   _  _ __    __ _ ");
		Console.display(" |  _  || '__|| || | | || '_ \\  / _` |");
		Console.display(" | | | || |   | || |_| || | | || (_| |");
		Console.display(" \\_| |_/|_|   | | \\__,_||_| |_| \\__,_|");
		Console.display("             _/ |                     ");
		Console.display("            |__/                      ");
		                              
		Console.marker(60);	
		Console.display("Copyright (c) 2017-18 Test Mile Software Testing Pvt Ltd");
		Console.marker(60);
		Console.displayPaddedKeyValue("Product Name", this.edition);
		Console.displayPaddedKeyValue("Version", this.version);
		Console.displayPaddedKeyValue("Website", "arjuna.testmile.com");
		Console.displayPaddedKeyValue("Contact", "support@testmile.com");
		Console.marker(60);	
	}

	public void setCliArgs(String[] args) {
		cliArgs = args;
	}
	
	public Reporter getReporter(){
		return this.reporter;
	}
	
	public void setReporter(Reporter reporter){
		this.reporter = reporter;
	}

	public void processNonTestClass(Class<?> klass) throws Exception {
		if (klass.isAnnotationPresent(DataMethodContainer.class)){
			dataMethodContainers.process(klass);
		} else if (klass.isAnnotationPresent(DataGenerator.class)){
			dataGenerators.process(klass);
		}

	}

	public Method getDataGeneratorMethod(String containerName, String dgName) throws Exception {
		return this.dataMethodContainers.getMethod(containerName, dgName);
	}

	public Method getDataGeneratorMethod(Class<?> containerClass, String dgName) throws Exception {
		return this.dataMethodContainers.getMethod(containerClass, dgName);
	}

	public DataSource getDataSourceFromDataGenName(String dataGenName) throws Exception {
		return this.dataGenerators.getDataSource(dataGenName);
	}

	public void setCentralExecState(GlobalState execState) {
		this.execState = execState;
	}
	
	public GlobalState getCentralExecState() {
		return this.execState;
	}
	
	public CLIConfigurator getCliConfigurator(){
		return this.cliConfigurator;
	}

	public Session getSession() {
		return this.session;
	}

	public void setPickerOptions(Map<TestPickerProperty, String> options) {
		this.cliPickerOptions = options;
	}
	
}