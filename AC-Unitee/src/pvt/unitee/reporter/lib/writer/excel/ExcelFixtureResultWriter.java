package pvt.unitee.reporter.lib.writer.excel;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.FixtureResultPropertyType;
import pvt.unitee.reporter.lib.fixture.FixtureResult;
import unitee.enums.TestObjectAttribute;

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
