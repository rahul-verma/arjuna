package pvt.unitee.testobject.lib.loader.group;

import java.util.List;

import pvt.unitee.enums.PickerTargetType;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.loader.tree.ExecutionSlotsCreator;

public interface Picker {

	int pick(ExecutionSlotsCreator execSlotsCreator, JavaTestClassDefinition classDef) throws Exception;

	void setConsiderPatterns(List<String> patterns);

	void setIgnorePatterns(List<String> patterns);

	void setGroup(Group group);

	PickerTargetType getTargetType();	
}
