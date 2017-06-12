package pvt.unitee.reporter.lib.writer.excel;

import java.io.File;
import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;
import org.apache.poi.hssf.usermodel.HSSFCell;
import org.apache.poi.hssf.usermodel.HSSFCellStyle;
import org.apache.poi.hssf.usermodel.HSSFRow;
import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.Font;
import org.apache.poi.ss.usermodel.IndexedColors;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.interfaces.Value;
import arjunasdk.sysauto.batteries.SystemBatteries;
import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.enums.EventAttribute;
import pvt.unitee.enums.FixtureResultPropertyType;
import pvt.unitee.enums.IssueAttribute;
import pvt.unitee.enums.StepResultAttribute;
import pvt.unitee.enums.TestReportSection;
import pvt.unitee.enums.TestResultAttribute;
import pvt.unitee.enums.TestResultType;
import pvt.unitee.interfaces.ReportGenerator;
import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.fixture.FixtureResult;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.step.StepResult;
import pvt.unitee.reporter.lib.test.TestResult;
import unitee.enums.TestAttribute;
import unitee.enums.TestObjectAttribute;
import unitee.interfaces.TestVariables;

public class ExcelReportGenerator implements ReportGenerator{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private FileOutputStream fileOut = null;
	private HSSFWorkbook workbook = null;
	HSSFCellStyle cellStyle = null;
	HSSFCellStyle topRowStyle = null;
	HSSFCellStyle lastCellStyle = null;
	private ExcelTestResultWriter testResultSheet = null;
	private ExcelIssueWriter issuesResultSheet = null;
	private ExcelEventWriter eventSheet = null;
	private ExcelFixtureResultWriter fixtureSheet = null;
	private Set<TestResultType> allowedRTypes = null;
	
	public ExcelReportGenerator(String reportDir) throws Exception {
		FileUtils.forceMkdir(new File(reportDir));
		fileOut  = new FileOutputStream(reportDir + "/" + Batteries.value(ArjunaProperty.REPORT_NAME_FORMAT).asString() + ".xls");
		this.allowedRTypes = ArjunaInternal.getReportableTestTypes();
	}
	
	private void createWorkBook() throws Exception{
		workbook = new HSSFWorkbook();
		cellStyle = workbook.createCellStyle();
		cellStyle.setBorderLeft((short) 1);
		cellStyle.setBorderRight((short) 1);
		cellStyle.setBorderTop((short) 1);
		cellStyle.setBorderBottom((short) 1);
		cellStyle.setWrapText(true);
		cellStyle.setVerticalAlignment((short) 1);

		lastCellStyle = workbook.createCellStyle();
		lastCellStyle.setBorderLeft((short) 1);
		lastCellStyle.setBorderRight((short) 1);
		lastCellStyle.setBorderTop((short) 1);
		lastCellStyle.setBorderBottom((short) 1);
		lastCellStyle.setWrapText(true);
		lastCellStyle.setVerticalAlignment((short) 0);

		Font font = workbook.createFont();
		font.setBold(true);
		font.setItalic(false);
		topRowStyle = workbook.createCellStyle();
		topRowStyle.setBorderLeft((short) 1);
		topRowStyle.setBorderRight((short) 1);
		topRowStyle.setBorderTop((short) 1);
		topRowStyle.setBorderBottom((short) 1);
		topRowStyle.setWrapText(true);
		topRowStyle.setVerticalAlignment((short) 1);
		topRowStyle.setFillForegroundColor(IndexedColors.AQUA.getIndex());
		topRowStyle.setFillPattern(CellStyle.SOLID_FOREGROUND);
		topRowStyle.setFont(font);		
	}

