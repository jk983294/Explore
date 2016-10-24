package com.victor.script.collection.set;

import java.util.Arrays;
import java.util.Comparator;
import java.util.TreeSet;

public class TreeSetUsage {

    static class BigIntegerFirstComparator implements Comparator<Integer> {
        @Override
        public int compare(Integer e1, Integer e2) {
            return -e1.compareTo(e2);
        }
    }

    public static void main(String[] args) {
        TreeSet<Integer> set = new TreeSet<>(new BigIntegerFirstComparator());
        set.add(1);
        set.addAll(Arrays.asList(2, 3, 4));

        for(Integer i : set){                           // differ from HashSet, it is sorted
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
