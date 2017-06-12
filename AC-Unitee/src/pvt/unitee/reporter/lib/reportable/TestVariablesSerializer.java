package pvt.unitee.reporter.lib.reportable;

import org.apache.log4j.Logger;

import com.google.gson.JsonObject;

import arjunasdk.console.Console;
import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import unitee.interfaces.TestVariables;

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
			jsonObject.add("attr", serializeEnumKeyMap(testVars.attr().items()));
			jsonObject.add("execVars", serializeEnumKeyMap(testVars.execVars().items()));
			jsonObject.add("dataRecord", serializeEnumKeyMap(testVars.record().items()));
		} catch (Exception e){
			jsonObject.addProperty("rType", "Error in getting string representation");
			Console.displayExceptionBlock(e);
			throw e;
		}		
	}
}
