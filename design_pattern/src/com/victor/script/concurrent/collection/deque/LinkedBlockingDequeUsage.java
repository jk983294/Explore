package com.victor.script.concurrent.collection.deque;

import java.util.concurrent.BlockingDeque;
import java.util.concurrent.LinkedBlockingDeque;

/**
 * The BlockingDeque interface represents a deque which is thread safe to put into, and take instances from.
 * it will block if a thread attempts to take elements out of it while it is empty,
 * regardless of what end the thread is attempting to take elements from.
 */
public class LinkedBlockingDequeUsage {

    public static void main(String[] args) throws InterruptedException {
        BlockingDeque<String> deque = new LinkedBlockingDeque<>();

        deque.addFirst("1");
        deque.addLast("2");

        String two = deque.takeLast();
        String one = deque.takeFirst();
    }

}