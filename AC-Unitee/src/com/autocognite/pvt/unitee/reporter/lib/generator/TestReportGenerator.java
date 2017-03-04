package com.autocognite.pvt.unitee.reporter.lib.generator;

import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.batteries.config.RunConfig;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.arjuna.interfaces.InternalReportGenerator;
import com.autocognite.pvt.unitee.reporter.lib.test.TestResult;
import com.autocognite.pvt.unitee.reporter.lib.test.TestResultDeserializer;
import com.google.gson.JsonElement;

public class TestReportGenerator extends JsonResultsReader{
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private TestResultDeserializer deserializer = null;
	
	public TestReportGenerator(List<InternalReportGenerator> generators) throws Exception{
		super(RunConfig.value(ArjunaProperty.DIRECTORY_RUNID_REPORT_JSON_RAW_TESTS).asString(), generators);
		deserializer = new TestResultDeserializer();
	}
	
	protected TestResult getResultObject(JsonElement jElement){
		return deserializer.process(jElement.getAsJsonObject());
	}
	
	protected void update(JsonElement jElement) throws Exception {
		TestResult reportable = this.getResultObject(jElement);
		for (InternalReportGenerator generator: this.getGenerators()){
			if (ArjunaInternal.displayReportGenerationInfo){
				logger.debug(String.format("%s: Updating: %s.", this.getClass().getSimpleName(), generator.getClass().getSimpleName()));
				logger.debug(String.format("Result Object: %s.", reportable.asJsonObject().toString()));
			}
			generator.update(reportable);
		}
	}

}
