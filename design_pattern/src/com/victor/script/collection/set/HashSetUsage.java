package com.victor.script.collection.set;

import java.util.Arrays;
import java.util.HashSet;

public class HashSetUsage {

    public static void main(String[] args) {
        HashSet<Integer> set = new HashSet<>();
        set.add(1);
        set.addAll(Arrays.asList(2, 3, 4));

        for(Integer i : set){
            System.out.println(i);
        }

        System.out.println(set.isEmpty());
        System.out.println(set.size());

        System.out.println(set.contains(1));
        System.out.println(set.contains(10));

        set.remove(1);
        System.out.println(set.contains(1));
        set.clear();
    }

}
