package pvt.unitee.reporter.lib.writer.excel;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.StepResultAttribute;
import pvt.unitee.reporter.lib.step.StepResult;
import unitee.enums.TestAttribute;
import unitee.enums.TestObjectAttribute;
import unitee.interfaces.TestVariables;

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


