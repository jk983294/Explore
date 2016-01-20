package com.victor.design.creational.abstractfactory;


import com.victor.design.model.color.Color;
import com.victor.design.model.shape.Shape;


/**
 * Abstract Factory patterns work around a super-factory which creates other factories.
 * This factory is also called as factory of factories.
 */
public abstract class AbstractFactory {
    abstract Color getColor(String color);
    abstract Shape getShape(String shape) ;
}
