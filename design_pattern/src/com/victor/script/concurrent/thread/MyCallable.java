package com.victor.script.concurrent.thread;


import java.util.concurrent.*;

public class MyCallable implements Callable<Integer> {

    @Override
    public Integer call() throws Exception {
        String threadName = Thread.currentThread().getName();
        System.out.println("Hello " + threadName);
        return 42;
    }

    public static void main(String args[]) {
        Callable<Integer> callable = new MyCallable();
        FutureTask<Integer> futureTask = new FutureTask<>(callable);

        Thread t=new Thread(futureTask);
        t.start();

        try {
            Integer result = futureTask.get();
            System.out.println(result);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}