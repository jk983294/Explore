package com.victor.script.core;


public class Variable {

    public static void main(String[] args) {
        int flags = 0b110011;           // binary literal
        int x = 10_000_000;             // underscore in numeric literals
        double y = 10_000.00;

        System.out.println(flags);
        System.out.println(x);
        System.out.println(y);
    }

}
