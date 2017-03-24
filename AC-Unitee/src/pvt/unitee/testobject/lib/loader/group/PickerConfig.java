package pvt.unitee.testobject.lib.loader.group;

import pvt.arjunapro.enums.PickerTargetType;

public interface PickerConfig {

	PickerTargetType getTargetType();

	Picker createPicker() throws Exception;

	void setGroup(Group group);

	void process() throws Exception;
	
	Group getGroup();

}