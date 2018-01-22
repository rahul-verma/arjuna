package pvt.unitee.reporter.lib.generator;

import java.util.List;

import org.apache.log4j.Logger;

import com.google.gson.JsonElement;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.reporter.lib.fixture.FixtureResult;
import pvt.unitee.reporter.lib.fixture.FixtureResultDeserializer;
import unitee.interfaces.Reporter;

public class FixtureReportGenerator extends JsonResultsReader{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private FixtureResultDeserializer deserializer = null;
	
	public FixtureReportGenerator(List<Reporter> generators) throws Exception{
		super(Batteries.value(ArjunaProperty.PROJECT_RUN_REPORT_JSON_FIXTURES_DIR).asString(), generators);
		deserializer = new FixtureResultDeserializer();
	}
	
	protected FixtureResult getResultObject(JsonElement jElement){
		return deserializer.process(jElement.getAsJsonObject());
	}
	
	protected void update(JsonElement jElement) throws Exception {
		FixtureResult reportable = this.getResultObject(jElement);
		for (Reporter generator: this.getGenerators()){
			if (ArjunaInternal.displayReportGenerationInfo){
				logger.debug(String.format("%s: Updating: %s.", this.getClass().getSimpleName(), generator.getClass().getSimpleName()));
				logger.debug(String.format("Result Object: %s.", reportable.asJsonObject().toString()));
			}
			generator.update(reportable);
		}
	}

}
