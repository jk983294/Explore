package com.victor.script.concurrent.sync;

import java.util.LinkedList;
import java.util.concurrent.Semaphore;

/**
 * The counting semaphore is initialized with a given number of "permits".
 * For each call to acquire() a permit is taken by the calling thread.
 * For each call to release() a permit is returned to the semaphore.
 */
public class SemaphoreUsage {

    static class Queue {
        LinkedList<Integer> data = new LinkedList<>();

        Semaphore consumerCount = new Semaphore(0);
        Semaphore producerCount = new Semaphore(5);
        Semaphore mutex = new Semaphore(1);

        void get() throws InterruptedException {
            consumerCount.acquire();

            mutex.acquire();
            Integer value = data.removeFirst();
            System.out.println(Thread.currentThread().getName() + " got: " + value);
            mutex.release();

            producerCount.release();
        }

        void put(int n) throws InterruptedException {
            producerCount.acquire();

            mutex.acquire();
            data.offerLast(n);
            System.out.println(Thread.currentThread().getName() + " put: " + n);
            mutex.release();

            consumerCount.release();
        }
    }

    static class Producer implements Runnable {
        Queue q;

        Producer(Queue q, String name) {
            this.q = q;
            new Thread(this, name).start();
        }

        public void run() {
            for (int i = 0; i < 60; i++){
                try {
                    q.put(i);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    static class Consumer implements Runnable {
        Queue q;

        Consumer(Queue q, String name) {
            this.q = q;
            new Thread(this, name).start();
        }

        public void run() {
            for (int i = 0; i < 20; i++){
                try {
                    q.get();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }


    public static void main(String[] args) {
        Queue q = new Queue();
        new Consumer(q, "Consumer1");
        new Consumer(q, "Consumer2");
        new Consumer(q, "Consumer3");
        new Producer(q, "Producer1");
    }
}