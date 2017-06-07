package pvt.unitee.testobject.lib.loader.session;

import com.google.gson.JsonObject;

import pvt.unitee.enums.PickerTargetType;

public class MSession extends BaseSession{
	private String groupName = null;
	
	private MSession(String mGroupName) throws Exception{
		super("msession");
		this.groupName = mGroupName;
	}

	public MSession() throws Exception{
		this("magroup");		
	}
	
	public void load() throws Exception{
		BaseSessionNode node = new BaseSessionNode(this, 2, "mnode", groupName);
		this.addNode(node);
		super.load();
	}
	
	public MSession(PickerTargetType defaultPickerTarget) throws Exception{		
		this(getMagicGroupName(defaultPickerTarget));
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
	public JsonObject getUTVObject() {
		return new JsonObject();
	}
	
	@Override
	public JsonObject getUserConfigObject() {
		return new JsonObject();
	}
}
