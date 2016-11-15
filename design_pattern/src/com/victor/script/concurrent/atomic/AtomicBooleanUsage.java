package com.victor.script.concurrent.atomic;

import java.util.concurrent.atomic.AtomicBoolean;

/**
 * a boolean variable which can be read and written atomically
 */
public class AtomicBooleanUsage {

    public static void main(String[] args) {
        AtomicBoolean atomicBoolean = new AtomicBoolean();
        AtomicBoolean atomicBoolean1 = new AtomicBoolean(true);

        boolean value = atomicBoolean.get();

        atomicBoolean.set(false);

        boolean oldValue = atomicBoolean.getAndSet(true);

        boolean expectedValue = true;
        boolean newValue      = false;

        boolean wasNewValueSet = atomicBoolean.compareAndSet(expectedValue, newValue);
        System.out.println(wasNewValueSet);
    }
}