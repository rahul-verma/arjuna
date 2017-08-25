package pvt.unitee.reporter.lib.generator;

import java.util.List;

import org.apache.log4j.Logger;

import com.google.gson.JsonElement;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.interfaces.ReportGenerator;
import pvt.unitee.reporter.lib.ignored.IgnoredTest;
import pvt.unitee.reporter.lib.ignored.IgnoredTestDeserializer;
import pvt.unitee.reporter.lib.test.TestResult;
import pvt.unitee.reporter.lib.test.TestResultDeserializer;

public class IgnoredTestReportGenerator extends JsonResultsReader{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private IgnoredTestDeserializer deserializer = null;
	
	public IgnoredTestReportGenerator(List<ReportGenerator> generators) throws Exception{
		super(Batteries.value(ArjunaProperty.DIRECTORY_PROJECT_RUNID_REPORT_JSON_RAW_IGNOREDTESTS).asString(), generators);
		deserializer = new IgnoredTestDeserializer();
	}
	
	protected IgnoredTest getResultObject(JsonElement jElement){
		return deserializer.process(jElement.getAsJsonObject());
	}
	
	protected void update(JsonElement jElement) throws Exception {
		IgnoredTest reportable = this.getResultObject(jElement);
		for (ReportGenerator generator: this.getGenerators()){
			if (ArjunaInternal.displayReportGenerationInfo){
				logger.debug(String.format("%s: Updating: %s.", this.getClass().getSimpleName(), generator.getClass().getSimpleName()));
				logger.debug(String.format("Result Object: %s.", reportable.asJsonObject().toString()));
			}
			generator.update(reportable);
		}
	}

}
