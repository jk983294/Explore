package com.victor.script.concurrent.atomic;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * a boolean variable which can be read and written atomically
 */
public class AtomicIntegerUsage {

    public static void main(String[] args) {
        AtomicInteger atomicInteger = new AtomicInteger();
        AtomicInteger atomicInteger1 = new AtomicInteger(123);

        int theValue = atomicInteger.get();

        atomicInteger.set(234);

        int oldValue = atomicInteger.getAndSet(123);

        int expectedValue = 123;
        int newValue      = 234;
        boolean wasNewValueSet = atomicInteger.compareAndSet(expectedValue, newValue);
        System.out.println(wasNewValueSet);

        System.out.println(atomicInteger.getAndAdd(10));
        System.out.println(atomicInteger.addAndGet(10));
        System.out.println(atomicInteger.getAndIncrement());
        System.out.println(atomicInteger.incrementAndGet());

        System.out.println(atomicInteger.getAndDecrement());
        System.out.println(atomicInteger.decrementAndGet());
    }
}