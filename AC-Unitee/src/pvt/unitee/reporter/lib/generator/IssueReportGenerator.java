package pvt.unitee.reporter.lib.generator;

import java.util.List;

import org.apache.log4j.Logger;

import com.arjunapro.pvt.ArjunaInternal;
import com.google.gson.JsonElement;

import pvt.arjunapro.enums.ArjunaProperty;
import pvt.arjunapro.interfaces.ReportGenerator;
import pvt.batteries.config.Batteries;
import pvt.unitee.reporter.lib.issue.Issue;
import pvt.unitee.reporter.lib.issue.IssueDeserializer;

public class IssueReportGenerator extends JsonResultsReader{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private IssueDeserializer deserializer = null;
	
	public IssueReportGenerator(List<ReportGenerator> generators) throws Exception{
		super(Batteries.value(ArjunaProperty.DIRECTORY_RUNID_REPORT_JSON_RAW_ISSUES).asString(), generators);
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
