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
import pvt.unitee.enums.IgnoredTestAttribute;
import pvt.unitee.enums.IgnoredTestStatus;
import pvt.unitee.enums.IssueAttribute;
import pvt.unitee.enums.StepResultAttribute;
import pvt.unitee.enums.TestReportSection;
import pvt.unitee.enums.TestResultAttribute;
import pvt.unitee.enums.TestResultType;
import pvt.unitee.reporter.lib.BasePrivateCompositeReporter;
import pvt.unitee.reporter.lib.DefaultObserver;
import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.fixture.FixtureResult;
import pvt.unitee.reporter.lib.ignored.IgnoredTest;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.step.StepResult;
import pvt.unitee.reporter.lib.test.TestResult;
import unitee.enums.TestAttribute;
import unitee.enums.TestObjectAttribute;
import unitee.interfaces.Reporter;
import unitee.interfaces.TestVariables;

public class ExcelReporter extends BasePrivateCompositeReporter implements Reporter{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private FileOutputStream fileOut = null;
	private HSSFWorkbook workbook = null;
	HSSFCellStyle cellStyle = null;
	HSSFCellStyle topRowStyle = null;
	HSSFCellStyle lastCellStyle = null;
	
	public ExcelReporter(String reportDir) throws Exception {
		super();
		FileUtils.forceMkdir(new File(reportDir));
		fileOut  = new FileOutputStream(reportDir + "/" + Batteries.value(ArjunaProperty.REPORT_NAME_FORMAT).asString() + ".xls");
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
			ExcelTestResultWriter testResultSheet = new ExcelTestResultWriter(workbook);
			testResultSheet.setStyles(cellStyle, topRowStyle, lastCellStyle);
			testResultSheet.setUp();
			this.setTestResultObserver(testResultSheet);
		}
		
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.ISSUES)){
			ExcelIssueWriter issuesResultSheet = new ExcelIssueWriter(workbook);
			issuesResultSheet.setStyles(cellStyle, topRowStyle, lastCellStyle);
			issuesResultSheet.setUp();
			this.setIssueObserver(issuesResultSheet);
		}
		
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.IGNORED_TESTS)){
			ExcelIgnoredTestWriter ignoredTestSheet = new ExcelIgnoredTestWriter(workbook);
			ignoredTestSheet.setStyles(cellStyle, topRowStyle, lastCellStyle);
			ignoredTestSheet.setUp();
			this.setIgnoredTestObserver(ignoredTestSheet);
		}
		
		
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.FIXTURES)){
			ExcelFixtureResultWriter fixtureSheet = new ExcelFixtureResultWriter(workbook);
			fixtureSheet.setStyles(cellStyle, topRowStyle, lastCellStyle);
			fixtureSheet.setUp();	
			this.setFixtureResultObserver(fixtureSheet);
		}
		
		if (ArjunaInternal.shouldIncludedReportSection(TestReportSection.EVENTS)){
			ExcelEventWriter eventSheet = new ExcelEventWriter(workbook);
			eventSheet.setStyles(cellStyle, topRowStyle, lastCellStyle);
			eventSheet.setUp();	
			this.setEventObserver(eventSheet);
		}
	}

	public void tearDown() throws Exception {
		super.tearDown();
		workbook.write(fileOut);
		fileOut.close();
		logger.debug("Tear Down - Finish");
	}
}