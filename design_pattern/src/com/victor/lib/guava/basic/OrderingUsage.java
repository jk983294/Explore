package com.victor.lib.guava.basic;


import com.google.common.base.Function;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.Lists;
import com.google.common.collect.Ordering;
import com.google.common.primitives.Ints;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * demo for ordering
 */
public class OrderingUsage {

    class Foo {
        String sortedBy;
        int notSortedBy;
    }

    public static void orderDemo(){
        List<String> list = Lists.newArrayList();
        list.add("peida");
        list.add("jerry");
        list.add("harry");
        list.add("eva");
        list.add("jhon");
        list.add("neron");

        System.out.println("list:"+ list);

        Ordering<String> naturalOrdering = Ordering.natural();
        System.out.println("naturalOrdering:"+ naturalOrdering.sortedCopy(list));

        List<Integer> listReduce= Lists.newArrayList();
        for(int i=9;i>0;i--){
            listReduce.add(i);
        }

        List<Integer> listtest= Lists.newArrayList();
        listtest.add(1);
        listtest.add(1);
        listtest.add(1);
        listtest.add(2);

        Ordering<Integer> naturalIntReduceOrdering = Ordering.natural();

        System.out.println("listtest:"+ listtest);
        System.out.println(naturalIntReduceOrdering.isOrdered(listtest));
        System.out.println(naturalIntReduceOrdering.isStrictlyOrdered(listtest));


        System.out.println("naturalIntReduceOrdering:"+ naturalIntReduceOrdering.sortedCopy(listReduce));
        System.out.println("listReduce:"+ listReduce);


        System.out.println(naturalIntReduceOrdering.isOrdered(naturalIntReduceOrdering.sortedCopy(listReduce)));
        System.out.println(naturalIntReduceOrdering.isStrictlyOrdered(naturalIntReduceOrdering.sortedCopy(listReduce)));


        Ordering<String> natural = Ordering.natural();

        List<String> abc = ImmutableList.of("a", "b", "c");
        System.out.println(natural.isOrdered(abc));
        System.out.println(natural.isStrictlyOrdered(abc));

        System.out.println("isOrdered reverse :"+ natural.reverse().isOrdered(abc));

        List<String> cba = ImmutableList.of("c", "b", "a");
        System.out.println(natural.isOrdered(cba));
        System.out.println(natural.isStrictlyOrdered(cba));
        System.out.println(cba = natural.sortedCopy(cba));

        System.out.println("max:"+natural.max(cba));
        System.out.println("min:"+natural.min(cba));

        System.out.println("leastOf:"+natural.leastOf(cba, 2));
        System.out.println("naturalOrdering:"+ naturalOrdering.sortedCopy(list));
        System.out.println("leastOf list:"+naturalOrdering.leastOf(list, 3));
        System.out.println("greatestOf:"+naturalOrdering.greatestOf(list, 3));
        System.out.println("reverse list :"+ naturalOrdering.reverse().sortedCopy(list));
        System.out.println("isOrdered list :"+ naturalOrdering.isOrdered(list));
        System.out.println("isOrdered list :"+ naturalOrdering.reverse().isOrdered(list));
        list.add(null);
        System.out.println("add null list:"+list);
        System.out.println("nullsFirst list :"+ naturalOrdering.nullsFirst().sortedCopy(list));
        System.out.println("nullsLast list :"+ naturalOrdering.nullsLast().sortedCopy(list));
    }

    public static void demo(){
        Ordering<String> byLengthOrdering = new Ordering<String>() {
            public int compare(String left, String right) {
                return Ints.compare(left.length(), right.length());
            }
        };

        Ordering<Foo> orderingObject = Ordering.natural().nullsFirst().onResultOf(new Function<Foo, String>() {
            public String apply(Foo foo) {
                return foo.sortedBy;
            }
        });


        List<Integer> numbers = new ArrayList<Integer>();

        numbers.add(new Integer(5));
        numbers.add(new Integer(2));
        numbers.add(new Integer(15));
        numbers.add(new Integer(51));
        numbers.add(new Integer(53));
        numbers.add(new Integer(35));
        numbers.add(new Integer(45));
        numbers.add(new Integer(32));
        numbers.add(new Integer(43));
        numbers.add(new Integer(16));

        Ordering ordering = Ordering.natural();
        System.out.println("Input List: ");
        System.out.println(numbers);

        Collections.sort(numbers,ordering );
        System.out.println("Sorted List: ");
        System.out.println(numbers);

        System.out.println("======================");
        System.out.println("List is sorted: " + ordering.isOrdered(numbers));
        System.out.println("Minimum: " + ordering.min(numbers));
        System.out.println("Maximum: " + ordering.max(numbers));

        Collections.sort(numbers,ordering.reverse());
        System.out.println("Reverse: " + numbers);

        numbers.add(null);
        System.out.println("Null added to Sorted List: ");
        System.out.println(numbers);

        Collections.sort(numbers,ordering.nullsFirst());
        System.out.println("Null first Sorted List: ");
        System.out.println(numbers);
        System.out.println("======================");

        List<String> names = new ArrayList<String>();

        names.add("Ram");
        names.add("Shyam");
        names.add("Mohan");
        names.add("Sohan");
        names.add("Ramesh");
        names.add("Suresh");
        names.add("Naresh");
        names.add("Mahesh");
        names.add(null);
        names.add("Vikas");
        names.add("Deepak");

        System.out.println("Another List: ");
        System.out.println(names);

        Collections.sort(names, ordering.nullsFirst().reverse());
        System.out.println("Null first then reverse sorted list: ");
        System.out.println(names);
    }

    public static void main(String[] args) {
        orderDemo();
        demo();
    }
}
