package pvt.unitee.testobject.lib.loader.session;

import org.apache.log4j.Logger;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import arjunasdk.console.Console;
import pvt.batteries.config.Batteries;
import pvt.batteries.hocon.HoconFileReader;
import pvt.batteries.hocon.HoconReader;

public class UserDefinedSession extends BaseSession{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private String sessionFilePath = null;
	private JsonObject arjunaOptionsObj = null;
	private JsonObject sObject = null;
	private JsonObject execVarsObj = null;
	private JsonObject userOptionsObj = null;

	public UserDefinedSession(String sessionName, String sessionFilePath) throws Exception{
		super(sessionName);
		this.sessionFilePath = sessionFilePath;
		HoconReader reader = new HoconFileReader(sessionFilePath);
		reader.process();
		String jsonString = reader.getConfig().root().render();
		JsonElement root = (new JsonParser()).parse(jsonString);
		sObject = root.getAsJsonObject();
		arjunaOptionsObj = sObject.getAsJsonObject("arjunaOptions");
		execVarsObj = sObject.getAsJsonObject("execVars");
		userOptionsObj = sObject.getAsJsonObject("userOptions");
	}
	
	private void exitAsAttrNotAnArray(String subjectName, String attr){
		Console.displayError(
				String.format(
						"A %s must define >>%s<< as an array. Fix session template file: >>%s<<",
						subjectName,
						attr,
						sessionFilePath
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	private void exitAsAttrIsNull(String subjectName, String attr){
		Console.displayError(
				String.format(
						"A %s must have a >>%s<< attribute. Fix session template file: >>%s<<",
						subjectName,
						attr,
						sessionFilePath
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	private void exitAsAttrIsEmptyArray(String subjectName, String attr){
		Console.displayError(
				String.format(
						"A %s must have non-empty >>%s<< array. Fix session template file: >>%s<<",
						subjectName,
						attr,
						sessionFilePath
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
		
	private void existAsInvalidSessionNodeSupplied(){
		Console.displayError(
				String.format(
						">>nodes<< attribute can only contain a queue of either group names or session node json object.Fix session template file: >>%s<<",
						sessionFilePath
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	@Override
	public JsonObject getConfigObject(){
		return this.arjunaOptionsObj;
	}
	
	public void load() throws Exception{
		JsonArray jArr = null;
		try{
			jArr = sObject.getAsJsonArray("nodes");
		} catch (ClassCastException e){
			exitAsAttrNotAnArray("session definition", "nodes");
		}
		if (jArr == null){
			exitAsAttrIsNull("session definition", "nodes");		
		}
		if (jArr.size() == 0){
			exitAsAttrIsEmptyArray("session definition", "nodes");			
		}

		int counter = 1;
		for (JsonElement nodeElem: jArr){
			BaseSessionNode node = null;
			JsonObject nodeObj = null;
			String nodeName = null;
			counter += 1;
			try{
				nodeObj = nodeElem.getAsJsonObject();
				node = new BaseSessionNode(this, counter, nodeObj);
			} catch (IllegalStateException e){
				try{
					nodeName =  nodeElem.getAsString();
				} catch (Exception f){
					existAsInvalidSessionNodeSupplied();
				}
				
				try{
					node = new BaseSessionNode(this, counter, nodeName);					
				} catch (Exception h){
					Console.displayError(String.format("An unknown exception occured in creating session for %s. Investigate.", sessionFilePath));
					Console.displayExceptionBlock(h);
					Console.displayError("Exiting...");
					System.exit(-1);
				}
			}
			
			this.addNode(node);
		}
		super.load();
	}

	@Override
	public String getSessionFilePath() {
		return this.sessionFilePath;
	}

	@Override
	public JsonObject getExecVarObject() {
		return this.execVarsObj;
	}
	
	@Override
	public JsonObject getUserOptionsObject() {
		return this.userOptionsObj;
	}
}
