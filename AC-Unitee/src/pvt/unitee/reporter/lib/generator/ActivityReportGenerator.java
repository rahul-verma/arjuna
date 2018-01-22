package pvt.unitee.reporter.lib.generator;

import java.util.List;

import org.apache.log4j.Logger;

import com.google.gson.JsonElement;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.event.EventDeserializer;
import unitee.interfaces.Reporter;

public class ActivityReportGenerator extends JsonResultsReader{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private EventDeserializer deserializer = null;
	
	public ActivityReportGenerator(List<Reporter> generators) throws Exception{
		super(Batteries.value(ArjunaProperty.PROJECT_RUN_REPORT_JSON_EVENTS_DIR).asString(), generators);
		deserializer = new EventDeserializer();
	}
	
	protected Event getResultObject(JsonElement jElement){
		return deserializer.process(jElement.getAsJsonObject());
	}

	protected void update(JsonElement jElement) throws Exception {
		Event reportable = this.getResultObject(jElement);
		for (Reporter generator: this.getGenerators()){
			if (ArjunaInternal.displayReportGenerationInfo){
				logger.debug(String.format("%s: Updating: %s.", this.getClass().getSimpleName(), generator.getClass().getSimpleName()));
			}
			generator.update(reportable);
		}
	}
}
