package com.victor.script.collection.limited;

import java.util.*;

public class QueueUsage {

    public static void queueUsage(){
        Queue<Integer> q = new LinkedList<>();
        q.add(1);
        q.offer(2);                                         // preferable for capacity-restricted queue

        System.out.println(q.isEmpty());
        System.out.println(q.size());

        System.out.println(q.peek());                       // get but don't remove, return null when empty
        System.out.println(q.element());                    // get but don't remove, throw exception when empty

        System.out.println(q.poll());                       // return null when empty
        System.out.println(q.remove());                     // throw exception when empty

        // better to use offer/peek/poll along with isEmpty/size
    }

    public static void dequeUsage(){
        Deque<Integer> q = new LinkedList<>();
        q.offerFirst(1);
        q.offerLast(2);

        System.out.println(q.isEmpty());
        System.out.println(q.size());

        System.out.println(q.peekFirst());
        System.out.println(q.peekLast());

        System.out.println(q.pollFirst());
        System.out.println(q.pollLast());
    }


    public static void main(String[] args) {
        queueUsage();
        dequeUsage();
    }

}
