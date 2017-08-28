package pvt.unitee.lib.engine;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import arjunasdk.config.RunConfig;
import arjunasdk.console.Console;
import arjunasdk.sysauto.batteries.ThreadBatteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.testobject.lib.loader.session.SessionNode;

public class TestSessionNodeRunner implements Runnable {
	private static Logger logger = RunConfig.logger();
	SessionNode sessionNode = null;

	public TestSessionNodeRunner(SessionNode node) {
		this.sessionNode = node;
	}

	public void run() {
		logger.debug(String.format("Session Node: %s:: Run begin", sessionNode.getName()));
		List<Thread> groupThreads = new ArrayList<Thread>();
		Thread t;
		List<String> threadNames = new ArrayList<String>();
		if (ArjunaInternal.displaySlotsInfo){
			logger.debug(String.format("Launching threads for session node: %s", this.sessionNode.getName()));
		}
		
		logger.debug(String.format("Session Node: %s:: Thread Count: %d", sessionNode.getName(), sessionNode.getGroupThreadCount()));		
		for (int i = 1; i <= sessionNode.getGroupThreadCount(); i++){
			String threadName = String.format("%s|T-%d", Thread.currentThread().getName(), i);
			try{
				t = ThreadBatteries.createThread(threadName, new TestSessionSubNodeRunner(this.sessionNode));
				threadNames.add(t.getName());
				ArjunaInternal.getGlobalState().registerThread(t.getName());
				t.start();
				groupThreads.add(t);
			} catch (Exception e){
				System.err.println("Critical Error: Exception occured while creating Test Slot Execution Thread.");
				Console.displayExceptionBlock(e);
				System.err.println("Exiting...");
				System.exit(1);
			}
		}
		
		try{
			for(Thread tLaunched : groupThreads){
				tLaunched.join();
			}	
		} catch (InterruptedException e){
			Console.displayExceptionBlock(e);
		}
		
		for (String tName: threadNames){
			ArjunaInternal.getGlobalState().deregisterThread(tName);
		}
		
		logger.debug(String.format("Session Node: %s:: Run end", sessionNode.getName()));
	}
	
}
