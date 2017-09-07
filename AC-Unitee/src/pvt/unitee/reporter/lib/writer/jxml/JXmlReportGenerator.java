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
package pvt.unitee.reporter.lib.writer.jxml;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;
import org.apache.poi.hssf.usermodel.HSSFCellStyle;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.Font;
import org.apache.poi.ss.usermodel.IndexedColors;
import org.w3c.dom.DOMException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

import arjunasdk.config.RunConfig;
import arjunasdk.sysauto.batteries.SystemBatteries;
import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.enums.IgnoredTestStatus;
import pvt.unitee.enums.TestReportSection;
import pvt.unitee.enums.TestResultAttribute;
import pvt.unitee.enums.TestResultType;
import pvt.unitee.interfaces.ReportGenerator;
import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.fixture.FixtureResult;
import pvt.unitee.reporter.lib.ignored.IgnoredTest;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.issue.IssueProperties;
import pvt.unitee.reporter.lib.test.TestResult;
import unitee.enums.TestAttribute;
import unitee.enums.TestObjectAttribute;


public class JXmlReportGenerator implements ReportGenerator {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	String name;
	private int failCount = 0;
	private int errCount = 0;
	private int skipCount = 0;
	private int testCount = 0;
	ArrayList<Element> testResultNodes = new ArrayList<Element>();
	HashMap<String, String> tsAttributes = new HashMap<String, String>();
	String filePath;
	
	// New variables
	private Set<TestResultType> allowedRTypes = null;
	private FileOutputStream fileOut = null;
	
	private List<String> headers = null;
	private List<TestObjectAttribute> execTestObjectProps = null;
	private List<TestAttribute> execTestProps = null;
	private List<TestResultAttribute> execResultProps = null;
	private List<String> execHeaders = new ArrayList<String>();
	
	private boolean shouldIncludeAnnotatedTestProps = false;
	private boolean shouldIncludeAttr = false;
	private boolean shouldIncludeExecVars = false;
	private boolean shouldIncludeDataRecord = false;
	private boolean shouldIncludeDataRef = false;
	
	private Document dom;
	private Element root;
	private Element testSuite;
	
	private Double elapsedTime = 0.0;
	private Map<Integer, Issue> issues = new HashMap<Integer, Issue>();
	
	public JXmlReportGenerator(String reportDir) throws Exception {
		FileUtils.forceMkdir(new File(reportDir));
		fileOut  = new FileOutputStream(reportDir + "/" + Batteries.value(ArjunaProperty.REPORT_NAME_FORMAT).asString() + ".xml");
		this.allowedRTypes = ArjunaInternal.getReportableTestTypes();
	}
	
	public void setUp() throws Exception {
		// Populate meta-data
		Map<TestObjectAttribute,String> testObjectNames = ArjunaInternal.getTestObjectAttrNameMap();
		Map<TestAttribute,String> testPropNames = ArjunaInternal.getTestAttrNameMap();
		
		// Test Result Section		
		Map<TestResultAttribute,String> testResultPropNames = ArjunaInternal.getTestResultAttrNameMap();
		execTestObjectProps = ArjunaInternal.getTestObjectAttrListForTestReport();
		execTestProps = ArjunaInternal.getTestAttrList();
		shouldIncludeAnnotatedTestProps = ArjunaInternal.shouldIncludeAnnotatedTestPropsInReport();
		shouldIncludeAttr = ArjunaInternal.shouldIncludeTestAttrInReport();
		shouldIncludeExecVars = ArjunaInternal.shouldIncludeExecVarsInReport();
		shouldIncludeDataRecord = ArjunaInternal.shouldIncludeDataRecordInReport();
		shouldIncludeDataRef = ArjunaInternal.shouldIncludeDataRefInReport();
		execResultProps = ArjunaInternal.getTestResultAttrList();
		for (TestObjectAttribute prop: execTestObjectProps){
			this.execHeaders.add(testObjectNames.get(prop));
		}
		if (shouldIncludeAnnotatedTestProps){
			for (TestAttribute prop: execTestProps){
				this.execHeaders.add(testPropNames.get(prop));
			}
		}

		for (TestResultAttribute prop: execResultProps){
			this.execHeaders.add(testResultPropNames.get(prop));
		}
		
		if (shouldIncludeAttr){
			this.execHeaders.add("Test Attributes");
		}
		
		if (shouldIncludeExecVars){
			this.execHeaders.add("Execution Variables");
		}
		
		if (shouldIncludeDataRecord){
			this.execHeaders.add("Data Record");
		}
		
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		DocumentBuilder db = dbf.newDocumentBuilder();
		dom = db.newDocument();
		this.root = dom.createElement("testsuites");
		this.testSuite = dom.createElement("testsuite");
	}
	
