package pvt.unitee.runner.lib.slots;

import org.apache.log4j.Logger;

import com.arjunapro.testauto.config.RunConfig;

import pvt.arjunapro.ArjunaInternal;
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
					e.printStackTrace();
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

				this.executeSetUp(test);

				try{
					test.execute();
				} catch (Exception e){
					e.printStackTrace();
				}

				this.executeTearDown(test);
			} catch (Exception e){
				e.printStackTrace();
			}
		}
	}
}
