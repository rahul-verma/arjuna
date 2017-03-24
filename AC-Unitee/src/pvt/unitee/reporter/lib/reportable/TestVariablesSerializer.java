package pvt.unitee.reporter.lib.reportable;

import org.apache.log4j.Logger;

import com.arjunapro.pvt.ArjunaInternal;
import com.arjunapro.testauto.interfaces.TestVariables;
import com.google.gson.JsonObject;

import pvt.batteries.config.Batteries;

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
