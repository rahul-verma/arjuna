package pvt.unitee.testobject.lib.interfaces;

import java.util.List;

import pvt.unitee.testobject.lib.fixture.TestFixtures;
import pvt.unitee.testobject.lib.java.JavaTestMethod;
import pvt.unitee.testobject.lib.loader.DataMethodsHandler;

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
