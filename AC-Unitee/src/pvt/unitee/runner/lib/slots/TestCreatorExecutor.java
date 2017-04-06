package pvt.unitee.runner.lib.slots;

import org.apache.log4j.Logger;

import com.arjunapro.testauto.config.RunConfig;

import pvt.arjunapro.ArjunaInternal;
import pvt.arjunapro.enums.TestResultCode;
import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.reporter.lib.IssueId;
import pvt.unitee.testobject.lib.interfaces.TestContainerFragment;
import pvt.unitee.testobject.lib.interfaces.TestCreator;

public class TestCreatorExecutor extends AbstractTestObjectExecutor implements Runnable{
	private static Logger logger = RunConfig.logger();
	private TestSlotTestContainerFragment slotTestContainerFragment = null;
	private TestCreator currentTestCreator = null;
	private TestSlotTestCreator currentSlotTestCreator = null;

	public TestCreatorExecutor (int slotNum, TestSlotTestContainerFragment slotTestContainerFragment){
		super(slotNum);
		this.slotTestContainerFragment = slotTestContainerFragment;
	}

	protected int getChildThreadCount(){
		return currentTestCreator.getInstanceThreadCount();
	}

	protected String getThreadNameSuffix(int threadNum){
		return String.format("%s-CrIT%d", currentTestCreator.getName(), threadNum);
	}

	protected Runnable createRunnable(){
		return new TestCreatorInstanceExecutor(this.getSlotNum(), currentSlotTestCreator);
	}

	public void execute(TestSlotTestCreator slotTestCreator) throws Exception{
		this.currentSlotTestCreator = slotTestCreator;
		currentTestCreator = slotTestCreator.getTestCreator();
		currentTestCreator.setThreadId(Thread.currentThread().getName());
		currentTestCreator.populateUserProps();

		this.executeSetUp(currentTestCreator);

		this.execute();

		this.executeTearDown(currentTestCreator);
	}

	public void run() {
		while(true){
			TestSlotTestCreator slotTestCreator = null;

			try{
				slotTestCreator  = this.slotTestContainerFragment.next();
				if (ArjunaInternal.displaySlotsInfo){
					logger.debug("Executing Test Creator: " + slotTestCreator.getTestCreator().getQualifiedName());
				}

				TestContainerFragment containerFragment = slotTestCreator.getTestCreator().getTestContainerFragment();
				IssueId outId = new IssueId();

				boolean marked = copySchedulingStatusFromParentAndReturnFalseIfNotApplicable(containerFragment, slotTestCreator.getTestCreator());
				if (!marked){
					if (!slotTestCreator.getTestCreator().shouldExecute(outId)){
						slotTestCreator.getTestCreator().markExcluded(
								TestResultCode.TEST_CREATOR_DEPENDENCY_NOTMET,
								String.format("%s did not meet its dependencies.", slotTestCreator.getTestCreator().getName()),
								outId.ID
								);
					}
				}
				this.execute(slotTestCreator);
			} catch (SubTestsFinishedException e){
				return;
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}

		}

	}
}
