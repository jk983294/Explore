package com.victor.script.concurrent.collection;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

/**
 * ConcurrentHashMap does not lock the Map while you are reading from it.
 * Additionally, ConcurrentHashMap does not lock the entire Map when writing to it.
 * It only locks the part of the Map that is being written to, internally.
 * it does not throw ConcurrentModificationException if the ConcurrentHashMap is changed while being iterated.
 */
public class ConcurrentHashMapUsage {

    public static void main(String[] args) {
        ConcurrentMap concurrentMap = new ConcurrentHashMap();

        concurrentMap.put("key", "value");

        Object value = concurrentMap.get("key");
    }
}