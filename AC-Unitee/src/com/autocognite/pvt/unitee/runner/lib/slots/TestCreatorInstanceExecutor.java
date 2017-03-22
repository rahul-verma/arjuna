package com.autocognite.pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.utils.batteries.ThreadBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreator;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

public class TestCreatorInstanceExecutor extends AbstractTestObjectExecutor implements Runnable{
	private static Logger logger = RunConfig.logger();
	private int slotNum;
	private TestSlotTestCreator slotTestCreator = null;
	private TestCreatorInstance currentTestCreatorInstance = null;
	private TestSlotTestCreatorInstance currentSlotTestCreatorInstance = null;

	public TestCreatorInstanceExecutor(int slotNum, TestSlotTestCreator slotTestCreator) {
		super(slotNum);
		this.slotTestCreator = slotTestCreator;
	}

	protected int getChildThreadCount(){
		return currentTestCreatorInstance.getTestThreadCount();
	}

	protected String getThreadNameSuffix(int threadNum){
		return String.format("TT%d", threadNum);
	}

	protected Runnable createRunnable(){
		return new TestExecutor(this.getSlotNum(), currentSlotTestCreatorInstance);
	}

	public void execute(TestSlotTestCreatorInstance slotCreatorInstance) throws Exception{
		this.currentSlotTestCreatorInstance = slotCreatorInstance;
		currentTestCreatorInstance = slotCreatorInstance.getCreatorInstance();
		currentTestCreatorInstance.setThreadId(Thread.currentThread().getName());
		currentTestCreatorInstance.populateUserProps();

		this.executeSetUp(currentTestCreatorInstance);

		this.execute();

		this.executeTearDown(currentTestCreatorInstance);
	}

	public void run() {
		TestSlotTestCreatorInstance slotCreatorInstance = null;
		while(true){
			try{
				slotCreatorInstance  = this.slotTestCreator.next();
				TestCreator creator = slotCreatorInstance.getCreatorInstance().getParentTestCreator();

				copySchedulingStatusFromParentAndReturnFalseIfNotApplicable(creator, slotCreatorInstance.getCreatorInstance());

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
