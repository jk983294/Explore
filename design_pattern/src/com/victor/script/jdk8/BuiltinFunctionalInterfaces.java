package com.victor.script.jdk8;

import java.util.Comparator;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;

/**
 * like Google Guava lib
 */
public class BuiltinFunctionalInterfaces {

    public static void predicate(){
        Predicate<String> predicate = (s) -> s.length() > 0;

        predicate.test("foo");              // true
        predicate.negate().test("foo");     // false

        Predicate<Boolean> nonNull = Objects::nonNull;
        Predicate<Boolean> isNull = Objects::isNull;

        Predicate<String> isEmpty = String::isEmpty;
        Predicate<String> isNotEmpty = isEmpty.negate();
    }

    public static void functions(){
        Function<String, Integer> toInteger = Integer::valueOf;
        Function<String, String> backToString = toInteger.andThen(String::valueOf);
        System.out.println(backToString.apply("123"));
    }

    public static void supplier(){
        Supplier<Person> personSupplier = Person::new;
        personSupplier.get();   // new Person
    }

    public static void consumer(){
        Consumer<Person> greeter = (p) -> System.out.println("Hello, " + p.firstName);
        greeter.accept(new Person("Luke", "Skywalker"));
    }

    public static void comparators(){
        Comparator<Person> comparator = (p1, p2) -> p1.firstName.compareTo(p2.firstName);
        Person p1 = new Person("John", "Doe");
        Person p2 = new Person("Alice", "Wonderland");
        comparator.compare(p1, p2);             // > 0
        comparator.reversed().compare(p1, p2);  // < 0
    }

    /**
     * Optional is a simple container for a value which may be null or non-null.
     * Think of a method which may return a non-null result but sometimes return nothing.
     * Instead of returning null you return an Optional in Java 8.
     */
    public static void optionals(){
        Optional<String> optional = Optional.of("bam");
        optional.isPresent();           // true
        optional.get();                 // "bam"
        optional.orElse("fallback");    // "bam"
        optional.ifPresent((s) -> System.out.println(s.charAt(0)));     // "b"
    }

    public static void main(String[] args){
        predicate();
        functions();
        supplier();
        consumer();
        comparators();
        optionals();
    }
}
