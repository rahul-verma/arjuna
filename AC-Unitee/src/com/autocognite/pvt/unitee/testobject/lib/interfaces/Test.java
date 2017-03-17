package com.autocognite.pvt.unitee.testobject.lib.interfaces;

import com.autocognite.arjuna.interfaces.DataRecord;
import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.unitee.testobject.lib.fixture.Fixture;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestClassFragment;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestMethodInstance;

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