	@Override
	public void setUp() throws Exception {
		createWorkBook();
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.TESTS)){
			testResultSheet = new ExcelTestResultWriter(workbook);
			testResultSheet.setStyles(cellStyle, topRowStyle, lastCellStyle);
			testResultSheet.setUp();
		}
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.ISSUES)){
			issuesResultSheet = new ExcelIssueWriter(workbook);
			issuesResultSheet.setStyles(cellStyle, topRowStyle, lastCellStyle);
			issuesResultSheet.setUp();
		}
		
		
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.FIXTURES)){
			fixtureSheet = new ExcelFixtureResultWriter(workbook);
			fixtureSheet.setStyles(cellStyle, topRowStyle, lastCellStyle);
			fixtureSheet.setUp();	
		}
		
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.EVENTS)){
			eventSheet = new ExcelEventWriter(workbook);
			eventSheet.setStyles(cellStyle, topRowStyle, lastCellStyle);
			eventSheet.setUp();	
		}
	}

	public void tearDown() throws Exception {
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.TESTS)){
			testResultSheet.tearDown();
		}
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.ISSUES)){
			issuesResultSheet.tearDown();
		}
		
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.FIXTURES)){
			fixtureSheet.tearDown();
		}
		
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.EVENTS)){
			eventSheet.tearDown();
		}
		workbook.write(fileOut);
		fileOut.close();
		logger.debug("Tear Down - Finish");
	}

	@Override
	public synchronized void update(TestResult reportable) throws Exception {
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.TESTS)){
			if (allowedRTypes.contains(reportable.resultProps().result())){
				testResultSheet.update(reportable);
			}
		}
	}

	@Override
	public synchronized void update(Issue reportable) throws Exception {
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.ISSUES)){
			issuesResultSheet.update(reportable);
		}
	}
	
	@Override
	public synchronized void update(FixtureResult reportable) throws Exception {
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.FIXTURES)){
			fixtureSheet.update(reportable);
		}
	}

	@Override
	public synchronized void update(Event reportable) throws Exception {
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.EVENTS)){
			eventSheet.update(reportable);
		}
	}

}

abstract class ExcelResultWriter<T>{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private String reportTypeLabel = null;
	private HSSFSheet sheet = null;
	private int currentRow = -1;
	private int lastColumnNumber;
	private List<String> headers = null;
	HSSFCellStyle cellStyle = null;
	HSSFCellStyle topRowStyle = null;
	HSSFCellStyle lastCellStyle = null;
	HSSFWorkbook workbook = null;
	HSSFCellStyle currentStyle = null;

	public ExcelResultWriter(HSSFWorkbook workbook, String reportTypeLabel) throws Exception {
		this.workbook = workbook;
		this.reportTypeLabel = reportTypeLabel;
	}
	
	public void setStyles(HSSFCellStyle cStyle, HSSFCellStyle tStyle, HSSFCellStyle lStyle){
		cellStyle = cStyle;
		topRowStyle = tStyle;
		lastCellStyle = lStyle;		
	}
	
	protected void setHeaders(List<String> headers){
		this.headers  = headers;
		this.lastColumnNumber = headers.size();
	}
	
	protected List<String> getHeaders(){
		return this.headers;
	}
	
	protected void writeHeader() throws Exception{
		this.writeExcelRow(this.headers, true);
	}
	
	protected void writeData(List<String> values) throws Exception{
		this.writeExcelRow(values, false);		
	}

	private void writeExcelRow(List<String> values, boolean headerRow) throws Exception {
		//		logger.debug("Writing Excel Row in " + sheet.getSheetName());
		//		logger.debug("Record: " + DataBatteries.flatten(row));
		if (headerRow) {
			currentStyle = this.topRowStyle;
		} else {
			currentStyle = this.cellStyle;
		}
		HSSFRow excelRow = null;
		currentRow += 1;
		excelRow = sheet.createRow(currentRow);

		//excelRow.setRowStyle(currentStyle);
		for (int i = 0; i < values.size(); i++) {
			HSSFCell cell = excelRow.createCell(i);
			cell.setCellType(HSSFCell.CELL_TYPE_STRING);
			if (values.get(i).length() < 32767){
				cell.setCellValue(values.get(i));
			} else {
				cell.setCellValue("!!EXCEL LIMIT FOR CELL EXCCEEDED. Ignoring content of this cell.!!!");
			}
			if (!headerRow) {
				if (i == lastColumnNumber) {
					cell.setCellStyle(lastCellStyle);
				} else {
					cell.setCellStyle(currentStyle);
				}
				if (values.get(i) != "") {
					excelRow.setHeightInPoints(5 * sheet.getDefaultRowHeightInPoints());
				}
			} else {
				excelRow.setHeightInPoints(2 * sheet.getDefaultRowHeightInPoints());
				cell.setCellStyle(currentStyle); 
			}


			//sheet.autoSizeColumn((short) 1);
		}
		//sheet.autoSizeColumn((short) 1);
	}


	public void setUp() throws Exception {
		sheet = workbook.createSheet(reportTypeLabel);
	}	

	public void tearDown() throws Exception {
		logger.debug("Tear Down - Begin");
		for (int i = 0; i < this.headers.size(); i++) {
			sheet.autoSizeColumn(i);
		}
		logger.debug("Tear Down - Finish");
	}
}

