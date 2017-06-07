package pvt.unitee.runner.lib.slots;

import org.apache.log4j.Logger;

import arjunasdk.config.RunConfig;
import arjunasdk.console.Console;
import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.enums.TestResultCode;
import pvt.unitee.reporter.lib.IssueId;
import pvt.unitee.testobject.lib.interfaces.TestContainer;

public class TestContainerExecutor extends AbstractTestObjectExecutor implements Runnable{
	private static Logger logger = RunConfig.logger();
	private TestSlot testSlot = null;
	private TestContainer testContainer = null;
	private TestSlotTestContainer currentSlotsContainer = null;

	public TestContainerExecutor (int slotNum, TestSlot testSlot){
		super(slotNum);
		this.testSlot = testSlot;
	}
	
	protected int getChildThreadCount(){
		return testContainer.getInstanceThreadCount();
	}

	protected String getThreadNameSuffix(int threadNum){
		return String.format("C-%s-CIT-%d", testContainer.getQualifiedName(), threadNum);
	}
	
	protected Runnable createRunnable(){
		return new TestContainerInstanceExecutor(this.getSlotNum(), currentSlotsContainer);
	}
	
	public void execute(TestSlotTestContainer slotTestContainer) throws Exception{
		currentSlotsContainer = slotTestContainer;
		testContainer = slotTestContainer.getTestContainer();
		testContainer.setThreadId(Thread.currentThread().getName());
		testContainer.populateUserProps();
		
		executeSetUp(testContainer);
		
		execute();
		
		executeTearDown(testContainer);
	}

	public void run() {
		while(true){
			TestSlotTestContainer testSlotContainer = null;
			try{
				testSlotContainer = this.testSlot.next();
				IssueId outId = new IssueId();
				
				 if (!testSlotContainer.getTestContainer().shouldExecute(outId)){
					  testSlotContainer.getTestContainer().markExcluded(
							  TestResultCode.TEST_CONTAINER_DEPENDENCY_NOTMET,
							  String.format("%s did not meet its dependencies.", testSlotContainer.getTestContainer().getUserTestClass().getSimpleName()),
							  outId.ID
					);
				  }
				  
				  this.execute(testSlotContainer);
			} catch (SubTestsFinishedException e){
				return;
			} catch (Exception e) {
				// TODO Auto-generated catch block
				Console.displayExceptionBlock(e);
			}
		}

	}
}
