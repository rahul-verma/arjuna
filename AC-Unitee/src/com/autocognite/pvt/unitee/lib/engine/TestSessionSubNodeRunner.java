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
package com.autocognite.pvt.unitee.lib.engine;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.utils.batteries.ThreadBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.core.lib.exception.SubTestsFinishedException;
import com.autocognite.pvt.unitee.testobject.lib.loader.session.SessionNode;
import com.autocognite.pvt.unitee.testobject.lib.loader.session.SessionSubNode;

public class TestSessionSubNodeRunner implements Runnable {
	private static Logger logger = RunConfig.logger();
	SessionNode sessionNode = null;
	
	public TestSessionSubNodeRunner(SessionNode sessionNode){
		this.sessionNode = sessionNode;
	}
	
	public void run(){
		SessionSubNode subNode = null;
		logger.debug(String.format("Session Node %s started.", this.sessionNode.getName()));
		while (true){
			try{
				subNode = this.sessionNode.next();
				String threadName = String.format("%s|G-%s", Thread.currentThread().getName(), subNode.getName());
				try{
					Thread t = ThreadBatteries.createThread(threadName, new TestSessionSubNodeSlotsRunner(subNode));
					ArjunaInternal.getCentralExecState().registerThread(t.getName());
					t.start();
					t.join();
					ArjunaInternal.getCentralExecState().deregisterThread(threadName);
				} catch (Exception e){
					System.err.println("Critical Error: Exception occured while creating Test Slot Execution Thread.");
					e.printStackTrace();
					System.err.println("Exiting...");
					System.exit(1);
				}
			} catch (SubTestsFinishedException e){
				logger.debug(String.format("Session Node %s finished.", sessionNode.getName()));
				break;
			} catch (Throwable e){
				logger.debug("Unexpected issue in Session runner.");
				e.printStackTrace();
				break;
			}
		}
	}
	
}


