package com.autocognite.pvt.unitee.testobject.lib.loader.group;

import java.util.List;

import com.autocognite.pvt.arjuna.enums.PickerTargetType;
import com.autocognite.pvt.unitee.testobject.lib.loader.tree.ExecutionSlotsCreator;

public interface Picker {

	int load(ExecutionSlotsCreator execSlotsCreator, List<String> unpickedContainers) throws Exception;

	void setConsiderPatterns(List<String> patterns);

	void setIgnorePatterns(List<String> patterns);

	void setGroup(Group group);

	PickerTargetType getTargetType();	
}
