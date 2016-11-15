package com.victor.script.concurrent.thread;


public class MyThread extends Thread {

    public void run() {
        String threadName = Thread.currentThread().getName();
        System.out.println("Hello " + threadName);
    }

    public static void main(String args[]) {
        new MyThread().start();
    }

}
