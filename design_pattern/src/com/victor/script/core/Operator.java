package com.victor.script.core;


public class Operator {

    public static void main(String[] args) {
        int flags = 0b110011;                   // binary literal

        System.out.println(flags << 2);         // left shift
        System.out.println(flags >> 2);         // right shift
        System.out.println(flags >>> 2);        // unsigned right shift

        int i = 1, j = 1;
        //int undefined = i++ - j++;            // one statement cannot contain several ++ --
    }

}
