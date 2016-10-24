package com.victor.script.collection.limited;

import java.util.ArrayDeque;

public class StackUsage {

    public static void main(String[] args) {
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        stack.offerLast(2);
        stack.offerLast(1);

        System.out.println(stack.isEmpty());
        System.out.println(stack.size());

        System.out.println(stack.peekLast());           // 1

        System.out.println(stack.pollLast());           // 1
        System.out.println(stack.pollLast());           // 2
    }

}
