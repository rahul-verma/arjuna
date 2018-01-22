package pvt.unitee.reporter.lib.generator;

import java.util.List;

import org.apache.log4j.Logger;

import com.google.gson.JsonElement;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.issue.IssueDeserializer;
import unitee.interfaces.Reporter;

public class IssueReportGenerator extends JsonResultsReader{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private IssueDeserializer deserializer = null;
	
	public IssueReportGenerator(List<Reporter> generators) throws Exception{
		super(Batteries.value(ArjunaProperty.PROJECT_RUN_REPORT_JSON_ISSUES_DIR).asString(), generators);
		deserializer = new IssueDeserializer();
	}
	
	protected Issue getResultObject(JsonElement jElement){
		return deserializer.process(jElement.getAsJsonObject());
	}

	protected void update(JsonElement jElement) throws Exception {
		Issue reportable = this.getResultObject(jElement);
		for (Reporter generator: this.getGenerators()){
			if (ArjunaInternal.displayReportGenerationInfo){
				logger.debug(String.format("%s: Updating: %s.", this.getClass().getSimpleName(), generator.getClass().getSimpleName()));
			}
			generator.update(reportable);
		}
	}
}
