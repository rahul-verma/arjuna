package com.autocognite.pvt.unitee.reporter.lib.generator;

import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.arjuna.interfaces.ReportGenerator;
import com.autocognite.pvt.unitee.reporter.lib.fixture.FixtureResult;
import com.autocognite.pvt.unitee.reporter.lib.fixture.FixtureResultDeserializer;
import com.autocognite.pvt.unitee.reporter.lib.test.TestResult;
import com.autocognite.pvt.unitee.reporter.lib.test.TestResultDeserializer;
import com.google.gson.JsonElement;

public class FixtureReportGenerator extends JsonResultsReader{
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private FixtureResultDeserializer deserializer = null;
	
	public FixtureReportGenerator(List<ReportGenerator> generators) throws Exception{
		super(RunConfig.value(ArjunaProperty.DIRECTORY_RUNID_REPORT_JSON_RAW_FIXTURES).asString(), generators);
		deserializer = new FixtureResultDeserializer();
	}
	
	protected FixtureResult getResultObject(JsonElement jElement){
		return deserializer.process(jElement.getAsJsonObject());
	}
	
	protected void update(JsonElement jElement) throws Exception {
		FixtureResult reportable = this.getResultObject(jElement);
		for (ReportGenerator generator: this.getGenerators()){
			if (ArjunaInternal.displayReportGenerationInfo){
				logger.debug(String.format("%s: Updating: %s.", this.getClass().getSimpleName(), generator.getClass().getSimpleName()));
				logger.debug(String.format("Result Object: %s.", reportable.asJsonObject().toString()));
			}
			generator.update(reportable);
		}
	}

}
