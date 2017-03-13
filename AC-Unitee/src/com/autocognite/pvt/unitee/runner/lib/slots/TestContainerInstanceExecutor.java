package com.autocognite.pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.utils.ThreadBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainer;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;

public class TestContainerInstanceExecutor implements Runnable{
	private static Logger logger = RunConfig.getCentralLogger();
	private TestSlotTestContainer slotTestContainer = null;
	private int slotNum;

	public TestContainerInstanceExecutor (int slotNum, TestSlotTestContainer slotTestContainer){
		this.slotNum = slotNum;
		this.slotTestContainer = slotTestContainer;
	}

	protected void executeSetUpClassInstanceFor(TestContainerInstance containerInstance){
		try{
			containerInstance.setUpClassInstance();	
		} catch (Throwable e){
			e.printStackTrace();
		}
	}
	
	protected void executeSetUpClassFragmentFor(TestContainerInstance containerInstance){
		try{
			containerInstance.setUpClassFragment();	
		} catch (Throwable e){
			e.printStackTrace();
		}
	}
	
	protected void executeTearDownClassFragmentFor(TestContainerInstance containerInstance){
		try{
			containerInstance.tearDownClassFragment();	
		} catch (Exception e){
			e.printStackTrace();
		}
	}
	
	protected void executeTearDownClassInstanceFor(TestContainerInstance containerInstance){
		try{
			containerInstance.tearDownClassInstance();	
		} catch (Exception e){
			e.printStackTrace();
		}
	}

//	protected void excludeForSetUpClassIssue(TestCreator testCreator){
//		try{
//			ExcludedTestReportableFactory.reportExcludedTestBecauseOfFixture(
//					testCreator.getTestVariables(),
//					ExclusionType.ERROR_IN_SETUP_CLASS, 
//					testCreator.getTestContainerInstance().getTestFixtures().getFixtureName(TestClassFixtureType.SETUP_CLASS)
//			);
//		} catch (Exception e){
//			e.printStackTrace();
//		}
//	}

