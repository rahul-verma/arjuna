package pvt.unitee.testobject.lib.loader.session;

import com.google.gson.JsonObject;

import pvt.unitee.enums.PickerTargetType;
import pvt.unitee.testobject.lib.loader.group.PickerConfig;

public class MSession extends BaseSession{
	private PickerConfig config = null;
	
	public MSession(PickerConfig config) throws Exception{
		super("msession");
		this.config = config;
	}

	@Override
	public void schedule() throws Exception{
		BaseSessionNode node = new BaseSessionNode(this, 1, "mnode", config);
		this.addNode(node);
		super.schedule();
	}
	
	private static String getMagicGroupName(PickerTargetType defaultPickerTarget){
		String groupName = null;
		switch(defaultPickerTarget){
		case CLASSES:
			groupName = "mfcgroup";
			break;
		case METHODS:
			groupName = "mfmgroup";
			break;
		case PACKAGES:
			groupName = "mfpgroup";
			break;
		}
		return groupName;
	}

	public JsonObject getConfigObject(){
		return new JsonObject();
	}

	@Override
	public String getSessionFilePath() {
		return "NA";
	}

	@Override
	public JsonObject getExecVarObject() {
		return new JsonObject();
	}
	
	@Override
	public JsonObject getUserOptionsObject() {
		return new JsonObject();
	}
}