	private void populateExceptionData(Element e, TestResult tr) throws Exception{
		e.setAttribute("message", this.issues.get(tr.resultProps().issueId()).resultProps().emessage());
		e.setTextContent(this.issues.get(tr.resultProps().issueId()).resultProps().etrace());		
	}
	
	private void populateExceptionDataForExcluded(Element e, TestResult tr) throws Exception{
		IssueProperties ip = this.issues.get(tr.resultProps().issueId()).resultProps();
		String msg = "Excluded because of ";
		switch (tr.resultProps().code()){
		case DATA_SOURCE_CONSTRUCTION_ERROR:
			msg += "Error in Data Source construction.";
			break;
		case DATA_SOURCE_NEXT_ERROR:
			msg += "Error in fetching next record from Data Source.";
			break;
		case ERROR_IN_SETUP_CLASS:
			msg += "Error in Set Up Class.";
			break;
		case ERROR_IN_SETUP_CLASS_FRAGMENT:
			msg += "Error in Set Up Class Fragment.";
			break;
		case ERROR_IN_SETUP_CLASS_INSTANCE:
			msg += "Error in Set Up Class Instance";
			break;
		case ERROR_IN_SETUP_METHOD:
			msg += "Error in Set Up Method.";
			break;
		case ERROR_IN_SETUP_METHOD_INSTANCE:
			msg += "Error in Set Up Method Instance.";
			break;
		case ERROR_IN_SETUP_TEST:
			msg += "Error in Set Up Test.";
			break;
		case TEST_CONTAINER_CONSTRUCTOR_ERROR:
			msg += "Error in Test Class Constructor.";
			break;
		case TEST_CONTAINER_DEPENDENCY_NOTMET:
			msg += String.format("Dependency on Test Class %s not met",  this.issues.get(tr.resultProps().issueId()).objectProps().qualifiedName());
			break;
		case TEST_CREATOR_DEPENDENCY_NOTMET:
			msg += String.format("Dependency on Test Method %s not met",  this.issues.get(tr.resultProps().issueId()).objectProps().qualifiedName());
			break;
		default:
			msg = ip.emessage();
		}
		e.setAttribute("message", msg);
		String trace = ip.emessage() + SystemBatteries.getLineSeparator();
		trace += ip.etrace();
		e.setTextContent(trace);		
	}
	
	public void update(TestResult testResult) throws Exception {
	   	HashMap<String, String> testAttributes = new HashMap<String, String>();
	   	testAttributes.put("name", testResult.objectProps().name());
	   	testAttributes.put("classname", testResult.objectProps().parentQualifiedName());

    	Double elapsedTime = testResult.objectProps().time();
    	testAttributes.put("time",  Double.toString(elapsedTime));
    	this.elapsedTime += elapsedTime;

		Element tc = dom.createElement("testcase");
		this.testCount += 1;
		for (String k: testAttributes.keySet()) {
			//Element prop =  dom.createElement("property");
			tc.setAttribute(k, testAttributes.get(k));
		}
		
		switch(testResult.resultProps().result()){
		case FAIL: 
			Element f = dom.createElement("failure");
			f.setAttribute("type", "failure");
			populateExceptionData(f, testResult);
			tc.appendChild(f);
			
			this.failCount += 1;
			break;
		case ERROR: 
			Element err = dom.createElement("error");
			err.setAttribute("type", "error");
			populateExceptionData(err, testResult);
			tc.appendChild(err);
			this.errCount += 1;
			break;
		case EXCLUDED: 
			Element sk = dom.createElement("skipped");
			sk.setAttribute("type", "excluded");
			populateExceptionDataForExcluded(sk, testResult);
			tc.appendChild(sk);
			
			this.skipCount += 1;
			break;
		}
//		} else if (testResult.wasSkipped()) {
//			Element s = dom.createElement("skipped");
//			s.setAttribute("type", "skipped");
//			s.setAttribute("message", reportRecord.get("MESSAGE"));
//			tc.appendChild(s);
//			
//			this.skipCount += 1;
//		}
		
//		if (testResult.getStdoutText() != null) {
//			Element s = dom.createElement("system-out");
//			s.setTextContent(testResult.getStdoutText());
//			tc.appendChild(s);					
//		}
//		
//		if (testResult.getStderrText() != null) {
//			Element s = dom.createElement("system-err");
//			s.setTextContent(testResult.getStderrText());
//			tc.appendChild(s);					
//		}
		
		testResultNodes.add(tc);
		//logger.debug("Add Test Result - Finish");
	}
	
	private String str(int i) {
		return Integer.toString(i);
	}
	
