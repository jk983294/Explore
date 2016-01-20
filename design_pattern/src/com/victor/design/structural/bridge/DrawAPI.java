package com.victor.design.structural.bridge;

/**
 * decouple an abstraction from its implementation.
 * this pattern decouples implementation class and abstract class by providing a bridge structure between them.
 * an interface which acts as a bridge which makes the functionality of concrete classes independent from
 * interface implementer classes.
 */
public interface DrawAPI {
    public void drawCircle(int radius, int x, int y);
}
