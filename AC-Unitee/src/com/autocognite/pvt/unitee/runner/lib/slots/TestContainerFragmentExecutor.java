package com.autocognite.pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.utils.ThreadBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainer;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerFragment;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestContainerInstance;

public class TestContainerFragmentExecutor extends AbstractTestObjectExecutor implements Runnable{
	private static Logger logger = RunConfig.getCentralLogger();
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
				e.printStackTrace();
			}
		}

	}
}
