package com.autocognite.pvt.unitee.reporter.lib.generator;

import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.arjuna.interfaces.ReportGenerator;
import com.autocognite.pvt.unitee.reporter.lib.issue.Issue;
import com.autocognite.pvt.unitee.reporter.lib.issue.IssueDeserializer;
import com.google.gson.JsonElement;

public class IssueReportGenerator extends JsonResultsReader{
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private IssueDeserializer deserializer = null;
	
	public IssueReportGenerator(List<ReportGenerator> generators) throws Exception{
		super(RunConfig.value(ArjunaProperty.DIRECTORY_RUNID_REPORT_JSON_RAW_ISSUES).asString(), generators);
		deserializer = new IssueDeserializer();
	}
	
	protected Issue getResultObject(JsonElement jElement){
		return deserializer.process(jElement.getAsJsonObject());
	}

	protected void update(JsonElement jElement) throws Exception {
		Issue reportable = this.getResultObject(jElement);
		for (ReportGenerator generator: this.getGenerators()){
			if (ArjunaInternal.displayReportGenerationInfo){
				logger.debug(String.format("%s: Updating: %s.", this.getClass().getSimpleName(), generator.getClass().getSimpleName()));
			}
			generator.update(reportable);
		}
	}
}
