package pvt.unitee.runner.lib.slots;

import org.apache.log4j.Logger;

import com.arjunapro.testauto.config.RunConfig;

import pvt.unitee.core.lib.exception.SubTestsFinishedException;
import pvt.unitee.testobject.lib.interfaces.TestCreator;
import pvt.unitee.testobject.lib.interfaces.TestCreatorInstance;

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