	public void execute(TestSlotTestContainerInstance slotTestContainerInstance) throws Exception{
		TestContainerInstance testContainerInstance = slotTestContainerInstance.getContainerInstance();
		testContainerInstance.setThreadId(Thread.currentThread().getName());
		if (ArjunaInternal.logExclusionInfo){
			logger.debug(String.format("Exclusion Info: %s", testContainerInstance.getQualifiedName()));
			logger.debug(String.format("Is marked for exclusion? %s", testContainerInstance.wasExcluded()));
			logger.debug(String.format("Exclusion Type? %s", testContainerInstance.getExclusionType()));
			logger.debug(String.format("Exclusion Description? %s", testContainerInstance.getExclusionDesc()));
		}
		// Before venturing into launching test creators, setupclass is executed
		
		if ((!testContainerInstance.getTestVariables().objectProps().group().toLowerCase().equals("mlgroup") &&
		(testContainerInstance.shouldExecuteSetupClassInstanceFixture()))){
			if (ArjunaInternal.displayFixtureExecInfo){
				logger.debug(String.format("Attempting Set Up Class Instance for Test Class %s in Slot# %d", 
						testContainerInstance.getQualifiedName(),
						this.slotNum
						));
			}
	
			if (!testContainerInstance.wasSetUpClassInstanceFixtureExecuted()){
				if (ArjunaInternal.displayFixtureExecInfo){
					logger.debug("Set Up Class");
				}
				executeSetUpClassInstanceFor(testContainerInstance);
			}
			
			if (ArjunaInternal.logExclusionInfo){
				logger.debug("After Set Up Class");
				logger.debug(String.format("Exclusion Info: %s", testContainerInstance.getQualifiedName()));
				logger.debug(String.format("Is marked for exclusion? %s", testContainerInstance.wasExcluded()));
				logger.debug(String.format("Exclusion Type? %s", testContainerInstance.getExclusionType()));
				logger.debug(String.format("Exclusion Description? %s", testContainerInstance.getExclusionDesc()));
			}
		}
		
		if ((!testContainerInstance.getTestVariables().objectProps().group().toLowerCase().equals("mlgroup") &&
		 (testContainerInstance.shouldExecuteSetupClassFragmentFixture()))){
			if (ArjunaInternal.displayFixtureExecInfo){
				logger.debug(String.format("Attempting Set Up Class Fragment for Test Class %s in Slot# %d", 
						testContainerInstance.getQualifiedName(),
						this.slotNum
						));
			}
			
			executeSetUpClassFragmentFor(testContainerInstance);
			
			if (ArjunaInternal.logExclusionInfo){
				logger.debug("After Set Up Class");
				logger.debug(String.format("Exclusion Info: %s", testContainerInstance.getQualifiedName()));
				logger.debug(String.format("Is marked for exclusion? %s", testContainerInstance.wasExcluded()));
				logger.debug(String.format("Exclusion Type? %s", testContainerInstance.getExclusionType()));
				logger.debug(String.format("Exclusion Description? %s", testContainerInstance.getExclusionDesc()));
			}
		}
		
		if (ArjunaInternal.displaySlotsInfo){
			logger.debug(String.format("Now Executing Test Class %s methods in Slot# %d", 
				testContainerInstance.getQualifiedName(),
				this.slotNum
				));
		}
		ArrayList<Thread> containerInstanceThreads = new ArrayList<Thread>();
		Thread t;
		
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Launching threads for: Slot# %d - Test Container: %s - Instance #%d",
				this.slotNum, 
				testContainerInstance.getQualifiedName(), 
				testContainerInstance.getInstanceNumber()));
			logger.debug(String.format("Number of threads for running test creators: %d", testContainerInstance.getCreatorThreadCount()));
		}
		List<String> threadNames = new ArrayList<String>();
		for (int i = 1; i <= testContainerInstance.getCreatorThreadCount(); i++){
			String threadName = String.format("%s|CrT-%d", Thread.currentThread().getName(), i);
			try{
				t = ThreadBatteries.createThread(threadName, new TestCreatorExecutor(this.slotNum, slotTestContainerInstance));
				threadNames.add(t.getName());
				ArjunaInternal.getCentralExecState().registerThread(t.getName());
				t.start();
				containerInstanceThreads.add(t);
			} catch (Exception e){
				System.err.println("Critical Error: Exception occured while creating Test Slot Execution Thread.");
				e.printStackTrace();
				System.err.println("Exiting...");
				System.exit(1);
			}
		}
		try{
			for(Thread tLaunched : containerInstanceThreads){
				tLaunched.join();
			}	
		} catch (InterruptedException e){
			e.printStackTrace();
		}
		
		for (String tName: threadNames){
			ArjunaInternal.getCentralExecState().deregisterThread(tName);
		}
		
		if ((!testContainerInstance.getTestVariables().objectProps().group().toLowerCase().equals("mlgroup") &&
		(testContainerInstance.shouldExecuteTearDownClassFragmentFixture()))){
			if (testContainerInstance.hasFragmentCompleted()){
				this.executeTearDownClassFragmentFor(testContainerInstance);
				if (ArjunaInternal.displaySlotsInfo){
					logger.debug(String.format("All test instance creators in %s have finished for current execution slot. Tear down class fragment." , testContainerInstance.getQualifiedName()));
				}
			}
		}
		
		if ((!testContainerInstance.getTestVariables().objectProps().group().toLowerCase().equals("mlgroup") &&
		(testContainerInstance.shouldExecuteTearDownClassInstanceFixture()))){
			if (testContainerInstance.hasCompleted()){
				this.executeTearDownClassInstanceFor(testContainerInstance);
				if (ArjunaInternal.displaySlotsInfo){
					logger.debug(String.format("All scheduled test instance creators in %s have finished. Tear down class instance." , testContainerInstance.getQualifiedName()));
				}
			}
		}
		
		if (testContainerInstance.hasCompleted()){
			testContainerInstance.getContainer().markTestClassInstanceCompleted(testContainerInstance);
		}
	}

	public void run() {
		while(true){
			TestSlotTestContainerInstance slotTestContainerInstance = null;
			try{
				slotTestContainerInstance = this.slotTestContainer.next();
				TestContainer container = slotTestContainerInstance.getContainerInstance().getContainer();
				
					if (container.wasSkipped()){
					  slotTestContainerInstance.getContainerInstance().markSkipped(
							  container.getSkipType(),
							  container.getSkipDesc()
					);
				  } else if (container.wasUnSelected()){
					  slotTestContainerInstance.getContainerInstance().markUnSelected(
							  container.getUnSelectedType(),
							  container.getUnSelectedDesc()
					);
				  } else if (container.wasExcluded()){
				  slotTestContainerInstance.getContainerInstance().markExcluded(
						  container.getExclusionType(),
						  container.getExclusionDesc(),
						  container.getExclusionIssueId()
				);
			  }
			this.execute(slotTestContainerInstance);
			} catch (SubTestsFinishedException e){
				return;
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}

	}
}
