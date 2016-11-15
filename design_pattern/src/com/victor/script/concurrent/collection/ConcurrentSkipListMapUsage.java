package com.victor.script.concurrent.collection;

import java.util.concurrent.ConcurrentNavigableMap;
import java.util.concurrent.ConcurrentSkipListMap;

/**
 * support for concurrent access, and which has concurrent access enabled for its submaps.
 */
public class ConcurrentSkipListMapUsage {

    public static void main(String[] args) {
        ConcurrentNavigableMap map = new ConcurrentSkipListMap();

        map.put("1", "one");
        map.put("2", "two");
        map.put("3", "three");

        /**
         * headMap method returns a view of the map containing the keys < given key.
         * If you make changes to the original map, these changes are reflected in the head map.
         */
        ConcurrentNavigableMap headMap = map.headMap("2");

        /**
         * tailMap method returns a view of the map containing the keys >= given key.
         * If you make changes to the original map, these changes are reflected in the tail map
         */
        ConcurrentNavigableMap tailMap = map.tailMap("2");

        /**
         * subMap() method returns a view of the original map which contains all keys [from, to)
         */
        ConcurrentNavigableMap subMap = map.subMap("2", "3");
    }
}