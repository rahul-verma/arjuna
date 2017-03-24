/*******************************************************************************
 * Copyright 2015-16 AutoCognite Testing Research Pvt Ltd
 * 
 * Website: www.AutoCognite.com
 * Email: support [at] autocognite.com
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/
package pvt.unitee.runner.lib.slots;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.arjunapro.pvt.ArjunaInternal;
import com.arjunapro.sysauto.batteries.ThreadBatteries;
import com.arjunapro.testauto.config.RunConfig;

import pvt.unitee.testobject.lib.interfaces.TestContainer;

public class TestSlotExecutor{
	private static Logger logger = RunConfig.logger();
	private int slotNum;
	private TestSlot testSlot = null;
	private int classThreadCount = 1;

	public TestSlotExecutor (int slotNum, int classThreadCount, List<TestContainer> testContainers) throws Exception{
		this.slotNum = slotNum;
		this.testSlot = new TestSlot(slotNum, testContainers);
		this.classThreadCount = classThreadCount;
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Total test class units in slot# " + this.getSlotNumber() + ": " + testContainers.size());
		}
	}

	public void run() {
		ArrayList<Thread> testContainerThreads = new ArrayList<Thread>();
		Thread t = null;
		List<String> threadNames = new ArrayList<String>();
		for (int i = 1; i <= this.classThreadCount; i++){
			String threadName = String.format("S-%s|Sl-%d-CT-%d", Thread.currentThread().getName(), this.slotNum, i);
//			RunConfigSingleton.INSTANCE.setBucketNameForThread(threadName, "main");
			try{
				t = ThreadBatteries.createThread(threadName, new TestContainerExecutor(this.slotNum, this.testSlot));
				threadNames.add(t.getName());
				ArjunaInternal.getCentralExecState().registerThread(t.getName());
			} catch (Exception e){
				System.err.println("Critical Error: Exception occured while creating Test Slot Execution Thread.");
				e.printStackTrace();
				System.err.println("Exiting...");
				System.exit(1);
			}
			t.start();
			testContainerThreads.add(t);
		}
		try{
			for(Thread tLaunched : testContainerThreads){
				tLaunched.join();
			}	
		} catch (InterruptedException e){
			e.printStackTrace();
		}
		
		for (String tName: threadNames){
			ArjunaInternal.getCentralExecState().deregisterThread(tName);
		}
	}

	public int getSlotNumber() {
		return this.slotNum;
	}
}
