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
package pvt.unitee.arjuna;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import arjunasdk.sysauto.batteries.FileSystemBatteries;
import arjunasdk.sysauto.batteries.SystemBatteries;
import arjunasdk.sysauto.batteries.ThreadBatteries;
import pvt.batteries.config.Batteries;
import pvt.unitee.config.ArjunaSingleton;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.enums.ReportGenerationFormat;
import pvt.unitee.enums.ReportListenerFormat;
import pvt.unitee.enums.TestLanguage;
import pvt.unitee.interfaces.InternlReportableObserver;
import pvt.unitee.lib.engine.TestEngine;
import pvt.unitee.lib.engine.TestSessionRunner;
import pvt.unitee.reporter.lib.CentralReportGenerator;
import pvt.unitee.reporter.lib.DefaultReporter;
import pvt.unitee.reporter.lib.GlobalState;
import pvt.unitee.reporter.lib.Reporter;
import pvt.unitee.reporter.lib.SummaryResult;
import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.test.TestResult;
import pvt.unitee.reporter.lib.writer.console.ConsoleEventWriter;
import pvt.unitee.reporter.lib.writer.console.ConsoleTestResultWriter;
import pvt.unitee.reporter.lib.writer.excel.ExcelReportGenerator;
import pvt.unitee.reporter.lib.writer.jxml.JXmlReportGenerator;
import pvt.unitee.testobject.lib.java.loader.JavaTestClassDefLoader;
import pvt.unitee.testobject.lib.java.loader.TestDefinitionsProcessor;
import pvt.unitee.testobject.lib.loader.session.Session;

public class ArjunaTestEngine implements TestEngine{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private Session session = null;
	
