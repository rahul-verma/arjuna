package com.autocognite.pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.batteries.config.RunConfig;
import com.autocognite.batteries.util.ThreadBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreator;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

public class TestCreatorInstanceExecutor implements Runnable{
	private static Logger logger = RunConfig.getCentralLogger();
	private int slotNum;
	private TestSlotTestCreator slotTestCreator = null;
	
	public TestCreatorInstanceExecutor(int slotNum, TestSlotTestCreator slotTestCreator) {
		this.slotNum = slotNum;
		this.slotTestCreator = slotTestCreator;
	}
	
	protected void executeSetUpMethodInstanceFor(TestCreatorInstance creator){
		try{
			creator.setUpMethodInstance();	
		} catch (Exception e){
			e.printStackTrace();
		}
	}
	
	protected void executeTearDownMethodInstanceFor(TestCreatorInstance creator){
		try{
			creator.tearDownMethodInstance();	
		} catch (Exception e){
			e.printStackTrace();
		}
	}
	
	public void execute(TestSlotTestCreatorInstance slotCreatorInstance) throws Exception{
		TestCreatorInstance testCreatorInstance = slotCreatorInstance.getCreatorInstance();
		testCreatorInstance.setThreadId(Thread.currentThread().getName());
		if (testCreatorInstance.shouldExecuteSetupMethodInstanceFixture()){
	//		logger.debug(String.format("Attempting Set Up Method for %s.%s in Slot# %d",
	//				testCreator.getUserTestClassName(),
	//				testCreator.getName(),
	//				creatorUnit.getSlotNumber()
	//				));
	
			if (!testCreatorInstance.wasSetUpMethodInstanceFixtureExecuted()){
				executeSetUpMethodInstanceFor(testCreatorInstance);
			}
	
//			if (!testCreatorInstance.didSetUpMethodFixtureSucceed()){
//				excludeForSetUpMethodIssue(testCreatorInstance);
//				executeTearDownMethodFor(testCreatorInstance);
//				return;
//			}
		}
		
//		logger.debug(String.format("Now executing all test instances of %s.%s in Slot# %d",
//				testCreator.getUserTestClassName(),
//				testCreator.getName(),
//				creatorUnit.getSlotNumber()
//				));
		ArrayList<Thread> creatorInstanceThreads = new ArrayList<Thread>();
		Thread t = null;
		
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Launching threads for: Slot# %d - Test Creator %s - Instance# %d",
					this.slotNum, 
					testCreatorInstance.getQualifiedName(),
					testCreatorInstance.getInstanceNumber()));
			logger.debug(testCreatorInstance.getTestThreadCount());
		}
		List<String> threadNames = new ArrayList<String>();
		for (int i = 1; i <= testCreatorInstance.getTestThreadCount(); i++){
			String threadName = String.format("%s|TT%d", Thread.currentThread().getName(), i);
			try{
				t = ThreadBatteries.createThread(threadName, new TestExecutor(this.slotNum, slotCreatorInstance));
				threadNames.add(t.getName());
				ArjunaInternal.getCentralExecState().registerThread(t.getName());
			} catch (Exception e){
				System.err.println("Critical Error: Exception occured while creating Test Slot Execution Thread.");
				e.printStackTrace();
				System.err.println("Exiting...");
				System.exit(1);
			}
			t.start();
			creatorInstanceThreads.add(t);
		}
		try{
			for(Thread tLaunched : creatorInstanceThreads){
				tLaunched.join();
			}	
		} catch (InterruptedException e){
			e.printStackTrace();
		}
		
		
		for (String tName: threadNames){
			ArjunaInternal.getCentralExecState().deregisterThread(tName);
		}
		
		if (testCreatorInstance.shouldExecuteTearDownMethodInstanceFixture()){
			try{
				executeTearDownMethodInstanceFor(testCreatorInstance);
			} catch (Exception e){
				e.printStackTrace();
			}
		}
		
		testCreatorInstance.getParentTestCreator().markTestMethodInstanceCompleted(testCreatorInstance);
	}
	
   public void run() {
	  TestSlotTestCreatorInstance slotCreatorInstance = null;
	  while(true){
		  try{
			  slotCreatorInstance  = this.slotTestCreator.next();
			TestCreator creator = slotCreatorInstance.getCreatorInstance().getParentTestCreator();
			if (creator.wasSkipped()){
				slotCreatorInstance.getCreatorInstance().markSkipped(
						creator.getSkipType(),
						creator.getSkipDesc()
				);
			  } else if (creator.wasUnSelected()){
				  slotCreatorInstance.getCreatorInstance().markUnSelected(
						  creator.getUnSelectedType(),
						  creator.getUnSelectedDesc()
				);
			  } else if (creator.wasExcluded()){
				  slotCreatorInstance.getCreatorInstance().markExcluded(
						  creator.getExclusionType(),
						  creator.getExclusionDesc(),
						  creator.getExclusionIssueId()
				);
			  }
			  this.execute(slotCreatorInstance);
		  } catch (SubTestsFinishedException e){
			  return;
		  } catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	  }

   }
}
