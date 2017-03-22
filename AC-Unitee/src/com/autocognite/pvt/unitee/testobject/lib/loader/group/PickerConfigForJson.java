package com.autocognite.pvt.unitee.testobject.lib.loader.group;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Map.Entry;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.utils.console.Console;
import com.autocognite.pvt.arjuna.enums.PickerTargetType;
import com.autocognite.pvt.batteries.config.Batteries;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

public class PickerConfigForJson extends AbstractPickerConfig{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private JsonElement pickerJson = null;
	
	public PickerConfigForJson(Group group, JsonElement pElement) throws Exception{
		super();
		this.setGroup(group);
		pickerJson = pElement;
	}
	
	public void process() throws Exception{
		logger.debug("Configuring picker: " + pickerJson.toString());
		JsonObject pickerObj = pickerJson.getAsJsonObject();
		JsonPrimitive jPrim = pickerObj.getAsJsonPrimitive("target");
		if (jPrim == null){
			throw new PickerMisConfiguration();
		}
		String target = pickerObj.getAsJsonPrimitive("target").getAsString().toUpperCase();
		this.setTargetType(PickerTargetType.valueOf(target));
		this.configure(pickerObj);
		validate();
		validateJson();
		processNonRegexPickOptions();
	}
	
	// This happens when names are used instead of package/class patterns
	private void processNonRegexPickOptions(){
		if (isMethodConsiderOrIgnoreOptionProvided() || isClassConsiderOrIgnoreOptionProvided() || isPackageConsiderOrIgnoreOptionProvided()){
			return;
		} else if ((this.getTargetType() == PickerTargetType.CLASSES)
				&& (this.getPackageName() != null) && 
					(this.getClassName() != null)){
			logger.debug("Picker Combination: Package Name + Class Name");
			configureClassConsiderPatterns(Arrays.asList(this.getClassName()));
			return;	
		} else if ((this.getTargetType() == PickerTargetType.PACKAGES)
				&& (this.getPackageName() != null)){
		logger.debug("Picker Combination: Package Name");
		configurePackageConsiderPatterns(Arrays.asList(this.getPackageName()));
		return;	
		}
	}
	
	private void validateJson() throws Exception {
		if (!this.isJsonValid()){
			throw new PickerMisConfiguration();
		}
		
	}
	
	private boolean isJsonValid() throws Exception {
		if (this.getTargetType() == PickerTargetType.PACKAGES){
			if ((!this.isPackageConsiderOrIgnoreOptionProvided()) && (this.getPackageName() == null)){
				return false;
			}
			
			if (this.getClassName() != null){
				return false;
			}
		}

		if (this.getTargetType() == PickerTargetType.CLASSES){
			if ((!this.isClassConsiderOrIgnoreOptionProvided()) && (this.getClassName() == null)){
				return false;
			}
			
			if ((this.getPackageName() == null)){
				return false;
			}
		}
		
		if (this.getTargetType() == PickerTargetType.METHODS){
			if ((!this.isMethodConsiderOrIgnoreOptionProvided())){
				return false;
			}
			
			if ((this.getPackageName() == null)){
				return false;
			}
			
			if ((this.getClassName() == null)){
				return false;
			}
		}
		
		return true;
	}
	
	private List<String> jsonArrToStringList(JsonArray jArr){
		List<String> outList = new ArrayList<String>();
		for (JsonElement elem: jArr){
			outList.add(elem.getAsString());
		}
		return outList;	
	}
	
	private List<String> getPatternIfDefined(String attr, JsonElement elem){		
		JsonArray jArr = null;
		try{
			jArr = elem.getAsJsonArray();
		} catch (IllegalStateException e){
			Console.displayError(
					String.format(
							"A picker definition must define >>%s<< attribute as an array of regex patterns. Fix group template file: >>%s<<",
							attr,
							this.getGroup().getDefinitionFile()
					));			
			Console.displayError("Exiting...");
			System.exit(1);					
		}

		if (jArr.size() == 0){
			Console.displayError(
					String.format(
							">>%s<< attribute in picker definition can not be empty. Fix group template file: >>%s<<",
							attr,
							this.getGroup().getDefinitionFile()
					));			
			Console.displayError("Exiting...");
			System.exit(1);				
		}		
		
		return jsonArrToStringList(jArr);
	}

	private void configure(JsonObject pObject) throws Exception{
		Iterator<Entry<String,JsonElement>> iter = pObject.entrySet().iterator();
		while(iter.hasNext()){
			Entry<String,JsonElement> entry = iter.next();
			JsonTestPickerProperty prop = null;
			try{
				prop = JsonTestPickerProperty.valueOf(entry.getKey().toUpperCase());
			} catch (IllegalArgumentException e){
				Console.displayError(
						String.format(
								">>%s<< is not an allowed attribute in picker definition. Fix group template file: >>%s<<",
								entry.getKey(),
								this.getGroup().getDefinitionFile()
						));			
				Console.displayError("Exiting...");
				System.exit(1);						
			}
			switch(prop){
			case CLASS:
				if ((entry.getValue()!= null)  && (!entry.getValue().isJsonPrimitive())){
					Console.displayError(
							String.format(
									">>class<< attribute in picker can only be a string. Fix group template file: >>%s<<",
									entry.getKey(),
									this.getGroup().getDefinitionFile()
							));			
					Console.displayError("Exiting...");
					System.exit(1);						
				}
				this.configureClassName(entry.getValue().getAsString());
				break;
			case CONSIDER:
				List<String> cPatterns = getPatternIfDefined("consider", entry.getValue());
				if (cPatterns == null){
					break;
				}
				switch (this.getTargetType()){
				case CLASSES:
					this.configureClassConsiderPatterns(cPatterns);
					break;
				case METHODS:
					this.configureMethodConsiderPatterns(cPatterns);
					break;
				case PACKAGES:
					this.configurePackageConsiderPatterns(cPatterns);
					break;
				}
				break;
			case IGNORE:
				List<String> iPatterns = getPatternIfDefined("ignore", entry.getValue());
				if (iPatterns == null){
					break;
				}
				switch (this.getTargetType()){
				case CLASSES:
					this.configureClassIgnorePatterns(iPatterns);
					break;
				case METHODS:
					this.configureMethodIgnorePatterns(iPatterns);
					break;
				case PACKAGES:
					this.configurePackageIgnorePatterns(iPatterns);
					break;
				}
				break;
			case PACKAGE:
				if ((entry.getValue()!= null)  && (!entry.getValue().isJsonPrimitive())){
					Console.displayError(
							String.format(
									">>package<< attribute in picker can only be a string. Fix group template file: >>%s<<",
									entry.getKey(),
									this.getGroup().getDefinitionFile()
							));			
					Console.displayError("Exiting...");
					System.exit(1);						
				}
				this.configurePackageName(entry.getValue().getAsString());
				break;
			case TARGET:
				// Do nothing, the target type has already been set.
				break;
			}
		}
	}
}
