package pvt.unitee.reporter.lib.generator;

import java.util.List;

import org.apache.log4j.Logger;

import com.google.gson.JsonElement;

import pvt.arjunapro.ArjunaInternal;
import pvt.batteries.config.Batteries;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.interfaces.ReportGenerator;
import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.event.EventDeserializer;

public class ActivityReportGenerator extends JsonResultsReader{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private EventDeserializer deserializer = null;
	
	public ActivityReportGenerator(List<ReportGenerator> generators) throws Exception{
		super(Batteries.value(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_EVENTS).asString(), generators);
		deserializer = new EventDeserializer();
	}
	
	protected Event getResultObject(JsonElement jElement){
		return deserializer.process(jElement.getAsJsonObject());
	}

	protected void update(JsonElement jElement) throws Exception {
		Event reportable = this.getResultObject(jElement);
		for (ReportGenerator generator: this.getGenerators()){
			if (ArjunaInternal.displayReportGenerationInfo){
				logger.debug(String.format("%s: Updating: %s.", this.getClass().getSimpleName(), generator.getClass().getSimpleName()));
			}
			generator.update(reportable);
		}
	}
}
