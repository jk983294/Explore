package com.victor.script.collection.map;

import java.util.*;

public class TreeMapUsage {

    public static Map<Integer, Integer> sortByValues() {
        final TreeMap<Integer, Integer> map = new TreeMap<>();
        map.put(1, 4);
        map.put(2, 3);
        map.put(3, 2);
        map.put(4, 1);

        Comparator<Integer> valueComparator = new Comparator<Integer>() {
            public int compare(Integer k1, Integer k2) {
                int compare = map.get(k1).compareTo(map.get(k2));
                if (compare == 0)
                    return 1;
                else
                    return compare;
            }
        };

        Map<Integer, Integer> sortedByValues = new TreeMap<>(valueComparator);
        sortedByValues.putAll(map);

        for(Integer i : sortedByValues.keySet()){
            System.out.println(i + " -> " + map.get(i));
        }
        return sortedByValues;
    }

    public static void reverseOrder(){
        Map<Integer, Integer> map = new TreeMap<>(Collections.reverseOrder());
        map.put(1, 1);
        map.put(2, 2);
        map.put(3, 3);
        map.put(4, 4);
        for(Integer i : map.keySet()){
            System.out.println(i + " -> " + map.get(i));
        }
    }

    public static void main(String[] args) {
        TreeMap<Integer, Integer> map = new TreeMap<>();
        map.put(1, 1);
        map.put(2, 2);
        map.put(3, 3);
        map.put(4, 4);
        // map.put(null, 5);                                    // can not contains null key
        // System.out.println(map.containsKey(null));           // can not contains null key

        for(Integer i : map.keySet()){
            System.out.println(i + " -> " + map.get(i));
        }

        System.out.println(map.isEmpty());
        System.out.println(map.size());

        System.out.println(map.firstKey());
        System.out.println(map.lastKey());

        System.out.println(map.containsKey(1));
        System.out.println(map.containsValue(10));

        SortedMap<Integer, Integer> s1 = map.subMap(1, 3);          // [1, 3)
        for(Integer i : s1.keySet()){
            System.out.println(i + " -> " + map.get(i));
        }

        SortedMap<Integer, Integer> s2 = map.tailMap(1);            // [1, 4]
        for(Integer i : s2.keySet()){
            System.out.println(i + " -> " + map.get(i));
        }

        map.remove(1);
        System.out.println(map.containsKey(1));
        map.clear();

        reverseOrder();
        sortByValues();
    }

}
