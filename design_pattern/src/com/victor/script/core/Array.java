package com.victor.script.core;

public class Array {

    public static void main(String[] args) {
        int[] a1 = new int[5];
        int[] a2 = {1, 2, 3, 4, 5};

        for (int i = 0; i < a2.length; i++) {
            System.out.println(i);
        }

        int[][] a3 = new int[5][5];
        int[][] a4 = {
                { 1, 2, 3 },
                { 4, 5, 6 },
                { 7, 8, 9 }
        };
    }
}
