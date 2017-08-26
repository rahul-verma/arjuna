package pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import arjunasdk.config.RunConfig;
import arjunasdk.console.Console;
import arjunasdk.sysauto.batteries.ThreadBatteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.testobject.lib.interfaces.TestObject;

public abstract class AbstractTestObjectExecutor {
	private static Logger logger = RunConfig.logger();
	private int slotNum;

	protected AbstractTestObjectExecutor(int slotNum){
		this.setSlotNum(slotNum); 
	}

	private void executeSetUpWrapper(TestObject testObj){

		try{
			testObj.setUp();

		} catch (Throwable e){
			Console.displayExceptionBlock(e);
		}
	}

	private void executeTearDownWrapper(TestObject testObj){
		try{
			testObj.tearDown();	
		} catch (Throwable e){
			Console.displayExceptionBlock(e);
		}
	}

	protected void executeSetUp(TestObject testObj) throws Exception{
//		if ((!testObj.getTestVariables().object().group().toLowerCase().equals("mlgroup")
//				&&
		if (testObj.shouldExecuteSetUp()){
			if (ArjunaInternal.displayFixtureExecInfo){
				logger.debug(String.format("Attempting Set Up Class for Test Class %s in Slot# %d", 
						testObj.getQualifiedName(),
						this.getSlotNum()
						));
			}

			if (!testObj.wasSetUpExecuted()){
				if (ArjunaInternal.displayFixtureExecInfo){
					logger.debug("Set Up Class");
				}
				executeSetUpWrapper(testObj);
			}
		}		
	}

	protected void executeTearDown(TestObject testObj) throws Exception{
//		if ((!testObj.getTestVariables().object().group().toLowerCase().equals("mlgroup") &&
		if (testObj.shouldExecuteTearDown()){
			if (testObj.hasCompleted()){
				this.executeTearDownWrapper(testObj);
				if (ArjunaInternal.displaySlotsInfo){
					logger.debug(String.format("All test instances of %s have finished. Tear down class." , testObj.getQualifiedName()));
				}
			}
		}
	}

	protected int getSlotNum() {
		return slotNum;
	}

	private void setSlotNum(int slotNum) {
		this.slotNum = slotNum;
	}

	protected abstract int getChildThreadCount();

	protected abstract String getThreadNameSuffix(int threadNum);

	protected abstract Runnable createRunnable();

	protected void execute(){
		ArrayList<Thread> threads = new ArrayList<Thread>();
		Thread t;
		List<String> threadNames = new ArrayList<String>();

		for (int i = 1; i <= this.getChildThreadCount(); i++){

			String threadName = String.format("%s|%s", Thread.currentThread().getName(), this.getThreadNameSuffix(i));
			try{
				t = ThreadBatteries.createThread(threadName, createRunnable());
				threadNames.add(t.getName());
				ArjunaInternal.getCentralExecState().registerThread(t.getName());
				t.start();
				threads.add(t);
			} catch (Exception e){
				System.err.println("Critical Error: Exception occured while creating Test Slot Execution Thread.");
				Console.displayExceptionBlock(e);
				System.err.println("Exiting...");
				System.exit(1);
			}
		}
		try{
			for(Thread tLaunched : threads){
				tLaunched.join();
			}	
		} catch (InterruptedException e){
			Console.displayExceptionBlock(e);
		}

		for (String tName: threadNames){
			ArjunaInternal.getCentralExecState().deregisterThread(tName);
		}		
	}

	protected boolean copySchedulingStatusFromParentAndReturnFalseIfNotApplicable(TestObject parent, TestObject testObj){
//		if (parent.wasSkipped()){
//			testObj.markSkipped(
//					parent.getSkipType(),
//					parent.getSkipDesc()
//					);
//			return true;
//		} else if (parent.wasUnSelected()){
//			testObj.markUnSelected(
//					parent.getUnSelectedType(),
//					parent.getUnSelectedDesc()
//					);
//			return true;
//		} else 
		if (parent.wasExcluded()){
			testObj.markExcluded(
					parent.getExclusionType(),
					parent.getExclusionDesc(),
					parent.getExclusionIssueId()
					);
			return true;
		} else {
			return false;
		}

	}

}
