package com.victor.design.creational.singleton;

public class SingleObject3 {
    // lazy init
    private static SingleObject3 uniqueInstance;
    private SingleObject3() {
    }

    // nested inner class
    public static SingleObject3 getInstance(){
        return Nested.instance;
    }

    static class Nested{
        static SingleObject3 instance = new SingleObject3();
    }

    public void showMessage(){
        System.out.println("Hello World!");
    }
}
