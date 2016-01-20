package com.victor.design.structural.flyweight;

import com.victor.design.model.shape.Circle;
import com.victor.design.model.shape.Shape;

import java.util.HashMap;

/**
 * Flyweight pattern is primarily used to reduce the number of objects created and to decrease memory footprint
 * and increase performance.
 * Flyweight pattern tries to reuse already existing similar kind objects by storing them
 * and creates new object when no matching object is found.
 */
public class ShapeFactory {
    private static final HashMap<String, Shape> circleMap = new HashMap();

    public static Shape getCircle(String color) {
        Circle circle = (Circle)circleMap.get(color);   // reuse existing colored circle

        if(circle == null) {
            circle = new Circle(color);
            circleMap.put(color, circle);
            System.out.println("Creating circle of color : " + color);
        }
        return circle;
    }
}
