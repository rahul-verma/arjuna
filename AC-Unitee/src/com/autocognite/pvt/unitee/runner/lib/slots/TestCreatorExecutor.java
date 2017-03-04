package com.autocognite.pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.batteries.config.RunConfig;
import com.autocognite.batteries.util.ThreadBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.TestResultCode;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.reporter.lib.IssueId;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreator;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

public class TestCreatorExecutor implements Runnable{
	private static Logger logger = RunConfig.getCentralLogger();
	private int slotNum;
	private TestSlotTestContainerInstance slotTestContainerInstance = null;

	public TestCreatorExecutor (int slotNum, TestSlotTestContainerInstance slotTestContainerInstance){
		this.slotNum = slotNum;
		this.slotTestContainerInstance = slotTestContainerInstance;
	}
	
	protected void executeSetUpMethodFor(TestCreator creator){
		try{
			creator.setUpMethod();	
		} catch (Exception e){
			e.printStackTrace();
		}
	}
	
	protected void executeTearDownMethodFor(TestCreator creator){
		try{
			creator.tearDownMethod();	
		} catch (Exception e){
			e.printStackTrace();
		}
	}

	public void execute(TestSlotTestCreator slotTestCreator) throws Exception{
		TestCreator testCreator = slotTestCreator.getTestCreator();
		testCreator.setThreadId(Thread.currentThread().getName());
		if (ArjunaInternal.logExclusionInfo){
			logger.debug(String.format("Exclusion Info: %s", testCreator.getQualifiedName()));
			logger.debug(String.format("Is marked for exclusion? %s", testCreator.wasExcluded()));
			logger.debug(String.format("Exclusion Type? %s", testCreator.getExclusionType()));
			logger.debug(String.format("Exclusion Description? %s", testCreator.getExclusionDesc()));
		}
		
		if (testCreator.shouldExecuteSetupMethodFixture()){
	
			if (!testCreator.wasSetUpMethodFixtureExecuted()){
				executeSetUpMethodFor(testCreator);
			}

		}
		ArrayList<Thread> creatorThreads = new ArrayList<Thread>();
		Thread t;
		
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Launching threads for: Slot# %d - Test Creator %s",
					this.slotNum, 
					testCreator.getQualifiedName()));
			logger.debug("Test Creator Instance Thread Count: " + testCreator.getInstanceThreadCount());
		}
		List<String> threadNames = new ArrayList<String>();
		for (int i = 1; i <= testCreator.getInstanceThreadCount(); i++){
			String threadName = String.format("%s|%s-CrIT%d", Thread.currentThread().getName(), testCreator.getName(), i);
			try{
				t = ThreadBatteries.createThread(threadName, new TestCreatorInstanceExecutor(this.slotNum, slotTestCreator));
				threadNames.add(t.getName());
				ArjunaInternal.getCentralExecState().registerThread(t.getName());
				t.start();
				creatorThreads.add(t);
			} catch (Exception e){
				System.err.println("Critical Error: Exception occured while creating Test Slot Execution Thread.");
				e.printStackTrace();
				System.err.println("Exiting...");
				System.exit(1);
			}
		}
		try{
			for(Thread tLaunched : creatorThreads){
				tLaunched.join();
			}	
		} catch (InterruptedException e){
			e.printStackTrace();
		}
		
		for (String tName: threadNames){
			ArjunaInternal.getCentralExecState().deregisterThread(tName);
		}
		
		if (testCreator.shouldExecuteTearDownMethodFixture()){
			if (testCreator.hasCompleted()){
				this.executeTearDownMethodFor(testCreator);
				if (ArjunaInternal.displaySlotsInfo){
					logger.debug(String.format("All test instance creators in %s have finished. Tear down class." , testCreator.getQualifiedName()));
				}
			}
		}
		
		testCreator.getTestContainerInstance().markTestCreatorCompleted(testCreator);
	}

	public void run() {
		while(true){
			TestSlotTestCreator slotTestCreator = null;
			
			try{
				slotTestCreator  = this.slotTestContainerInstance.next();
				if (ArjunaInternal.displaySlotsInfo){
					logger.debug("Executing Test Creator: " + slotTestCreator.getTestCreator().getQualifiedName());
				}
				
			TestContainerInstance containerInstance = slotTestCreator.getTestCreator().getTestContainerInstance();
			IssueId outId = new IssueId();
			if (containerInstance.wasSkipped()){
				slotTestCreator.getTestCreator().markSkipped(
						  containerInstance.getSkipType(),
						  containerInstance.getSkipDesc()
				);
			  } else if (containerInstance.wasUnSelected()){
				  slotTestCreator.getTestCreator().markUnSelected(
						  containerInstance.getUnSelectedType(),
						  containerInstance.getUnSelectedDesc()
				);
			  } else if (containerInstance.wasExcluded()){
				  slotTestCreator.getTestCreator().markExcluded(
						  containerInstance.getExclusionType(),
						  containerInstance.getExclusionDesc(),
						  containerInstance.getExclusionIssueId()
				);
			  } else if (!slotTestCreator.getTestCreator().shouldExecute(outId)){
				  slotTestCreator.getTestCreator().markExcluded(
						  TestResultCode.TEST_CREATOR_DEPENDENCY_NOTMET,
						  String.format("%s did not meet its dependencies.", slotTestCreator.getTestCreator().getName()),
						  outId.ID
				);
			  }
//					  try{
//						  ExcludedTestReportableFactory.reportExcludedTestBecauseOfDependencyFailure(
//								  slotTestCreator.getTestCreator().getTestVariables());
//					  } catch (Exception e) {
//						  // Exclusion related report exception, so being ignoed for the overall run tp continue
//						  e.printStackTrace();
//					  }
//					  TestCreator tcr = slotTestCreator.getTestCreator();
//					  tcr.getTestContainerInstance().markTestCreatorCompleted(tcr);
//					  continue;
//				  } else {
//					 
//				  }
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
