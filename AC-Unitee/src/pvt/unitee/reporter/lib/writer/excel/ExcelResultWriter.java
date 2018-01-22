package pvt.unitee.reporter.lib.writer.excel;

import java.util.List;

import org.apache.log4j.Logger;
import org.apache.poi.hssf.usermodel.HSSFCell;
import org.apache.poi.hssf.usermodel.HSSFCellStyle;
import org.apache.poi.hssf.usermodel.HSSFRow;
import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;

import pvt.batteries.config.Batteries;
import pvt.unitee.reporter.lib.DefaultObserver;

abstract class ExcelResultWriter<T> extends DefaultObserver<T>{
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
