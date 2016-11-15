package com.victor.script.concurrent.executor;


import com.victor.script.concurrent.thread.MyCallable;
import com.victor.script.concurrent.thread.MyRunnable;
import com.victor.script.concurrent.thread.MyThread;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class SingleThreadExecutorUsage {

    public static void main(String[] args) {
        ExecutorService executorService = Executors.newSingleThreadExecutor();

        executorService.execute(new MyRunnable());
        executorService.execute(new MyThread());
        Future<Integer> result = executorService.submit(new MyCallable());
        Future result1 = executorService.submit(new MyRunnable());

        try {
            System.out.println(result.get());
            result1.get();
        } catch (Exception e) {
            e.printStackTrace();
        }

        executorService.shutdown();
    }
}