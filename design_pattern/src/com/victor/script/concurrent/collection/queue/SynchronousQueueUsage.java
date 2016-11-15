package com.victor.script.concurrent.collection.queue;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.SynchronousQueue;

/**
 * The SynchronousQueue is a queue that can only contain a single element internally.
 * A thread inserting an element into the queue is blocked until another thread takes that element from the queue.
 * Likewise, if a thread tries to take an element and no element is currently present,
 * that thread is blocked until a thread insert an element into the queue.
 */
public class SynchronousQueueUsage {

    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> queue   = new SynchronousQueue<>();

        queue.put("Value");

        String value = queue.take();
    }
}