	public void tearDown() throws Exception {
		//logger.debug("Tear Down - Begin");
		try {
	    	tsAttributes.put("name", RunConfig.value("session.name").asString());
	    	tsAttributes.put("failures", str(this.failCount));
	    	tsAttributes.put("errors", str(this.errCount));
	    	tsAttributes.put("skipped", str(this.skipCount));
	    	tsAttributes.put("time", Double.toString(this.elapsedTime));
	    	tsAttributes.put("tests", str(this.testCount));
			
			for (String k: tsAttributes.keySet()) {
				testSuite.setAttribute((String) k, (String) tsAttributes.get(k));
			}
			
			for (Element t: this.testResultNodes) {
				testSuite.appendChild(t);
			}
			
			root.appendChild(testSuite);
	
			dom.appendChild(root);
	        Transformer tr = TransformerFactory.newInstance().newTransformer();
	        tr.setOutputProperty(OutputKeys.INDENT, "yes");
	        tr.setOutputProperty(OutputKeys.METHOD, "xml");
	        tr.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
	        tr.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
	
	        // send DOM to file
	        tr.transform(new DOMSource(dom), 
	                             new StreamResult(fileOut));
	
	    } catch (TransformerException te) {
	    	logger.error(te.getMessage());
	    } catch (IOException ioe) {
	        logger.error(ioe.getMessage());
	    }
		//logger.debug("Tear Down - Finish");
	}

	@Override
	public void update(Issue reportable) throws Exception {
		this.issues.put(reportable.resultProps().id(), reportable);
	}
	
	@Override
	public void update(IgnoredTest reportable) throws Exception {
		//do nothing
	}

	@Override
	public void update(Event reportable) throws Exception {
		// do nothing
	}

	@Override
	public void update(FixtureResult reportable) throws Exception {
		// do nothing
	}
}

//Based on the following understanding of what Jenkins can parse for JUnit XML files.
//
//<?xml version = "1.0" encoding = "utf-8"?>
//<testsuites errors = "1" failures = "1" tests = "4" time = "45">
//<testsuite errors = "1" failures = "1" hostname = "localhost" id = "0" name = "base_test_1"
//         package = "testdb" tests = "4" timestamp = "2012-11-15T01:02:29">
//  <properties>
//      <property name = "assert-passed" value = "1"/>
//  </properties>
//  <testcase classname = "testdb.directory" name = "001-passed-test" time = "10"/>
//  <testcase classname = "testdb.directory" name = "002-failed-test" time = "20">
//      <failure message = "Assertion FAILED: some failed assert" type = "failure">
//          the output of the testcase
//      </failure>
//  </testcase>
//  <testcase classname = "package.directory" name = "003-errord-test" time = "15">
//      <error message = "Assertion ERROR: some error assert" type = "error">
//          the output of the testcase
//      </error>
//  </testcase>
//	<testcase classname = "package.directory" name = "003-skipped-test" time = "0">
//	    <skipped message = "SKIPPED Test" type = "skipped">
//          the output of the testcase
//      </skipped>	
//	</testcase>
//  <testcase classname = "testdb.directory" name = "003-passed-test" time = "10">
//      <system-out>
//          I am system output
//      </system-out>
//      <system-err>
//          I am the error output
//      </system-err>
//  </testcase>
//</testsuite>
//</testsuites>


/*

@staticmethod
def to_file(file_descriptor, test_suites, prettyprint = True, encoding = None):
    """Writes the JUnit XML document to file"""
    file_descriptor.write(TestSuite.to_xml_string(test_suites, prettyprint, encoding))

@staticmethod
def _clean_illegal_xml_chars(string_to_clean):
    """Removes any illegal unicode characters from the given XML string"""
    # see http://stackoverflow.com/questions/1707890/fast-way-to-filter-illegal-xml-unicode-chars-in-python
    illegal_unichrs = [(0x00, 0x08), (0x0B, 0x1F), (0x7F, 0x84), (0x86, 0x9F),
                       (0xD800, 0xDFFF), (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF),
                       (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF), (0x3FFFE, 0x3FFFF),
                       (0x4FFFE, 0x4FFFF), (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF),
                       (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF), (0x9FFFE, 0x9FFFF),
                       (0xAFFFE, 0xAFFFF), (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF),
                       (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF), (0xFFFFE, 0xFFFFF),
                       (0x10FFFE, 0x10FFFF)]

    illegal_ranges = ["%s-%s" % (unichr(low), unichr(high))
                      for (low, high) in illegal_unichrs
                      if low < sys.maxunicode]

    illegal_xml_re = re.compile(u'[%s]' % u''.join(illegal_ranges))
    return illegal_xml_re.sub('', string_to_clean)
*/

