package pvt.batteries.threads;

import java.util.concurrent.BlockingQueue;

public abstract class ProducerThread<T> {
	private BlockingQueue<T> sharedQueue = null;
	private int threadNumber;

	public ProducerThread(BlockingQueue<T> sharedQueue, int threadNumber) {
		this.sharedQueue = sharedQueue;
		this.threadNumber = threadNumber;
	}

	public abstract void run();
}
