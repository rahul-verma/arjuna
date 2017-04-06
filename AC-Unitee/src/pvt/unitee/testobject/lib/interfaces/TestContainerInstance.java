package pvt.unitee.testobject.lib.interfaces;

import java.util.List;

import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.loader.DataMethodsHandler;

public interface TestContainerInstance extends TestObject {

	int getInstanceNumber();

	TestContainer getContainer();
	
	TestContainerFragment getCurrentFragment();
	
	boolean hasCompleted();

	int getCreatorThreadCount();

	Class<?> getUserTestContainer();

	DataMethodsHandler getDataMethodsHandler();

	Object getUserTestContainerObject();

	TestFixtures getTestFixtures();

	void setAllScheduledCreators(List<String> creatorNames);

	void loadFragment(List<String> methods) throws Exception;

	void markCurrentFragmentCompleted(TestContainerFragment fragment);



}
