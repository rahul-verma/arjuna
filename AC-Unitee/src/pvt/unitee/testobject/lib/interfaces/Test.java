package pvt.unitee.testobject.lib.interfaces;

import com.arjunapro.ddt.interfaces.DataRecord;

import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.java.JavaTestClassFragment;
import pvt.unitee.testobject.lib.java.JavaTestMethodInstance;

public interface Test extends TestObject{

	String getQualifiedName();

	int getTestNumber();

	String getName();

	void run() throws Exception;

	TestFixtures getTestFixtures();

	void execute() throws Exception;

	void setDataRecord(DataRecord dataRecord);

	JavaTestMethodInstance getParentCreatorInstance();

	JavaTestClassFragment getTestContainerFragment();
}
