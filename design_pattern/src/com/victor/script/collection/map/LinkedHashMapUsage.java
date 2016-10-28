package com.victor.script.collection.map;

import java.util.LinkedHashMap;

public class LinkedHashMapUsage {

    public static void main(String[] args) {
        LinkedHashMap<Integer, Integer> map = new LinkedHashMap<>();
        map.put(1, 1);
        map.put(2, 2);
        map.put(3, 3);
        map.put(4, 4);
        map.put(null, 5);

        for(Integer i : map.keySet()){
            System.out.println(i + " -> " + map.get(i));
        }

        System.out.println(map.isEmpty());
        System.out.println(map.size());

        System.out.println(map.containsKey(null));
        System.out.println(map.containsKey(1));
        System.out.println(map.containsValue(10));

        map.remove(1);
        System.out.println(map.containsKey(1));
        map.clear();
    }

}
