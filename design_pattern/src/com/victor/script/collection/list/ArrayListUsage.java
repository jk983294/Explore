package com.victor.script.collection.list;

import com.victor.utilities.visual.VisualAssist;

import java.util.ArrayList;
import java.util.Arrays;

public class ArrayListUsage {

    public static void main(String[] args) {
        ArrayList<Integer> al = new ArrayList<>();
        ArrayList<Integer> al1 = new ArrayList<>();
        al.add(1);
        al.addAll(Arrays.asList(2, 3, 4, 4, 4, 6, 7, 8, 9));
        al.add(6, 5);                                       // shifts the element currently at that position (if any)

        VisualAssist.print(al);

        System.out.println(al.isEmpty());
        System.out.println(al.size());

        System.out.println(al.indexOf(4));                  // 3
        System.out.println(al.lastIndexOf(4));              // 5
        System.out.println(al.indexOf(10));                 // -1

        System.out.println(al.contains(3));                 // true
        System.out.println(al.contains(10));                // false

        al.set(0, 5);
        System.out.println(al.get(0));

        al.remove(8);                                       // remove al[8]
        VisualAssist.print(al);
        al.remove(Integer.valueOf(9));                      // remove object 9
        VisualAssist.print(al);
        al.clear();
        VisualAssist.print(al);


        al.addAll(Arrays.asList(2, 3, 4, 4, 4, 6, 7, 8, 9));
        al1.addAll(Arrays.asList(2, 3));
        al.removeAll(al1);                                  // get A - B
        VisualAssist.print(al);
        al.addAll(0, al1);
        VisualAssist.print(al);
        al.retainAll(al1);                                  // get A & B
        VisualAssist.print(al);
    }

}
