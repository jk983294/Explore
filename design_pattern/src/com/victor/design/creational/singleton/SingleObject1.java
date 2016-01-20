package com.victor.design.creational.singleton;

public class SingleObject1 {
    // lazy init
    private static SingleObject1 uniqueInstance;
    private SingleObject1() {
    }
    public static SingleObject1 getInstance() {
        if (uniqueInstance == null) {
            uniqueInstance = new SingleObject1();
        }
        return uniqueInstance;
    }

    public void showMessage(){
        System.out.println("Hello World!");
    }
}
