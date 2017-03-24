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
package pvt.unitee.lib.engine;

import org.apache.log4j.Logger;

import com.arjunapro.pvt.ArjunaInternal;
import com.arjunapro.sysauto.batteries.ThreadBatteries;
import com.arjunapro.testauto.config.RunConfig;

import pvt.unitee.core.lib.exception.SessionNodesFinishedException;
import pvt.unitee.testobject.lib.loader.session.Session;
import pvt.unitee.testobject.lib.loader.session.SessionNode;

public class TestSessionRunner implements Runnable {
	private static Logger logger = RunConfig.logger();
	Session session = null;
	
	public TestSessionRunner(Session session){
		this.session = session;
	}
	
	public void run(){
		if (session.getTestMethodCount() == 0){
			logger.fatal("No tests found as per provided configuration. Exiting.");
			return;
		}
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug("Number of Test Methods picked up: " + Integer.toString(session.getTestMethodCount()));
		}
		
		SessionNode node = null;
		int counter = 0;
		while (true){
			try{
				node = session.next();
			} catch (SessionNodesFinishedException e){
				logger.debug(String.format("Session %s finished.", this.session.getName()));
				break;
			} catch (Throwable e){
				logger.debug("Unexpected issue in Session runner.");
				e.printStackTrace();
			}
			
			logger.debug(String.format("Session: %s, Session Node: %s:: Creating Thread", this.session.getName(), node.getName()));
			Thread t;
			try{
				String tName = String.format("%s|n-%d-%s", Thread.currentThread().getName(), ++counter, node.getName());
				t = ThreadBatteries.createBaseThread(tName, new TestSessionNodeRunner(node));
				t.start();
				t.join();
			} catch (Exception e){
				System.err.println("Critical Error: Exception occured while session Thread.");
				e.printStackTrace();
				System.err.println("Exiting...");
				System.exit(1);
			}
		}
	}
	
}


