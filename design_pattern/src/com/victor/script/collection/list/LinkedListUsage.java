package com.victor.script.collection.list;

import com.victor.utilities.visual.VisualAssist;

import java.util.Arrays;
import java.util.LinkedList;

public class LinkedListUsage {

    public static void main(String[] args) {
        LinkedList<Integer> ll = new LinkedList<>();
        LinkedList<Integer> ll1 = new LinkedList<>();
        ll.add(1);
        ll.addAll(Arrays.asList(2, 3, 4, 4, 4, 6, 7, 8, 9));
        ll.add(6, 5);                                       // shifts the element currently at that position (if any)

        VisualAssist.print(ll);

        System.out.println(ll.isEmpty());
        System.out.println(ll.size());

        System.out.println(ll.indexOf(4));                  // 3
        System.out.println(ll.lastIndexOf(4));              // 5
        System.out.println(ll.indexOf(10));                 // -1

        System.out.println(ll.contains(3));                 // true
        System.out.println(ll.contains(10));                // false

        ll.set(0, 5);
        System.out.println(ll.get(0));

        ll.remove(8);                                       // remove al[8]
        VisualAssist.print(ll);
        ll.remove(Integer.valueOf(9));                      // remove object 9
        VisualAssist.print(ll);
        ll.clear();
        VisualAssist.print(ll);


        ll.addAll(Arrays.asList(2, 3, 4, 4, 4, 6, 7, 8, 9));
        ll1.addAll(Arrays.asList(2, 3));
        ll.removeAll(ll1);                                  // get A - B
        VisualAssist.print(ll);
        ll.addAll(0, ll1);
        VisualAssist.print(ll);
        ll.retainAll(ll1);                                  // get A & B
        VisualAssist.print(ll);
    }

}
