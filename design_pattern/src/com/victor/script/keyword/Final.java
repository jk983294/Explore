package com.victor.script.keyword;

public final class Final {          // A final class cannot be subclassed

    public final void f() {         // A final method cannot be overridden or hidden by subclasses
        System.out.println("final method can not be overridden.");
    }

    public final double radius;

    public Final() {
        radius = 1.0;               // A final variable can only be initialized once, either via an initializer or an assignment statement
    }

    public static void main(String[] args) {
        final Integer x = 5;

        new Runnable() {
            @Override
            public void run() {
                System.out.println(x);  //final allows variable to be accessed from inner class body
            }
        }.run();
    }
}
