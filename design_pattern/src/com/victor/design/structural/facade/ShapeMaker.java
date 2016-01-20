package com.victor.design.structural.facade;

import com.victor.design.model.shape.Circle;
import com.victor.design.model.shape.Rectangle;
import com.victor.design.model.shape.Shape;
import com.victor.design.model.shape.Square;

/**
 * this pattern adds an interface to existing system to hide its complexities.
 * This pattern involves a single class which provides simplified methods required by client
 * and delegates calls to methods of existing system classes.
 */
public class ShapeMaker {
    private Shape circle;
    private Shape rectangle;
    private Shape square;

    public ShapeMaker() {
        circle = new Circle();
        rectangle = new Rectangle();
        square = new Square();
    }

    public void drawCircle(){
        circle.draw();
    }
    public void drawRectangle(){
        rectangle.draw();
    }
    public void drawSquare(){
        square.draw();
    }
}
