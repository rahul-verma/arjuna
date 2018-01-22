package pvt.unitee.reporter.lib.writer.excel;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.IssueAttribute;
import pvt.unitee.reporter.lib.issue.Issue;
import unitee.enums.TestAttribute;
import unitee.enums.TestObjectAttribute;

class ExcelIssueWriter extends ExcelResultWriter<Issue> {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());

	private List<TestObjectAttribute> issueTestObjectProps = null;
	private List<TestAttribute> issueTestProps = null;
	private List<IssueAttribute> issueResultProps = null;	
	private List<String> issueHeaders = new ArrayList<String>();
	
	private boolean shouldIncludeAnnotatedTestProps = false;

	public ExcelIssueWriter(HSSFWorkbook workbook) throws Exception {
		super(workbook, "Issues");
	}

	public void setUp() throws Exception {
		// Populate meta-data
		Map<TestObjectAttribute,String> testObjectNames = ArjunaInternal.getTestObjectAttrNameMap();
		Map<TestAttribute,String> testPropNames = ArjunaInternal.getTestAttrNameMap();
	
		Map<IssueAttribute,String> fixtureResultPropNames = ArjunaInternal.getIssueAttrNameMap();
		issueTestObjectProps = ArjunaInternal.getTestObjectAttrListForIssueReport();
		issueTestProps = ArjunaInternal.getTestAttrList();
		issueResultProps = ArjunaInternal.getIssueAttrList();
		
		shouldIncludeAnnotatedTestProps = ArjunaInternal.shouldIncludeAnnotatedTestPropsInReport();

		for (IssueAttribute prop: issueResultProps){
			this.issueHeaders.add(fixtureResultPropNames.get(prop));
		}	

		for (TestObjectAttribute prop: issueTestObjectProps){
			this.issueHeaders.add(testObjectNames.get(prop));
		}
		
		if (shouldIncludeAnnotatedTestProps){
			for (TestAttribute prop: issueTestProps){
				this.issueHeaders.add(testPropNames.get(prop));
			}
		}
		
		super.setUp();
		super.setHeaders(this.issueHeaders);
		super.writeHeader();
	}	

	public void update(Issue reportable) throws Exception {
		List<String> resultArr = new ArrayList<String>();
		resultArr.addAll(reportable.resultPropStrings(this.issueResultProps));
		resultArr.addAll(reportable.objectPropStrings(this.issueTestObjectProps));
		if (shouldIncludeAnnotatedTestProps){
			resultArr.addAll(reportable.testPropStrings(this.issueTestProps));
		}
		writeData(resultArr);
	}

}