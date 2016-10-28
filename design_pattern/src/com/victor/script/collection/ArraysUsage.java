package com.victor.script.collection;

import java.util.Arrays;
import java.util.List;

public class ArraysUsage {

    public static void main(String[] args) {
        List<Integer> list = Arrays.asList(1, 2, 3, 4);

        int[] a1 = {9, 2, 7, 4, 3, 4, 5, 8, 2, 10};
        int[] a2 = {1, 2, 3, 4, 4, 4, 7, 8, 9, 10};
        int[] a3 = new int[5];

        Arrays.sort(a1);                                        // 2 2 3 4 4 5 7 8 9 10
        for(int i = 0; i < a1.length; i++){
            System.out.print(a1[i] + " ");
        }
        System.out.println();

        System.out.println(Arrays.binarySearch(a2, 2));
        System.out.println(Arrays.binarySearch(a2, 4));
        System.out.println(Arrays.binarySearch(a2, 6));
        System.out.println(Arrays.binarySearch(a2, 11));



        Arrays.fill(a3, 4);                                     // 4 4 4 4 4
        Arrays.fill(a3, 0, 2, 8);                               // 8 8 4 4 4

        int[] a4 = Arrays.copyOf(a3, 7);                        // 8 8 4 4 4 0 0
        int[] a5 = Arrays.copyOf(a3, 3);                        // 8 8 4
        int[] a6 = Arrays.copyOfRange(a3, 1, 3);                // 8 4


        System.out.println(Arrays.equals(a1, a2));
        System.out.println(Arrays.hashCode(a1));
        System.out.println(Arrays.toString(a1));

        /**
         * for object equals, hash code, toString
         */
//        Arrays.deepEquals();
//        Arrays.deepHashCode();
//        Arrays.deepToString();
    }
}
