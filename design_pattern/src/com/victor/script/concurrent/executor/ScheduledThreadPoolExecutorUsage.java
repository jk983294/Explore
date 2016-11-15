package com.victor.script.concurrent.executor;


import com.victor.script.concurrent.thread.MyCallable;
import com.victor.script.concurrent.thread.MyRunnable;
import com.victor.script.concurrent.thread.MyThread;

import java.util.concurrent.*;

public class ScheduledThreadPoolExecutorUsage {

    public static void main(String[] args) {
        ScheduledExecutorService executorService = Executors.newScheduledThreadPool(10);

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

        executorService.schedule(new MyRunnable(), 42, TimeUnit.SECONDS);
        executorService.schedule(new MyCallable(), 42, TimeUnit.SECONDS);
        /**
         * periodic action
         * scheduleAtFixedRate run again at fixed delay no matter current task finished or not
         * scheduleWithFixedDelay run again when current task finished + fixed delay
         */
        executorService.scheduleAtFixedRate(new MyRunnable(), 24, 42, TimeUnit.SECONDS);
        executorService.scheduleWithFixedDelay(new MyRunnable(), 24, 42, TimeUnit.SECONDS);

        executorService.shutdown();
    }
}