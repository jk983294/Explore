package com.victor.lib.guava.basic;



import com.google.common.base.Optional;
import com.google.common.base.Preconditions;

import static com.google.common.base.Preconditions.checkArgument;

/**
 * demo for basic utility
 */
public class BasicUsage {

    public static Integer sum(Optional<Integer> a, Optional<Integer> b) {
        //Optional.isPresent - checks the value is present or not
        System.out.println("First parameter is present: " + a.isPresent());
        System.out.println("Second parameter is present: " + b.isPresent());

        //Optional.or - returns the value if present otherwise returns
        //the default value passed.
        Integer value1 = a.or(new Integer(0));

        //Optional.get - gets the value, value should be present
        Integer value2 = b.get();

        return value1 + value2;
    }


    public static int sum(Integer a, Integer b){
        a = Preconditions.checkNotNull(a, "Illegal Argument passed: First parameter is Null.");
        b = Preconditions.checkNotNull(b, "Illegal Argument passed: Second parameter is Null.");
        return a+b;
    }

    public double sqrt(double input) throws IllegalArgumentException {
        Preconditions.checkArgument(input > 0.0,
                "Illegal Argument passed: Negative value %s.", input);
        return Math.sqrt(input);
    }

    /**
     * avoid null value
     */
    public static void optional(){
        Optional<Integer> possible = Optional.of(5);
        possible.isPresent(); // returns true
        possible.get(); // returns 5

        Integer value1 =  null;
        Integer value2 =  new Integer(10);

        //Optional.fromNullable - allows passed parameter to be null.
        Optional<Integer> a = Optional.fromNullable(value1);

        //Optional.of - throws NullPointerException if passed parameter is null
        Optional<Integer> b = Optional.of(value2);

        System.out.println(sum(a, b));
    }

    public static void preconditions(){
        int i = 0, j = 2;
        checkArgument(i >= 0, "Argument was %s but expected nonnegative", i);
        checkArgument(i < j, "Expected i < j, but %s > %s", i, j);
    }

    public static void main(String[] args) {
        optional();
        preconditions();
    }
}
