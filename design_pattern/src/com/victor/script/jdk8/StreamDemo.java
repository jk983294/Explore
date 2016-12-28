package com.victor.script.jdk8;

import java.util.*;
import java.util.concurrent.TimeUnit;

/**
 * stream demo
 */
public class StreamDemo {

    static List<String> stringCollection;

    static {
        System.out.println("init when class is loaded.");
        stringCollection = new ArrayList<>();
        stringCollection.add("ddd2");
        stringCollection.add("aaa2");
        stringCollection.add("bbb1");
        stringCollection.add("aaa1");
        stringCollection.add("bbb3");
        stringCollection.add("ccc");
        stringCollection.add("bbb2");
        stringCollection.add("ddd1");
    }

    public static void filter(){
        System.out.println("filter by startsWith 'a'");
        stringCollection.stream()
                .filter((s) -> s.startsWith("a"))
                .forEach(System.out::println);
    }

    /**
     * only stream view be sorted, not physical storage
     */
    public static void sorted(){
        System.out.println("sort then filter by startsWith 'a'");
        stringCollection.stream()
                .sorted()
                .filter((s) -> s.startsWith("a"))
                .forEach(System.out::println);
    }

    public static void map(){
        System.out.println("map to upper case then sort");
        stringCollection
                .stream()
                .map(String::toUpperCase)
                .sorted((a, b) -> b.compareTo(a))
                .forEach(System.out::println);
    }

    public static void reduce(){
        System.out.println("reduce to single result");
        Optional<String> reduced = stringCollection.stream()
                        .sorted()
                        .reduce((s1, s2) -> s1 + "#" + s2);
        reduced.ifPresent(System.out::println);
    }

    public static void match(){
        System.out.println("stream match");
        boolean anyStartsWithA =
                stringCollection
                        .stream()
                        .anyMatch((s) -> s.startsWith("a"));
        System.out.println(anyStartsWithA);      // true

        boolean allStartsWithA =
                stringCollection
                        .stream()
                        .allMatch((s) -> s.startsWith("a"));
        System.out.println(allStartsWithA);      // false

        boolean noneStartsWithZ =
                stringCollection
                        .stream()
                        .noneMatch((s) -> s.startsWith("z"));
        System.out.println(noneStartsWithZ);      // true
    }

    public static void count(){
        System.out.println("map to upper case then sort");
        long startsWithB = stringCollection.stream()
                .filter((s) -> s.startsWith("b"))
                .count();
        System.out.println(startsWithB);    // 3
    }

    public static void parallelStreams(){
        System.out.println("map to upper case then sort");
        int max = 1000000;
        List<String> values = new ArrayList<>(max);
        for (int i = 0; i < max; i++) {
            UUID uuid = UUID.randomUUID();
            values.add(uuid.toString());
        }

        long t0 = System.nanoTime();
        long count = values.stream().sorted().count();
        System.out.println(count);
        long t1 = System.nanoTime();
        long millis = TimeUnit.NANOSECONDS.toMillis(t1 - t0);
        System.out.println(String.format("sequential sort took: %d ms", millis));

        t0 = System.nanoTime();
        count = values.parallelStream().sorted().count();
        System.out.println(count);
        t1 = System.nanoTime();
        millis = TimeUnit.NANOSECONDS.toMillis(t1 - t0);
        System.out.println(String.format("parallel sort took: %d ms", millis));
    }

    public static void mapEnhancement(){
        System.out.println("map enhance method");
        Map<Integer, String> map = new HashMap<>();
        for (int i = 0; i < 10; i++) {
            map.putIfAbsent(i, "val" + i);
        }
        map.forEach((id, val) -> System.out.println(val));

        map.computeIfPresent(3, (num, val) -> val + num);
        map.get(3);             // val33
        map.computeIfPresent(9, (num, val) -> null);
        map.containsKey(9);     // false
        map.computeIfAbsent(23, num -> "val" + num);
        map.containsKey(23);    // true
        map.computeIfAbsent(3, num -> "bam");
        map.get(3);             // val33

        map.remove(3, "val3");
        map.get(3);             // val33
        map.remove(3, "val33");
        map.get(3);             // null

        map.getOrDefault(42, "not found");  // not found

        map.merge(9, "val9", (value, newValue) -> value.concat(newValue));
        map.get(9);             // val9
        map.merge(9, "concat", (value, newValue) -> value.concat(newValue));
        map.get(9);             // val9concat
    }

    public static void main(String[] args){
        filter();
        sorted();
        map();
        reduce();
        match();
        count();

        parallelStreams();
        mapEnhancement();
    }

}
