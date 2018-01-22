package pvt.unitee.reporter.lib.writer.excel;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.EventAttribute;
import pvt.unitee.reporter.lib.event.Event;

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

