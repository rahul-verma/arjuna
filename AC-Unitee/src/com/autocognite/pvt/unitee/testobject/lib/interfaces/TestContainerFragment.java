package com.autocognite.pvt.unitee.testobject.lib.interfaces;

import java.util.List;

import com.autocognite.pvt.arjuna.enums.FixtureResultType;
import com.autocognite.pvt.unitee.testobject.lib.fixture.TestFixtures;
import com.autocognite.pvt.unitee.testobject.lib.java.JavaTestMethod;
import com.autocognite.pvt.unitee.testobject.lib.loader.DataMethodsHandler;

public interface TestContainerFragment extends TestObject {

	int getFragmentNumber();

	TestContainer getContainer();
	
	TestContainerInstance getContainerInstance();

	int getCreatorThreadCount();

	Class<?> getUserTestContainer();

	DataMethodsHandler getDataMethodsHandler();

	Object getUserTestContainerObject();

	TestFixtures getTestFixtures();
	
	List<JavaTestMethod> getTestCreators();
	void loadTestCreators() throws Exception;

	void setCreatorNames(List<String> methods);

}
