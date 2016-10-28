package com.victor.script.collection.map;

import java.util.WeakHashMap;

public class WeakHashMapUsage {

    public static void main (String args[]) {
        final WeakHashMap map = new WeakHashMap();
        map.put(new String("Maine"), "Augusta");

        Runnable runner = new Runnable() {
            public void run() {
                while (map.containsKey("Maine")) {
                    try {
                        Thread.sleep(500);
                    }catch (InterruptedException ignored) {
                    }
                    System.out.println("Thread waiting");

                    /**
                     * allows a key-value pair to be garbage-collected
                     * when its key is no longer referenced outside of the WeakHashMap.
                     */
                    System.gc();
                }
            }
        };
        Thread t = new Thread(runner);
        t.start();
        System.out.println("Main waiting");
        try {
            t.join();
        }catch (InterruptedException ignored) {
        }
    }

}
