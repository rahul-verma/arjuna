package arjunasdk.sysauto.batteries;

import pvt.batteries.config.Batteries;

public class ThreadBatteries {

	public synchronized static String getCurrentThreadName() {
		return Thread.currentThread().getName();
	}

	public synchronized static Thread createThread(String threadName, Runnable runnable) throws Exception {
		Batteries.registerThread(ThreadBatteries.getCurrentThreadName(), threadName);
		return new Thread(runnable, threadName);
	}

	public synchronized static Thread createBaseThread(String threadName, Runnable runnable) throws Exception {
		Batteries.registerNewThread(threadName);
		return new Thread(runnable, threadName);
	}
}
