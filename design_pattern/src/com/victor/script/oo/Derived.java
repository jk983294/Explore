package com.victor.script.oo;


public class Derived extends Base {

    private String d;

    public Derived() {
    }

    public Derived(String a, String b, String c, String d) {
        super(a, b, c);
        this.d = d;
    }

    public Derived(Derived another) {                         // copy ctor
        this.a = another.a;
        this.b = another.b;
        this.c = another.c;
        this.d = another.d;
    }

    public static void main(String[] args) {
        Derived d = new Derived("aaa", null, null, "d");
        System.out.println(d.d);

    }
}
