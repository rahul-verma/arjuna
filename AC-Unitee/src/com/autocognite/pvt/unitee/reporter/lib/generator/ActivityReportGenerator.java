package com.autocognite.pvt.unitee.reporter.lib.generator;

import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.arjuna.interfaces.InternalReportGenerator;
import com.autocognite.pvt.unitee.reporter.lib.event.Event;
import com.autocognite.pvt.unitee.reporter.lib.event.EventDeserializer;
import com.google.gson.JsonElement;

public class ActivityReportGenerator extends JsonResultsReader{
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private EventDeserializer deserializer = null;
	
	public ActivityReportGenerator(List<InternalReportGenerator> generators) throws Exception{
		super(RunConfig.value(ArjunaProperty.DIRECTORY_RUNID_REPORT_JSON_RAW_EVENTS).asString(), generators);
		deserializer = new EventDeserializer();
	}
	
	protected Event getResultObject(JsonElement jElement){
		return deserializer.process(jElement.getAsJsonObject());
	}

	protected void update(JsonElement jElement) throws Exception {
		Event reportable = this.getResultObject(jElement);
		for (InternalReportGenerator generator: this.getGenerators()){
			if (ArjunaInternal.displayReportGenerationInfo){
				logger.debug(String.format("%s: Updating: %s.", this.getClass().getSimpleName(), generator.getClass().getSimpleName()));
			}
			generator.update(reportable);
		}
	}
}
