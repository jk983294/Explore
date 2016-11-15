package com.victor.script.concurrent.sync.lock;

import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * It allows multiple threads to read a certain resource, but only one to write it, at a time.
 */
public class ReadWriteLockUsage {

    static class Data {
        int data;

        ReadWriteLock readWriteLock = new ReentrantReadWriteLock();

        void read() throws InterruptedException {
            readWriteLock.readLock().lock();

            System.out.println(Thread.currentThread().getName() + " read: " + data);

            readWriteLock.readLock().unlock();
        }

        void write(int n) throws InterruptedException {
            readWriteLock.writeLock().lock();

            data = n;
            System.out.println(Thread.currentThread().getName() + " write: " + data);

            readWriteLock.writeLock().unlock();
        }
    }

    static class Writer implements Runnable {
        Data d;

        Writer(Data d, String name) {
            this.d = d;
            new Thread(this, name).start();
        }

        public void run() {
            for (int i = 0; i < 60; i++){
                try {
                    d.write(i);
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    static class Reader implements Runnable {
        Data d;

        Reader(Data d, String name) {
            this.d = d;
            new Thread(this, name).start();
        }

        public void run() {
            for (int i = 0; i < 20; i++){
                try {
                    d.read();
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }


    public static void main(String[] args) {
        Data d = new Data();
        new Reader(d, "Reader1");
        new Reader(d, "Reader2");
        new Reader(d, "Reader3");
        new Writer(d, "Writer1");
    }

}
