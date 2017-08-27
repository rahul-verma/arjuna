package pvt.unitee.testobject.lib.interfaces;

import java.util.List;

import pvt.unitee.reporter.lib.IssueId;
import pvt.unitee.testobject.lib.java.JavaTestClassFragment;
import pvt.unitee.testobject.lib.java.JavaTestMethodInstance;

public interface TestCreator extends TestObject{

	List<JavaTestMethodInstance> getInstances();

	int getInstanceThreadCount();

	boolean shouldExecute(IssueId outId);

	String getName();

	JavaTestClassFragment getTestContainerFragment();

	void loadInstances() throws Exception;
}
