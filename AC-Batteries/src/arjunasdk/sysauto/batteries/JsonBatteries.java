package arjunasdk.sysauto.batteries;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class JsonBatteries {

	public JsonObject strToJsonObject(String inStr){
		JsonElement root = (new JsonParser()).parse(inStr);
		return root.getAsJsonObject();		
	}
}
