package com.autocognite.arjuna.utils;

import com.autocognite.arjuna.config.RunConfig;

public class ThreadBatteries {

	public synchronized static String getCurrentThreadName() {
		return Thread.currentThread().getName();
	}

	public synchronized static Thread createThread(String threadName, Runnable runnable) throws Exception {
		RunConfig.registerThread(ThreadBatteries.getCurrentThreadName(), threadName);
		return new Thread(runnable, threadName);
	}

	public synchronized static Thread createBaseThread(String threadName, Runnable runnable) throws Exception {
		RunConfig.registerNewThread(threadName);
		return new Thread(runnable, threadName);
	}
}
