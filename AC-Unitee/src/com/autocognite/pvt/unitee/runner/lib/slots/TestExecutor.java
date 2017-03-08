package com.autocognite.pvt.unitee.runner.lib.slots;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.Test;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

public class TestExecutor implements Runnable{
	private static Logger logger = RunConfig.getCentralLogger();
	private int slotNum;
	private TestSlotTestCreatorInstance creatorInstance = null;

	public TestExecutor (int slotNum, TestSlotTestCreatorInstance creatorInstance){
		this.slotNum = slotNum;
		this.creatorInstance = creatorInstance;
	}

	protected void executeSetUpTestFor(Test test){
		try{
			test.setUpTest();	
		} catch (Exception e){
			e.printStackTrace();
		}
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
						this.slotNum)
						);
				}
	
				TestCreatorInstance creatorInstance = test.getParentCreatorInstance(); 
				try{
					creatorInstance.setThreadId(Thread.currentThread().getName());
				} catch (Exception e){
					
				}
				if (creatorInstance.wasSkipped()){
					test.markSkipped(
							creatorInstance.getSkipType(),
							creatorInstance.getSkipDesc()
					);
				  } else if (creatorInstance.wasUnSelected()){
					  test.markUnSelected(
							  creatorInstance.getUnSelectedType(),
							  creatorInstance.getUnSelectedDesc()
					);
				  } else if (creatorInstance.wasExcluded()){
					  test.markExcluded(
							  creatorInstance.getExclusionType(),
							  creatorInstance.getExclusionDesc(),
							  creatorInstance.getExclusionIssueId()
					);
				  }
				if (test.shouldExecuteSetupTestFixture()){
					executeSetUpTestFor(test);
				}
	
				try{
					test.execute();
				} catch (Exception e){
					e.printStackTrace();
				}
	
				if (test.shouldExecuteTearDownTestFixture()){
					try{
						test.tearDownTest();
					} catch (Exception e){
						e.printStackTrace();
					}
				}
			} catch (Exception e){
				e.printStackTrace();
			}
		}
	}
}