class ExcelTestResultWriter extends ExcelResultWriter<TestResult>{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private List<TestObjectAttribute> execTestObjectProps = null;
	private List<TestAttribute> execTestProps = null;
	private List<TestResultAttribute> execResultProps = null;
	private List<String> execHeaders = new ArrayList<String>();
	private ExcelStepResultWriter stepWriter = null;
	
	private boolean shouldIncludeAnnotatedTestProps = false;
	private boolean shouldIncludeAttr = false;
	private boolean shouldIncludeExecVars = false;
	private boolean shouldIncludeDataRecord = false;
	private boolean shouldIncludeDataRef = false;
	
	Gson gson = new GsonBuilder().setPrettyPrinting().create();

	public ExcelTestResultWriter(HSSFWorkbook workbook) throws Exception {
		super(workbook, "Test Execution Results");
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.STEPS)){
			stepWriter = new ExcelStepResultWriter(workbook);
		}
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
		
//		if (shouldIncludeDataRef){
//			this.execHeaders.add("Data Reference(s)");
//		}
		
		super.setUp();
		super.setHeaders(this.execHeaders);
		super.writeHeader();
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.STEPS)){
			stepWriter.setStyles(cellStyle, topRowStyle, lastCellStyle);
			stepWriter.setUp();
		}
	}	

	public void update(TestResult reportable) throws Exception {
		List<String> resultArr = new ArrayList<String>();
		resultArr.addAll(reportable.objectPropStrings(this.execTestObjectProps));
		if (shouldIncludeAnnotatedTestProps){
			resultArr.addAll(reportable.testPropStrings(this.execTestProps));
		}
		resultArr.addAll(reportable.resultPropStrings(this.execResultProps));
		
		if (shouldIncludeAttr){
			StringBuilder cb = new StringBuilder();
			Map<String,Value> cmap = reportable.attr().items();
			if (cmap.size() == 0){
				cb.append("NA");
			} else {
				for (String k: cmap.keySet()){
					cb.append(String.format("[%s] %s%s", k, cmap.get(k).asString(), SystemBatteries.getLineSeparator()));
				}
			}
			
			String cbString = cb.toString();
			if (cbString.length() > 32766){
				cbString = ("TOO_LENGTHY_FOR_EXCEL_CELL");
			}
			resultArr.add(cb.toString());
		}
		
		if (shouldIncludeExecVars){
			StringBuilder ub = new StringBuilder();
			Map<String,Value> umap = reportable.execVars().items();
			if (umap.size() == 0){
				ub.append("NA");
			} else {
				for (String k: umap.keySet()){
					ub.append(String.format("[%s] %s%s", k, umap.get(k).asString(), SystemBatteries.getLineSeparator()));
				}
			}
			
			String ubString = ub.toString();
			if (ubString.length() > 32766){
				ubString = ("TOO_LENGTHY_FOR_EXCEL_CELL");
			}
			
			resultArr.add(ubString);
		}
		
		if (this.shouldIncludeDataRecord){
			StringBuilder ub = new StringBuilder();
			DataRecord dr = reportable.testVars().record();
			if (dr != null){
				Map<String,Value> dmap = dr.items();
				if (dmap.size() == 0){
					ub.append("NA");
				} else {
					List<String> ar = new ArrayList<String>();
					String[] arr = dmap.keySet().toArray(new String[0]);
					Arrays.sort(arr);
					for (String k: arr){
						ub.append(String.format("[%s] %s%s", k, dmap.get(k).asString(), SystemBatteries.getLineSeparator()));
					}
				}
			} else {
				ub.append("NA");
			}
			
			String ubString = ub.toString();
			if (ubString.length() > 32766){
				ubString = ("TOO_LENGTHY_FOR_EXCEL_CELL");
			}
			
			resultArr.add(ubString);
		}
		
		writeData(resultArr);
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.STEPS)){
			this.stepWriter.update(reportable.testVars(), reportable.stepResults());
		}
	}	
	
	public void tearDown() throws Exception{
		super.tearDown();
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.STEPS)){
			this.stepWriter.tearDown();
		}
	}

}

