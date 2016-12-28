package com.victor.script.jdk8;

import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * Lambda Demo
 */
public class LambdaDemo {

    public static void lambda(){
        List<String> names = Arrays.asList("peter", "anna", "mike", "xenia");

        Collections.sort(names, new Comparator<String>() {
            @Override
            public int compare(String a, String b) {
                return b.compareTo(a);
            }
        });

        /**
         * several different syntax sugar
         */
        Collections.sort(names, (String a, String b) -> {
            return b.compareTo(a);
        });

        Collections.sort(names, (String a, String b) -> b.compareTo(a));

        Collections.sort(names, (a, b) -> b.compareTo(a));
    }

    @FunctionalInterface
    interface Converter<F, T> {
        T convert(F from);
    }

    static class Something {
        String startsWith(String s) {
            return String.valueOf(s.charAt(0));
        }
    }

    public static void functionalInterface(){
        Converter<String, Integer> converter = (from) -> Integer.valueOf(from);
        Integer converted = converter.convert("123");
        System.out.println(converted);    // 123
    }

    public static void methodReference(){
        Converter<String, Integer> converter = Integer::valueOf;
        System.out.println(converter.convert("123"));   // 123

        Something something = new Something();
        Converter<String, String> converter1 = something::startsWith;
        System.out.println(converter1.convert("Java"));    // "J"
    }


    interface PersonFactory<P extends Person> {
        P create(String firstName, String lastName);
    }

    public static void ctorReference(){
        PersonFactory<Person> personFactory = Person::new;
        Person person = personFactory.create("Peter", "Parker");
        System.out.println(person.getFirstName());    // "J"
    }

    /**
     * could refer to static variable and member variable
     */
    static class LambdaVariableScope {
        static int outerStaticNum;
        int outerNum;

        void testScopes() {
            Converter<Integer, String> stringConverter1 = (from) -> {
                outerNum = 23;
                return String.valueOf(from);
            };

            Converter<Integer, String> stringConverter2 = (from) -> {
                outerStaticNum = 72;
                return String.valueOf(from);
            };
        }
    }

    public static void main(String[] args){
        lambda();
        functionalInterface();
        methodReference();
        ctorReference();
    }


}
