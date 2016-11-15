package com.victor.script.concurrent.collection.queue;

import java.util.concurrent.DelayQueue;
import java.util.concurrent.Delayed;
import java.util.concurrent.TimeUnit;

/**
 * The DelayQueue blocks the elements internally until a certain delay has expired.
 */
public class DelayQueueUsage {

    public static class DelayedElement implements Delayed {

        public long time;
        public String name;

        public DelayedElement(String name, long time) {
            this.time = time;
            this.name = name;
        }

        @Override
        public long getDelay(TimeUnit unit) {
            long r =  unit.convert(time - System.currentTimeMillis(), TimeUnit.MILLISECONDS);
            return r;
        }

        @Override
        public int compareTo(Delayed o) {
            if(this.time < ((DelayedElement)o).time) return -1;
            else if(this.time > ((DelayedElement)o).time)return 1;
            else return 0;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        DelayQueue<DelayedElement> queue = new DelayQueue<>();

        long now = System.currentTimeMillis();
        System.out.println("current time in ms: " + now);
        DelayedElement ob1 = new DelayedElement("e1", now + 1000);
        DelayedElement ob2 = new DelayedElement("e2", now + 5000);
        DelayedElement ob3 = new DelayedElement("e3", now + 1500);

        queue.add(ob1);
        queue.add(ob2);
        queue.add(ob3);

        Thread.sleep(1);

        while(queue.size() > 0){
            try {
                DelayedElement e = queue.take();
                System.out.println("current time in ms: " + System.currentTimeMillis() + ", element:" + e.name);
            } catch (InterruptedException e) {
                throw new RuntimeException( e );
            }
        }
    }
}