	public ArjunaTestEngine(String[] options) throws Exception {
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.eng.ITestEngine#setUp()
	 */
	@Override
	public void setUp() throws Exception {	
	}
	
	@Override
	public void discover() throws Exception {
		TestDefinitionsProcessor testQueueBuilder = new TestDefinitionsProcessor();
		testQueueBuilder.setTestDefinitionsLoader(TestLanguage.JAVA, new JavaTestClassDefLoader());
		testQueueBuilder.populate();		
	}
	
	@Override
	public void initReporter() throws Exception {
		logger.debug(Batteries.getInfoMessageText(ArjunaInternal.info.TESTRUNNER_CREATE_START));
		logger.debug(Batteries.getInfoMessageText(ArjunaInternal.info.TESTREPORTER_CREATE_START));
		SummaryResult.init();
		ArjunaSingleton.INSTANCE.setCentralExecState(new GlobalState());
		Reporter reporter = new DefaultReporter();
		List<String> reportFormats = Batteries.value(ArjunaProperty.REPORT_LISTENERS_BUILTIN).asStringList();
		for (String reportFormatName: reportFormats) {
			if (ArjunaInternal.displayReportPrepInfo){
				logger.debug(reportFormatName);
			}
			ReportListenerFormat reportFormat = ReportListenerFormat.valueOf(reportFormatName.toUpperCase());
			switch(reportFormat){
			case CONSOLE:
				InternlReportableObserver<TestResult> execConsoleObserver = new ConsoleTestResultWriter();
				reporter.addTestResultObserver(execConsoleObserver);
				InternlReportableObserver<Event> acConsoleObserver = new ConsoleEventWriter();
				reporter.addEventObserver(acConsoleObserver);
				break;
			default:
				String msg = "Unrecognized report listener format option: " + reportFormatName + ". Exiting now...";
				logger.fatal(msg);
				Console.displayExceptionBlock(new Exception(msg));
				System.err.println(msg);
				System.exit(1);
			}
		}
		
		ArjunaSingleton.INSTANCE.setReporter(reporter);

		logger.debug(Batteries.getInfoMessageText(ArjunaInternal.info.TESTREPORTER_CREATE_FINISH));
		logger.debug(Batteries.getInfoMessageText(ArjunaInternal.info.TESTRUNNER_CREATE_FINISH));		
	}
	
	@Override
	public void report() throws Exception{
		if (ArjunaInternal.displayReportGenerationInfo){
			logger.debug("Setting up Report Generator");
		}
		
		String reportDir = this.getReportDir();
		CentralReportGenerator generator = new CentralReportGenerator();
		List<String> reportFormats = Batteries.value(ArjunaProperty.REPORT_GENERATORS_BUILTIN).asStringList();
		for (String reportFormatName: reportFormats) {
			if (ArjunaInternal.displayReportGenerationInfo){
				logger.debug(reportFormatName);
			}
			ReportGenerationFormat reportFormat = ReportGenerationFormat.valueOf(reportFormatName.toUpperCase());
			switch(reportFormat){
			case EXCEL:
				FileUtils.forceMkdir(new File(reportDir + "/excel"));
				generator.addReportGenerator(new ExcelReportGenerator(reportDir + "/excel"));
				break;
			case JXML:
				FileUtils.forceMkdir(new File(reportDir + "/jxml"));
				generator.addReportGenerator(new JXmlReportGenerator(reportDir + "/jxml"));
				break;
			default:
				String msg = "Unrecognized report format option: " + reportFormatName + ". Exiting now...";
				logger.fatal(msg);
				Console.displayExceptionBlock(new Exception(msg));
				System.err.println(msg);
			}
		}
		
		if (ArjunaInternal.displayReportGenerationInfo){
			logger.debug("Launching Report Generator");
		}
		generator.setUp();
		generator.generate();
		generator.tearDown();
		archive();
	}
	
	protected String getReportDir() throws Exception {
		return Batteries.value(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_ROOT).asString();
	}
	
	private String getArchivesDir() throws Exception{
		return Batteries.value(ArjunaProperty.DIRECTORY_PROJECT_ARCHIVES).asString();
	}
	
	protected void archive() throws Exception{
//		String dirPath = Batteries.value(ArjunaProperty.DIRECTORY_PROJECT_REPORT).asString(); 
//		
//		File dirObj = new File(dirPath);
//		//FileUtils.forceMkdir(arg0 );
//		if (!dirObj.exists()){
//			FileUtils.forceMkdir(dirObj);
//			//dirObj.mkdirs();
//		}
		
		File centralReportDir = new File(Batteries.value(ArjunaProperty.DIRECTORY_PROJECT_REPORT).asString());
		String lastRuntimestamp = new SimpleDateFormat("yyyy.MM.dd-HH.mm.ss").format(new Date(centralReportDir.lastModified()));
		String archiveDirForLatestTest = getArchivesDir() + "/" + lastRuntimestamp + "-" +  Batteries.value(ArjunaProperty.RUNID).asString();
		//FileUtils.forceMkdir(new File(archiveDirForLatestTest));
		
		File runReportDir = new File(this.getReportDir());
		
		FileUtils.copyDirectory(runReportDir, new File(archiveDirForLatestTest));

//		for (File f: runReportDir.listFiles()){
//			if (f.isHidden()) continue;
//			if (f.isDirectory()){
//				String targetPath = archiveDirForLatestTest + "/" + f.getName();
//				File targetDir = new File(targetPath);
//				FileUtils.copyDirectory(srcDir, destDir);(f, targetDir);
////				try{
////					FileUtils.moveDirectory(f, targetDir);
////				} catch (Throwable e){
////					Console.displayError("Arjuna archives previous run's report contents at beginning of new run.");
////					Console.displayError("Arjuna faced a critical issue in archiving contents of report directory.");
////					Console.displayError("Please close any files that you have opened from the report directory and execute the run again.");
////					Console.displayError("Now Arjuna would attempt to delete any partial archive created and exit.");
////					Console.displayExceptionBlock(e);
////					try{
////						FileSystemBatteries.deleteDirectory(targetPath);
////					} catch (Throwable g){
////						//Console.displayError("Arjuna archives previous run's report contents at beginning of new run.");
////					}
////				}
//			}
//		}
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.eng.ITestEngine#run()
	 */
	@Override
	public void run() throws Exception {
		logger.debug(Batteries.getInfoMessageText(ArjunaInternal.info.RUN_BEGIN));
		Thread t;
		try{
			Session session = ArjunaInternal.getSession();
			t = ThreadBatteries.createBaseThread(session.getName(), new TestSessionRunner(session));
			t.start();
			t.join();
		} catch (Exception e){
			System.err.println("Critical Error: Exception occured in session Thread.");
			Console.displayExceptionBlock(e);
			System.err.println("Exiting...");
			System.exit(1);
		}
		ArjunaInternal.getReporter().tearDown();
		logger.debug(Batteries.getInfoMessageText(ArjunaInternal.info.RUN_FINISH));
	}
	
	@Override
	public void tearDown() throws Exception {
	}
}
