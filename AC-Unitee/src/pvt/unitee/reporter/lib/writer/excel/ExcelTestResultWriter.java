package pvt.unitee.reporter.lib.writer.excel;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.interfaces.Value;
import arjunasdk.sysauto.batteries.SystemBatteries;
import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.TestReportSection;
import pvt.unitee.enums.TestResultAttribute;
import pvt.unitee.reporter.lib.test.TestResult;
import unitee.enums.TestAttribute;
import unitee.enums.TestObjectAttribute;

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

