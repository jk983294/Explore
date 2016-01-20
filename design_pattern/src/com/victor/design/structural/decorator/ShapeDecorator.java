package com.victor.design.structural.decorator;

/**
 * Decorator pattern allows to add new functionality to an existing object without altering its structure.
 * this pattern acts as a wrapper to existing class.
 * This pattern creates a decorator class which wraps the original class and provides additional functionality.
 *
 * decorate a shape with some color without alter shape class.
 */
public abstract class ShapeDecorator implements Shape {
    protected Shape decoratedShape;

    public ShapeDecorator(Shape decoratedShape){
        this.decoratedShape = decoratedShape;
    }

    public void draw(){
        decoratedShape.draw();
    }
}
