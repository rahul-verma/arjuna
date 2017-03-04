package com.autocognite.pvt.batteries.threads;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.LinkedBlockingQueue;

public class ProducerConsumerQueue<T> {
	private BlockingQueue<T> sharedQueue = new LinkedBlockingQueue<T>();
	private ExecutorService producers = null;
	private ExecutorService consumers = null;

	public ProducerConsumerQueue(int producerThreadPoolSize, int consumerThreadPoolSize) {
		producers = Executors.newFixedThreadPool(producerThreadPoolSize);
		producers = Executors.newFixedThreadPool(consumerThreadPoolSize);
	}

	public void addProducer(Runnable r) {
		producers.submit(r);
	}

	public void addConsumer(Runnable r) {
		producers.submit(r);
	}

}
