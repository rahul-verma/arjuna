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
				logger.debug(testVars.object());
				logger.debug(testVars.object().items());
			}
			jsonObject.add("objectProps", serializeEnumKeyMap(testVars.object().items()));
			jsonObject.add("testProps", serializeEnumKeyMap(testVars.test().items()));
			jsonObject.add("customProps", serializeEnumKeyMap(testVars.utp().items()));
			jsonObject.add("utv", serializeEnumKeyMap(testVars.utv().items()));
			jsonObject.add("dataRecord", serializeEnumKeyMap(testVars.record().items()));
		} catch (Exception e){
			jsonObject.addProperty("rType", "Error in getting string representation");
			e.printStackTrace();
			throw e;
		}		
	}
}
