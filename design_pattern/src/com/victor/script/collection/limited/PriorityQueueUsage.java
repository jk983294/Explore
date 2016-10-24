package com.victor.script.collection.limited;

import java.util.Comparator;
import java.util.PriorityQueue;

public class PriorityQueueUsage {

    static class BigIntegerFirstComparator implements Comparator<Integer> {
        @Override
        public int compare(Integer e1, Integer e2) {
            return -e1.compareTo(e2);
        }
    }

    public static void main(String[] args) {
        /**
         * default priority is small first
         */
        PriorityQueue<Integer> q = new PriorityQueue<>(10, new BigIntegerFirstComparator());
        q.offer(1);
        q.offer(2);

        System.out.println(q.isEmpty());
        System.out.println(q.size());

        System.out.println(q.peek());

        System.out.println(q.poll());
        System.out.println(q.poll());
    }
}
