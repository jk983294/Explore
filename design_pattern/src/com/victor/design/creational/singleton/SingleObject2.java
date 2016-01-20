package com.victor.design.creational.singleton;

public class SingleObject2 {
    // lazy init
    private static SingleObject2 uniqueInstance;
    private SingleObject2() {
    }

    // synchronized
    public static synchronized SingleObject2 getInstance() {
        if (uniqueInstance == null) {
            uniqueInstance = new SingleObject2();
        }
        return uniqueInstance;
    }

    public void showMessage(){
        System.out.println("Hello World!");
    }
}
