package com.victor.script.concurrent.sync;

import java.util.concurrent.CountDownLatch;

/**
 * allows one or more threads to wait for a given set of operations to complete.
 * threads call await() blocks the thread until the count reaches zero.
 */
public class CountDownLatchUsage {

    public static class Waiter implements Runnable{

        CountDownLatch latch = null;

        public Waiter(CountDownLatch latch) {
            this.latch = latch;
        }

        public void run() {
            try {
                latch.await();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("Waiter Released");
        }
    }

    public static class Decrementer implements Runnable {

        CountDownLatch latch = null;

        public Decrementer(CountDownLatch latch) {
            this.latch = latch;
        }

        public void run() {
            try {
                Thread.sleep(1000);
                this.latch.countDown();

                Thread.sleep(1000);
                this.latch.countDown();

                Thread.sleep(1000);
                this.latch.countDown();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        CountDownLatch latch = new CountDownLatch(3);

        Waiter      waiter      = new Waiter(latch);
        Decrementer decrementer = new Decrementer(latch);

        new Thread(waiter)     .start();
        new Thread(decrementer).start();

        Thread.sleep(4000);
    }
}