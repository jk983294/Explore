package com.victor.script.concurrent.collection.queue;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

/**
 * The LinkedBlockingQueue keeps the elements internally in a linked structure (linked nodes).
 * This linked structure can optionally have an upper bound if desired.
 */
public class LinkedBlockingQueueUsage {

    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> unbounded = new LinkedBlockingQueue<String>();
        BlockingQueue<String> bounded   = new LinkedBlockingQueue<String>(1024);

        bounded.put("Value");

        String value = bounded.take();
    }
}