class ExcelStepResultWriter extends ExcelResultWriter<StepResult> {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());

	private List<TestObjectAttribute> stepTestObjectProps = null;
	private List<TestAttribute> stepTestProps = null;
	private List<StepResultAttribute> stepResultProps = null;	
	private List<String> stepHeaders = new ArrayList<String>();
	
	private boolean shouldIncludeAnnotatedTestProps = false;
	
	public ExcelStepResultWriter(HSSFWorkbook workbook) throws Exception {
		super(workbook, "Test Step Results");
	}

	public void setUp() throws Exception {
		// Populate meta-data
		Map<TestObjectAttribute,String> testObjectNames = ArjunaInternal.getTestObjectAttrNameMap();
		Map<TestAttribute,String> testPropNames = ArjunaInternal.getTestAttrNameMap();
		
		// Step Result Section
		Map<StepResultAttribute,String> stepResultPropNames = ArjunaInternal.getStepResultAttrNameMap();
		stepTestObjectProps = ArjunaInternal.getTestObjectAttrListForStepReport();
		stepTestProps = ArjunaInternal.getTestAttrList();
		stepResultProps = ArjunaInternal.getStepResultAttrList();
		
		shouldIncludeAnnotatedTestProps = ArjunaInternal.shouldIncludeAnnotatedTestPropsInReport();
		
		for (TestObjectAttribute prop: stepTestObjectProps){
			this.stepHeaders.add(testObjectNames.get(prop));
		}
		
		if (shouldIncludeAnnotatedTestProps){
			for (TestAttribute prop: stepTestProps){
				this.stepHeaders.add(testPropNames.get(prop));
			}
		}
		for (StepResultAttribute prop: stepResultProps){
			this.stepHeaders.add(stepResultPropNames.get(prop));
		}
		
		super.setUp();
		super.setHeaders(this.stepHeaders);
		super.writeHeader();
	}	
	
	public void update(StepResult reportable) throws Exception {
		throw new Exception("Does not support this. Use update(TestVariables, List<StepResult>)");
	}
	
	public void update(TestVariables testVars, List<StepResult> reportables) throws Exception {
		List<String> testRelated = new ArrayList<String>(); 
		testRelated.addAll(testVars.object().strings(this.stepTestObjectProps));
		if (shouldIncludeAnnotatedTestProps){
			testRelated.addAll(testVars.test().strings(this.stepTestProps));
		}
		for (StepResult reportable: reportables){
			List<String> resultArr = new ArrayList<String>(); 
			resultArr.addAll(testRelated);
			resultArr.addAll(reportable.resultPropStrings(this.stepResultProps));
			writeData(resultArr);
		}

	}

}

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

class ExcelFixtureResultWriter extends ExcelResultWriter<FixtureResult> {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());

	private List<TestObjectAttribute> fixtureTestObjectProps = null;
	private List<FixtureResultPropertyType> fixtureResultProps = null;	
	private List<String> fixtureHeaders = new ArrayList<String>();

	public ExcelFixtureResultWriter(HSSFWorkbook workbook) throws Exception {
		super(workbook, "Fixtures");
	}

	public void setUp() throws Exception {
		// Populate meta-data
		Map<TestObjectAttribute,String> testObjectNames = ArjunaInternal.getTestObjectAttrNameMap();
	
		Map<FixtureResultPropertyType,String> fixtureResultPropNames = ArjunaInternal.getFixtureResultAttrNameMap();
		fixtureTestObjectProps = ArjunaInternal.getTestObjectAttrListForFixtureReport();
		fixtureResultProps = ArjunaInternal.getFixtureResultAttrList();

		for (TestObjectAttribute prop: fixtureTestObjectProps){
			this.fixtureHeaders.add(testObjectNames.get(prop));
		}
		
		for (FixtureResultPropertyType prop: fixtureResultProps){
			this.fixtureHeaders.add(fixtureResultPropNames.get(prop));
		}	
		
		super.setUp();
		super.setHeaders(this.fixtureHeaders);
		super.writeHeader();
	}	

	public void update(FixtureResult reportable) throws Exception {
		List<String> resultArr = new ArrayList<String>();
		resultArr.addAll(reportable.objectPropStrings(this.fixtureTestObjectProps));
		resultArr.addAll(reportable.resultPropStrings(this.fixtureResultProps));
		writeData(resultArr);
	}

}

class ExcelEventWriter extends ExcelResultWriter<Event> {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());

	private List<EventAttribute> eventAttrs = null;
	private List<String> eventHeaders = new ArrayList<String>();

	public ExcelEventWriter(HSSFWorkbook workbook) throws Exception {
		super(workbook, "Events");
	}

	public void setUp() throws Exception {
		Map<EventAttribute,String> activityPropNames = ArjunaInternal.getEventAttrNameMap();
		eventAttrs = ArjunaInternal.getEventAttrList();		
		for (EventAttribute prop: eventAttrs){
			this.eventHeaders.add(activityPropNames.get(prop));
		}		
		
		super.setUp();
		super.setHeaders(this.eventHeaders);
		super.writeHeader();
	}	

	public void update(Event reportable) throws Exception {
		writeData(reportable.infoPropStrings(this.eventAttrs));
	}

}

