package com.autocognite.pvt.unitee.testobject.lib.loader.group;

import com.autocognite.pvt.arjuna.enums.PickerTargetType;

public interface PickerConfig {

	PickerTargetType getTargetType();

	Picker createPicker() throws Exception;

	void setGroup(Group group);

	void process() throws Exception;
	
	Group getGroup();

}