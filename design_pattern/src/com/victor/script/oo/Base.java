package com.victor.script.oo;


public class Base {

    protected String a = "a";                             // step 1
    protected String b = "b";
    protected String c;

    {   // initialisation block
        a = "aa";                                       // step 2
    }

    public Base() {
    }

    public Base(String a, String b, String c) {
        this.a = a;                                     // step 3
        this.b = b;
        this.c = c;
    }

    public Base(String a) {
        this(a, "b", "c");                              // ctor cascade
    }

    public Base(Base another) {                         // copy ctor
        this.a = another.a;
        this.b = another.b;
        this.c = another.c;
    }


    public static void main(String[] args) {
        Base p = new Base("aaa");
        System.out.println(p.a);

        Base p1 = new Base(p);
        System.out.println(p1.a);

    }
}
