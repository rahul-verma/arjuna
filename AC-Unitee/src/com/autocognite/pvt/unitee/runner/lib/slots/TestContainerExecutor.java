package com.autocognite.pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.utils.ThreadBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.TestResultCode;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.reporter.lib.IssueId;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainer;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;

public class TestContainerExecutor implements Runnable{
	private static Logger logger = RunConfig.getCentralLogger();
	private TestSlot testSlot = null;
	private int slotNum;

	public TestContainerExecutor (int slotNum, TestSlot testSlot){
		this.slotNum = slotNum;
		this.testSlot = testSlot;
	}
	
	protected void executeSetUpClassFor(TestContainer container){
		try{
			container.setUpClass();	
		} catch (Throwable e){
			e.printStackTrace();
		}
	}
	
	protected void executeTearDownClassFor(TestContainer container){
		try{
			container.tearDownClass();	
		} catch (Throwable e){
			e.printStackTrace();
		}
	}

	public void execute(TestSlotTestContainer slotTestContainer) throws Exception{
		TestContainer testContainer = slotTestContainer.getTestContainer();
		testContainer.setThreadId(Thread.currentThread().getName());
		
		if (ArjunaInternal.displayFixtureExecInfo){
			logger.debug(String.format("Attempting Set Up Class for Test Class %s in Slot# %d", 
					testContainer.getQualifiedName(),
					this.slotNum
					));
		}
		
		if (ArjunaInternal.logExclusionInfo){
			logger.debug("After Set Up Class");
			logger.debug(String.format("Exclusion Info: %s", testContainer.getQualifiedName()));
			logger.debug(String.format("Is marked for exclusion? %s", testContainer.wasExcluded()));
			logger.debug(String.format("Exclusion Type? %s", testContainer.getExclusionType()));
			logger.debug(String.format("Exclusion Description? %s", testContainer.getExclusionDesc()));
		}
		
		if (testContainer.shouldExecuteSetupClassFixture()){
			if (ArjunaInternal.displayFixtureExecInfo){
				logger.debug(String.format("Attempting Set Up Class for Test Class %s in Slot# %d", 
						testContainer.getQualifiedName(),
						this.slotNum
						));
			}
	
			if (!testContainer.wasSetUpClassFixtureExecuted()){
				if (ArjunaInternal.displayFixtureExecInfo){
					logger.debug("Set Up Class");
				}
				executeSetUpClassFor(testContainer);
			}
			
			if (ArjunaInternal.logExclusionInfo){
				logger.debug("After Set Up Class");
				logger.debug(String.format("Exclusion Info: %s", testContainer.getQualifiedName()));
				logger.debug(String.format("Is marked for exclusion? %s", testContainer.wasExcluded()));
				logger.debug(String.format("Exclusion Type? %s", testContainer.getExclusionType()));
				logger.debug(String.format("Exclusion Description? %s", testContainer.getExclusionDesc()));
			}
		}
		
		ArrayList<Thread> testContainerInstanceExecutionThreads = new ArrayList<Thread>();
		Thread t;
		List<String> threadNames = new ArrayList<String>();
		if (ArjunaInternal.displaySlotsInfo){
			logger.debug(String.format("Launching threads for: Slot# %d - Test Container: %s", this.slotNum, testContainer.getQualifiedName()));
		}
		for (int i = 1; i <= testContainer.getInstanceThreadCount(); i++){
			if (ArjunaInternal.displaySlotsInfo){
				logger.debug(String.format("Thread: Slot# %d - Test Container: %s - Instance# %d", this.slotNum, testContainer.getQualifiedName(), i));
			}
			String threadName = String.format("%s|C-%s-CIT-%d", Thread.currentThread().getName(), testContainer.getQualifiedName(), i);
			try{
				t = ThreadBatteries.createThread(threadName, new TestContainerInstanceExecutor(this.slotNum, slotTestContainer));
				threadNames.add(t.getName());
				ArjunaInternal.getCentralExecState().registerThread(t.getName());
				t.start();
				testContainerInstanceExecutionThreads.add(t);
			} catch (Exception e){
				System.err.println("Critical Error: Exception occured while creating Test Slot Execution Thread.");
				e.printStackTrace();
				System.err.println("Exiting...");
				System.exit(1);
			}
		}
		try{
			for(Thread tLaunched : testContainerInstanceExecutionThreads){
				tLaunched.join();
			}	
		} catch (InterruptedException e){
			e.printStackTrace();
		}
		
		for (String tName: threadNames){
			ArjunaInternal.getCentralExecState().deregisterThread(tName);
		}
		
		if (testContainer.shouldExecuteTearDownClassFixture()){
			if (testContainer.hasCompleted()){
				this.executeTearDownClassFor(testContainer);
				if (ArjunaInternal.displaySlotsInfo){
					logger.debug(String.format("All test instances of %s have finished. Tear down class." , testContainer.getQualifiedName()));
				}
			}
		}
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
				e.printStackTrace();
			}
		}

	}
}
