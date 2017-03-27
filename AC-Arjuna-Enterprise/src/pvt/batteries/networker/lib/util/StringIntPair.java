package pvt.batteries.networker.lib.util;

public class StringIntPair {
	private String name = null;
	private int value = -1;
	
	public StringIntPair(String name, int value){
		this.setName(name);
		this.setValue(value);
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getValue() {
		return value;
	}

	public void setValue(int value) {
		this.value = value;
	}
}
