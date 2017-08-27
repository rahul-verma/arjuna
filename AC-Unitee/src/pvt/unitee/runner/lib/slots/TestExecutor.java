package pvt.unitee.runner.lib.slots;

import org.apache.log4j.Logger;

import arjunasdk.config.RunConfig;
import arjunasdk.console.Console;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.testobject.lib.interfaces.Test;
import pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

public class TestExecutor extends AbstractTestObjectExecutor implements Runnable{
	private static Logger logger = RunConfig.logger();
	private int slotNum;
	private TestSlotTestCreatorInstance creatorInstance = null;

	public TestExecutor (int slotNum, TestSlotTestCreatorInstance creatorInstance){
		super(slotNum);
		this.creatorInstance = creatorInstance;
	}

	protected int getChildThreadCount(){
		return -1;
	}

	protected String getThreadNameSuffix(int threadNum){
		return null;
	}

	protected Runnable createRunnable(){
		return null;
	}

	public void run() {
		Test test = null;
		while(true){
			try{
				try{
					test = this.creatorInstance.next();
					test.initTimeStamp();
				} catch (SubTestsFinishedException e){
					return;
				} catch (Exception e){
					Console.displayExceptionBlock(e);
				}
				if (ArjunaInternal.displaySlotsInfo){
					logger.debug(String.format("Now Executing %s (Test# %d) in Slot# %d",
							test.getQualifiedName(),
							test.getTestNumber(),
							this.getSlotNum())
							);
				}

				TestCreatorInstance creatorInstance = test.getParentCreatorInstance(); 
				try{
					creatorInstance.setThreadId(Thread.currentThread().getName());
				} catch (Exception e){

				}

				copySchedulingStatusFromParentAndReturnFalseIfNotApplicable(creatorInstance, test);
				
				test.populateUserProps();
				
				ArjunaInternal.getCentralExecState().getCurrentThreadState().enableTestThreadFlag();
				
				test.beginTest();
				
				test.initTimeStamp();

				this.executeSetUp(test);
				
				if (test.wasExcluded()){
					this.executeTearDown(test);
					test.endTimeStamp();
					test.reportExclusion();
					test.endTest();
					continue;
				}

				try{
					test.execute();
				} catch (Exception e){
					Console.displayExceptionBlock(e);
				}

				this.executeTearDown(test);
				test.reportExecuted();
				test.endTest();
				
				ArjunaInternal.getCentralExecState().getCurrentThreadState().disableTestThreadFlag();
			} catch (Exception e){
				Console.displayExceptionBlock(e);
			}
		}
	}
}
