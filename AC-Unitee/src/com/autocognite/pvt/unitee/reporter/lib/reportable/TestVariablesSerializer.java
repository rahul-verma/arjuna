package com.autocognite.pvt.unitee.reporter.lib.reportable;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.interfaces.TestVariables;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.batteries.config.Batteries;
import com.google.gson.JsonObject;

public class TestVariablesSerializer extends BaseSerializer {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	
	public void serializeTestVariables(JsonObject jsonObject, TestVariables testVars) throws Exception{
		try{
			if (ArjunaInternal.logJsonSerializationInfo){
				logger.debug(testVars.objectProps());
				logger.debug(testVars.objectProps().items());
			}
			jsonObject.add("objectProps", serializeEnumKeyMap(testVars.objectProps().items()));
			jsonObject.add("testProps", serializeEnumKeyMap(testVars.testProps().items()));
			jsonObject.add("customProps", serializeEnumKeyMap(testVars.customProps().items()));
			jsonObject.add("udv", serializeEnumKeyMap(testVars.udv().items()));
			jsonObject.add("dataRecord", serializeEnumKeyMap(testVars.dataRecord().items()));
		} catch (Exception e){
			jsonObject.addProperty("rType", "Error in getting string representation");
			e.printStackTrace();
			throw e;
		}		
	}
}
