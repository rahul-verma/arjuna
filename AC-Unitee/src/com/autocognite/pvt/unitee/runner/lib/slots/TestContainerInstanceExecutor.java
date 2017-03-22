package com.autocognite.pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.utils.batteries.ThreadBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainer;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestObject;

public class TestContainerInstanceExecutor extends AbstractTestObjectExecutor implements Runnable{
	private static Logger logger = RunConfig.logger();
	private TestSlotTestContainer slotTestContainer = null;
	private TestContainerInstance currentTestContainerInstance = null;
	private TestSlotTestContainerInstance currentSlotsContainerInstance = null;

	public TestContainerInstanceExecutor (int slotNum, TestSlotTestContainer slotTestContainer){
		super(slotNum);
		this.slotTestContainer = slotTestContainer;
	}

	protected int getChildThreadCount(){
		return 1;
	}

	protected String getThreadNameSuffix(int threadNum){
		return "T-1";
	}

	protected Runnable createRunnable(){
		return new TestContainerFragmentExecutor(this.getSlotNum(), currentSlotsContainerInstance);
	}

	public void execute(TestSlotTestContainerInstance slotTestContainerInstance) throws Exception{
		this.currentSlotsContainerInstance = slotTestContainerInstance;
		currentTestContainerInstance = slotTestContainerInstance.getContainerInstance();
		currentTestContainerInstance.setThreadId(Thread.currentThread().getName());
		currentTestContainerInstance.populateUserProps();

		this.executeSetUp(currentTestContainerInstance);

		this.execute();

		this.executeTearDown(currentTestContainerInstance);

		if (ArjunaInternal.displaySlotsInfo){
			logger.debug(String.format("Check if  %s class instance has completed." , currentTestContainerInstance.getQualifiedName()));
		}
		if (currentTestContainerInstance.hasCompleted()){
			if (ArjunaInternal.displaySlotsInfo){
				logger.debug(String.format("Class instance  %s completed. Update class and mark this instance completed." , currentTestContainerInstance.getQualifiedName()));
			}
			currentTestContainerInstance.getContainer().markTestClassInstanceCompleted(currentTestContainerInstance);
			if (ArjunaInternal.displaySlotsInfo){
				logger.debug("Updated");
			}
		}
	}

	public void run() {
		while(true){
			TestSlotTestContainerInstance slotTestContainerInstance = null;
			try{
				slotTestContainerInstance = this.slotTestContainer.next();
				TestContainer container = slotTestContainerInstance.getContainerInstance().getContainer();

				copySchedulingStatusFromParentAndReturnFalseIfNotApplicable(container, slotTestContainerInstance.getContainerInstance());

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
