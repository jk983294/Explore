package com.victor.script.concurrent.sync.lock;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * differences between a Lock and a synchronized block are:
 * A synchronized block makes no guarantees about the sequence in which threads waiting to entering it are granted access.
 * a timeout trying to get access to a synchronized block is not possible.
 * The synchronized block must be fully contained within a single method. A Lock can have it's calls to lock() and unlock() in separate methods.
 */
public class ReentrantLockUsage {

    static public class ThreadSafeArrayList<E>
    {
        private final Lock lock = new ReentrantLock();

        private final List<E> list = new ArrayList<>();

        private int i = 0;

        public void set(E o){
            lock.lock();

            try {
                i++;
                list.add(o);
                System.out.println("Adding element by thread" + Thread.currentThread().getName());
            }
            finally {
                lock.unlock();
            }
        }
    }

    public static void main(String[] args) {
        final ThreadSafeArrayList<String> list = new ThreadSafeArrayList<String>();

        Runnable syncThread = new Runnable(){
            @Override
            public void run(){
                while (list.i < 6){
                    list.set(String.valueOf(list.i));

                    try {
                        Thread.sleep(100);
                    }
                    catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        };
        Runnable lockingThread = new Runnable(){
            @Override
            public void run(){
                while (list.i < 6){
                    list.set(String.valueOf(list.i));
                    try {
                        Thread.sleep(100);
                    }
                    catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        };

        Thread t1 = new Thread(syncThread, "syncThread");
        Thread t2 = new Thread(lockingThread, "lockingThread");
        t1.start();
        t2.start();
    }

}