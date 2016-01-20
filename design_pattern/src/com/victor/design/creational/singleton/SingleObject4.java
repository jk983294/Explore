package com.victor.design.creational.singleton;

public class SingleObject4 {
    // lazy init, if no volatile will encounter problem
    private static volatile SingleObject4 uniqueInstance;
    private SingleObject4() {
    }

    // double null check
    public static SingleObject4 getInstance() {
        if (uniqueInstance == null) {   // thread B could see this is not null, but not initialized yet
            synchronized (SingleObject4.class) {
                if (uniqueInstance == null) {
                    // (allocate, init, reference assign), may reorder to (reference assign, reference assign, init)
                    uniqueInstance = new SingleObject4();
                }
            }
        }
        return uniqueInstance;
    }

    public void showMessage(){
        System.out.println("Hello World!");
    }
}
