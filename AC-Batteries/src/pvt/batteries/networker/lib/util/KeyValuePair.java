package pvt.batteries.networker.lib.util;

public class KeyValuePair {
	private String name = null;
	private String value = null;
	
	public KeyValuePair(String name, String value){
		this.setName(name);
		this.setValue(value);
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getValue() {
		return value;
	}

	public void setValue(String value) {
		this.value = value;
	}
}
