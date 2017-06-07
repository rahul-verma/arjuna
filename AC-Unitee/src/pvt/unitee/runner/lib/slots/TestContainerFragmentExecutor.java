package pvt.unitee.runner.lib.slots;

import org.apache.log4j.Logger;

import arjunasdk.config.RunConfig;
import arjunasdk.console.Console;
import pvt.arjunapro.ArjunaInternal;
import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.testobject.lib.interfaces.TestContainerFragment;
import pvt.unitee.testobject.lib.interfaces.TestContainerInstance;

public class TestContainerFragmentExecutor extends AbstractTestObjectExecutor implements Runnable{
	private static Logger logger = RunConfig.logger();
	private TestSlotTestContainerInstance slotTestContainerInstance = null;
	private TestContainerFragment currentTestContainerFragment = null;
	private TestSlotTestContainerFragment currentSlotsContainerFragment = null;

	public TestContainerFragmentExecutor (int slotNum, TestSlotTestContainerInstance slotTestContainerInstance){
		super(slotNum);
		this.slotTestContainerInstance = slotTestContainerInstance;
	}

	protected int getChildThreadCount(){
		return currentTestContainerFragment.getCreatorThreadCount();
	}

	protected String getThreadNameSuffix(int threadNum){
		return String.format("IF-%d|CrT-%d", currentTestContainerFragment.getFragmentNumber(), threadNum);
	}

	protected Runnable createRunnable(){
		return new TestCreatorExecutor(this.getSlotNum(), currentSlotsContainerFragment);
	}

	public void execute(TestSlotTestContainerFragment slotTestContainerFragment) throws Exception{
		this.currentSlotsContainerFragment = slotTestContainerFragment;

		currentTestContainerFragment = slotTestContainerFragment.getContainerFragment();
		currentTestContainerFragment.setThreadId(Thread.currentThread().getName());
		currentTestContainerFragment.populateUserProps();

		this.executeSetUp(currentTestContainerFragment);

		this.execute();

		this.executeTearDown(currentTestContainerFragment);

		if (ArjunaInternal.displaySlotsInfo){
			logger.debug(String.format("Check if  %s class instance has completed." , currentTestContainerFragment.getQualifiedName()));
		}
		if (currentTestContainerFragment.hasCompleted()){
			if (ArjunaInternal.displaySlotsInfo){
				logger.debug(String.format("Class instance  %s completed. Update class and mark this instance completed." , currentTestContainerFragment.getQualifiedName()));
			}
			currentTestContainerFragment.getContainerInstance().markCurrentFragmentCompleted(currentTestContainerFragment);
			if (ArjunaInternal.displaySlotsInfo){
				logger.debug("Updated");
			}
		}
	}

	public void run() {
		while(true){
			TestSlotTestContainerFragment slotTestContainerFragment = null;
			try{
				slotTestContainerFragment = this.slotTestContainerInstance.next();
				TestContainerInstance containerInstance = slotTestContainerFragment.getContainerFragment().getContainerInstance();

				copySchedulingStatusFromParentAndReturnFalseIfNotApplicable(containerInstance, slotTestContainerFragment.getContainerFragment());

				this.execute(slotTestContainerFragment);
			} catch (SubTestsFinishedException e){
				return;
			} catch (Exception e) {
				// TODO Auto-generated catch block
				Console.displayExceptionBlock(e);
			}
		}

	}
}
