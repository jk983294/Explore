package com.victor.script.concurrent.collection.queue;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.PriorityBlockingQueue;

/**
 * The PriorityBlockingQueue is an unbounded concurrent queue.
 * You cannot insert null into this queue.
 * it does not enforce any specific behaviour for elements that have equal priority (compare() == 0).
 * when obtain an Iterator from a PriorityBlockingQueue, the Iterator does not guarantee to iterate the elements in priority order.
 */
public class PriorityBlockingQueueUsage {

    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> queue   = new PriorityBlockingQueue<>();

        //String implements java.lang.Comparable
        queue.put("Value");

        String value = queue.take();
    }
}