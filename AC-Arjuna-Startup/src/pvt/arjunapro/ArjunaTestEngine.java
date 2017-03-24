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
package pvt.arjunapro;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;

import com.arjunapro.pvt.ArjunaInternal;
import com.arjunapro.sysauto.batteries.ThreadBatteries;
import com.arjunapro.testauto.config.RunConfig;
import com.arjunapro.testauto.console.Console;

import pvt.arjunapro.enums.ArjunaProperty;
import pvt.arjunapro.enums.ReportFormat;
import pvt.arjunapro.enums.TestLanguage;
import pvt.arjunapro.interfaces.InternlReportableObserver;
import pvt.batteries.config.Batteries;
import pvt.unitee.config.ArjunaSingleton;
import pvt.unitee.lib.engine.TestEngine;
import pvt.unitee.lib.engine.TestSessionRunner;
import pvt.unitee.reporter.lib.CentralExecutionState;
import pvt.unitee.reporter.lib.CentralReportGenerator;
import pvt.unitee.reporter.lib.DefaultReporter;
import pvt.unitee.reporter.lib.Reporter;
import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.test.TestResult;
import pvt.unitee.reporter.lib.writer.console.ConsoleEventWriter;
import pvt.unitee.reporter.lib.writer.console.ConsoleTestResultWriter;
import pvt.unitee.reporter.lib.writer.excel.ExcelReportGenerator;
import pvt.unitee.testobject.lib.loader.JavaTestClassDefinitionsLoader;
import pvt.unitee.testobject.lib.loader.TestDefinitionsProcessor;
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
		testQueueBuilder.setTestDefinitionsLoader(TestLanguage.JAVA, new JavaTestClassDefinitionsLoader());
		testQueueBuilder.populate();		
	}
	
	@Override
	public void initReporter() throws Exception {
		logger.debug(Batteries.getInfoMessageText(ArjunaInternal.info.TESTRUNNER_CREATE_START));
		logger.debug(Batteries.getInfoMessageText(ArjunaInternal.info.TESTREPORTER_CREATE_START));
		archive();
		
		ArjunaSingleton.INSTANCE.setCentralExecState(new CentralExecutionState());
		Reporter reporter = new DefaultReporter();
		List<String> reportFormats = Batteries.value(ArjunaProperty.REPORT_LISTENERS_BUILTIN).asStringList();
		for (String reportFormatName: reportFormats) {
			if (ArjunaInternal.displayReportPrepInfo){
				logger.debug(reportFormatName);
			}
			ReportFormat reportFormat = ReportFormat.valueOf(reportFormatName.toUpperCase());
			switch(reportFormat){
			case CONSOLE:
				InternlReportableObserver<TestResult> execConsoleObserver = new ConsoleTestResultWriter();
				reporter.addTestResultObserver(execConsoleObserver);
				InternlReportableObserver<Event> acConsoleObserver = new ConsoleEventWriter();
				reporter.addEventObserver(acConsoleObserver);
				break;
			default:
				String msg = "Unrecognized report format option: " + reportFormatName + ". Exiting now...";
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
			ReportFormat reportFormat = ReportFormat.valueOf(reportFormatName.toUpperCase());
			switch(reportFormat){
			case EXCEL:
				FileUtils.forceMkdir(new File(reportDir + "/excel"));
				generator.addReportGenerator(new ExcelReportGenerator(reportDir + "/excel"));
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
	}
	
	protected String getReportDir() throws Exception {
		String dirPath = Batteries.value(ArjunaProperty.DIRECTORY_RUNID_REPORT_ROOT).asString(); 
		
		File dirObj = new File(dirPath);
		//FileUtils.forceMkdir(arg0 );
		if (!dirObj.exists()){
			FileUtils.forceMkdir(dirObj);
			//dirObj.mkdirs();
		}
		
		return dirPath;
	}
	
	private String getArchivesDir() throws Exception{
		return Batteries.value(ArjunaProperty.DIRECTORY_ARCHIVES).asString();
	}
	
	protected void archive() throws Exception{
		String dirPath = Batteries.value(ArjunaProperty.DIRECTORY_REPORT).asString(); 
		
		File dirObj = new File(dirPath);
		//FileUtils.forceMkdir(arg0 );
		if (!dirObj.exists()){
			FileUtils.forceMkdir(dirObj);
			//dirObj.mkdirs();
		}
		
		FileUtils.forceMkdir(new File(getArchivesDir()));
		for (File f: (new File(Batteries.value(ArjunaProperty.DIRECTORY_REPORT).asString())).listFiles()){
			if (f.isHidden()) continue;
			if (f.isDirectory()){
				String targetPath = getArchivesDir() + "/" + f.getName();
				File targetDir = new File(targetPath);
				FileUtils.moveDirectory(f, targetDir);
			}
		}
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
			System.err.println("Critical Error: Exception occured while session Thread.");
			e.printStackTrace();
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
