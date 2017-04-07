package pvt.unitee.reporter.lib.generator;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.log4j.Logger;

import com.arjunapro.testauto.console.Console;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

import pvt.arjunapro.ArjunaInternal;
import pvt.arjunapro.interfaces.ReportGenerator;
import pvt.batteries.config.Batteries;
import pvt.batteries.filehandler.FileReader;

public abstract class JsonResultsReader{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private String reportDir = null;
	private File[] files = null;
	private List<ReportGenerator> generators = new ArrayList<ReportGenerator>();
	
	public JsonResultsReader(String reportDir, List<ReportGenerator> observers) throws Exception{
		this.reportDir = reportDir;
		files = (new File(reportDir)).listFiles();
		Arrays.sort(files);
		this.getGenerators().addAll(observers);
	}
	
	public void addGenerator(ReportGenerator observer){
		this.getGenerators().add(observer);
	}
	
	private JsonElement getJson(File f) throws IOException{
		FileReader reader = new FileReader(reportDir + "/" + f.getName());
		return (new JsonParser()).parse(reader.read());
	}
	
	abstract protected void update(JsonElement jElement) throws Exception;
	
	public void generate() {
		if (ArjunaInternal.displayReportGenerationInfo){
			logger.debug(String.format("%s: #Generators: %d.", this.getClass().getSimpleName(), this.generators.size()));
			logger.debug(String.format("%s: #Records: %d.", this.getClass().getSimpleName(), this.files.length));
		}
		for (File f: files){
			try {
				if (ArjunaInternal.displayReportGenerationInfo){
					logger.debug(String.format("%s: Convert file to Json: %s.", this.getClass().getSimpleName(), f.getName()));
				}
				JsonElement jElement = getJson(f);
				if (ArjunaInternal.displayReportGenerationInfo){
					logger.debug(String.format("%s: Convert JSON to Reportable.", this.getClass().getSimpleName(), f.getName()));
					logger.debug(String.format("JSON: %s.", jElement.toString()));
					logger.debug(String.format("%s: Update generators.", this.getClass().getSimpleName(), f.getName()));
				}
				update(jElement);
				if (ArjunaInternal.displayReportGenerationInfo){
					
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				Console.displayExceptionBlock(e);
			}
		}			
	}

	protected List<ReportGenerator> getGenerators() {
		return generators;
	}

	private void setGenerators(List<ReportGenerator> generators) {
		this.generators = generators;
	}
}
