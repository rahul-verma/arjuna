package com.autocognite.pvt.unitee.testobject.lib.loader.group;

import java.util.ArrayList;
import java.util.List;

import com.autocognite.pvt.batteries.console.Console;
import com.autocognite.pvt.batteries.hocon.HoconFileReader;
import com.autocognite.pvt.batteries.hocon.HoconReader;
import com.autocognite.pvt.batteries.hocon.HoconStringReader;
import com.autocognite.pvt.unitee.testobject.lib.loader.session.SessionSubNode;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.typesafe.config.ConfigException;

public class UserDefinedGroup extends BaseGroup{
	private String groupFilePath = null;

	public UserDefinedGroup(SessionSubNode subNode, String gName, String groupTemplatePath) throws Exception {
		super(subNode, gName);
		groupFilePath = groupTemplatePath;
		HoconReader reader = null;
		try{
			reader = new HoconFileReader(groupFilePath);
			reader.process();
		} catch (ConfigException e){
			if (e.getClass().getName().endsWith("Parse")){
				Console.displayError(String.format("A parsing exception occured in loading group from group template at %s. Investigate.", groupTemplatePath));
			} else {
				Console.displayError(String.format("An unknown exception occured in loading group from group template at %s. Investigate.", groupTemplatePath));
			}
			Console.displayExceptionBlock(e);
			Console.displayError("Exiting...");
			System.exit(-1);					
		}
		String jsonString = reader.getConfig().root().render();
		JsonElement root = (new JsonParser()).parse(jsonString);
		processJson(root.getAsJsonObject());
		this.setLoader(new JavaTestClassLoader(this));
	}
	
	private void errorUdvNotObject(){
		Console.displayError(
				String.format(
						">>udv<< attribute in group definition should be a JSON object. Fix session template file: >>%s<<",
						groupFilePath
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	private void existAsClassThreadsIsNotInt(){
		Console.displayError(
				String.format(
						">>classThreads<< attribute in group definition can only be an Integer. Fix group template file: >>%s<<",
						groupFilePath
				));			
		Console.displayError("Exiting...");
		System.exit(1);			
	}
	
	private void processJson(JsonObject gObject) throws Exception{
		
		try{
			JsonObject udv = gObject.getAsJsonObject("udv");
			HoconReader udvReader = new HoconStringReader(udv.toString());
			udvReader.process();
			this.getUDV().add(udvReader.getProperties());
		} catch (ClassCastException e){
			this.errorUdvNotObject();
		} catch (NullPointerException e){
			// do nothing
		}
		
		JsonArray jArr = null;
		try{
			jArr = gObject.getAsJsonArray("pickers");
		} catch (ClassCastException e){
			Console.displayError(
					String.format(
							"A group definition must define >>pickers<< as an array. Fix group template file: >>%s<<",
							groupFilePath
					));			
			Console.displayError("Exiting...");
			System.exit(1);					
		}
		if (jArr == null){
			Console.displayError(
					String.format(
							"A group definition must have a >>pickers<< attribute. Fix group template file: >>%s<<",
							groupFilePath
					));			
			Console.displayError("Exiting...");
			System.exit(1);			
		}
		if (jArr.size() == 0){
			Console.displayError(
					String.format(
							">>pickers<< array can not be empty. Fix group template file: >>%s<<",
							groupFilePath
					));			
			Console.displayError("Exiting...");
			System.exit(1);				
		}
		
		int classThreads = 1;
		try{ 
			classThreads = gObject.getAsJsonPrimitive("classThreads").getAsInt();
		} catch (NumberFormatException e){
			this.existAsClassThreadsIsNotInt();
		} catch (ClassCastException e){
			this.existAsClassThreadsIsNotInt();
		} catch (NullPointerException e){
			// Do nothing. Default is 1
		}

		this.setClassThreadCount(classThreads);
		List<Picker> pickers = new ArrayList<Picker>();
		for (JsonElement pickerElem : jArr){
			PickerConfig config = null;
			try{
				config = new PickerConfigForJson(this, pickerElem);
				config.process();
			} catch (PickerMisConfiguration e){
				Console.displayError(
						String.format(
								"There is an error in picker configuration in group template file: >>%s<<",
								groupFilePath
						));
				AbstractPickerConfig.displayError(pickerElem);
				Console.displayError("Exiting...");
				System.exit(1);
			}
			pickers.add(config.createPicker());
		}		
		this.setPickers(pickers);
	}
	

	@Override
	public String getDefinitionFile() {
		return this.groupFilePath;
	}

}
