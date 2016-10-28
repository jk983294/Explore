package com.victor.script.collection;

import java.util.*;

public class CollectionsUsage {

    static class BigIntegerFirstComparator implements Comparator<Integer> {
        @Override
        public int compare(Integer e1, Integer e2) {
            return -e1.compareTo(e2);
        }
    }

    public static void main(String[] args) {
        List<Integer> l1 = new ArrayList<>(Arrays.asList(9, 2, 7, 4, 3, 4, 5, 8, 2, 10));
        List<Integer> l2 = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 4, 4, 7, 8, 9, 10));

        Collections.sort(l1);                                           // 2 2 3 4 4 5 7 8 9 10
        Collections.sort(l1, new BigIntegerFirstComparator());          // 10 9 8 7 5 4 4 3 2 2
        Comparator smallFirst = Collections.reverseOrder(new BigIntegerFirstComparator());
        Collections.sort(l1, smallFirst);                               // 2 2 3 4 4 5 7 8 9 10
        for(int i = 0; i < l1.size(); i++){
            System.out.print(l1.get(i) + " ");
        }
        System.out.println();

        System.out.println(Collections.max(l2));
        System.out.println(Collections.min(l2));

        System.out.println(Collections.binarySearch(l2, 2));
        System.out.println(Collections.binarySearch(l2, 4));
        System.out.println(Collections.binarySearch(l2, 6));
        System.out.println(Collections.binarySearch(l2, 11));

        List<Integer> l3 = new ArrayList<>(l2);
        Collections.fill(l3, 4);                                        // 4 4 4 4 4 4 4 4 4 4
        List<Integer> l4 = Collections.nCopies(3, 4);                   // 4 4 4

        Collections.replaceAll(l3, 4, 5);                               // 5 5 5 5 5 5 5 5 5 5

        Collections.reverse(l1);                                        // 10 9 8 7 5 4 4 3 2 2
        Collections.rotate(l1, 3);                                      // 3 2 2 10 9 8 7 5 4 4
        Collections.rotate(l1, -3);                                     // 10 9 8 7 5 4 4 3 2 2
        Collections.swap(l1, 0, 1);                                     // 9 10 8 7 5 4 4 3 2 2

        Collections.shuffle(l3);

        Set<Integer> s = Collections.singleton(1);
        List<Integer> l = Collections.singletonList(1);
        Map<Integer, Integer> m = Collections.singletonMap(1, 1);

        Set<Integer> ss = Collections.synchronizedSet(s);
        List<Integer> sl = Collections.synchronizedList(l);
        Map<Integer, Integer> sm = Collections.synchronizedMap(m);

        Set<Integer> us = Collections.unmodifiableSet(s);
        List<Integer> ul = Collections.unmodifiableList(l);
        Map<Integer, Integer> um = Collections.unmodifiableMap(m);
    }

}