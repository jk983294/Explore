package com.victor.script.concurrent.thread;


public class MyRunnable implements Runnable {

    @Override
    public void run() {
        String threadName = Thread.currentThread().getName();
        System.out.println("Hello " + threadName);
    }

    public static void main(String args[]) {
        new Thread(new MyRunnable()).start();
    }

}