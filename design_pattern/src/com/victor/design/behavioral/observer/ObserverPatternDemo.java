package com.victor.design.behavioral.observer;

/**
 * Observer pattern is used when there is one-to-many relationship between objects such as
 * if one object is modified, its depenedent objects are to be notified automatically.
 *
 * Subject is an object having methods to attach and detach observers to a client object.
 */
public class ObserverPatternDemo {
    public static void main(String[] args) {
        Subject subject = new Subject();

        new HexaObserver(subject);
        new OctalObserver(subject);
        new BinaryObserver(subject);

        System.out.println("First state change: 15");
        subject.setState(15);
        System.out.println("Second state change: 10");
        subject.setState(10);
    }
}
