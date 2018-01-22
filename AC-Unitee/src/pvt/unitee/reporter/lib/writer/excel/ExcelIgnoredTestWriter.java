package pvt.unitee.reporter.lib.writer.excel;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.IgnoredTestAttribute;
import pvt.unitee.reporter.lib.ignored.IgnoredTest;
import unitee.enums.TestObjectAttribute;

class ExcelIgnoredTestWriter extends ExcelResultWriter<IgnoredTest> {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());

	private List<TestObjectAttribute> ignoredTestObjectProps = null;
	private List<IgnoredTestAttribute> ignoredTestProps = null;	
	private List<String> ignoredTestHeaders = new ArrayList<String>();

	public ExcelIgnoredTestWriter(HSSFWorkbook workbook) throws Exception {
		super(workbook, "Skipped and Unpicked");
	}

	public void setUp() throws Exception {
		// Populate meta-data
		Map<TestObjectAttribute,String> testObjectNames = ArjunaInternal.getTestObjectAttrNameMap();
		Map<IgnoredTestAttribute,String> ignoredTestPropNameMap = ArjunaInternal.getIgnoredTestAttrNameMap();
		
		ignoredTestObjectProps = ArjunaInternal.getTestObjectAttrListForIgnoredTestReport();
		ignoredTestProps = ArjunaInternal.getIgnoredTestAttrList();

		for (TestObjectAttribute prop: ignoredTestObjectProps){
			this.ignoredTestHeaders.add(testObjectNames.get(prop));
		}
		
		for (IgnoredTestAttribute prop: ignoredTestProps){
			this.ignoredTestHeaders.add(ignoredTestPropNameMap.get(prop));
		}	
		
		super.setUp();
		super.setHeaders(this.ignoredTestHeaders);
		super.writeHeader();
	}	

	public void update(IgnoredTest reportable) throws Exception {
		List<String> resultArr = new ArrayList<String>();
		resultArr.addAll(reportable.objectPropStrings(this.ignoredTestObjectProps));
		resultArr.addAll(reportable.resultPropStrings(this.ignoredTestProps));
		writeData(resultArr);
	}

}

