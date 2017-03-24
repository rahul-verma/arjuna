package pvt.unitee.testobject.lib.loader.group;

import java.util.List;

import pvt.arjunapro.enums.PickerTargetType;
import pvt.unitee.testobject.lib.loader.tree.ExecutionSlotsCreator;

public interface Picker {

	int load(ExecutionSlotsCreator execSlotsCreator, List<String> unpickedContainers) throws Exception;

	void setConsiderPatterns(List<String> patterns);

	void setIgnorePatterns(List<String> patterns);

	void setGroup(Group group);

	PickerTargetType getTargetType();	
}
