package com.victor.design.creational.factory;


import com.victor.design.model.shape.Circle;
import com.victor.design.model.shape.Rectangle;
import com.victor.design.model.shape.Shape;
import com.victor.design.model.shape.Square;

public class ShapeFactory {

    //use getShape method to get object of type shape
    public Shape getShape(String shapeType){
        if(shapeType == null){
            return null;
        }
        if(shapeType.equalsIgnoreCase("CIRCLE")){
            return new Circle();

        } else if(shapeType.equalsIgnoreCase("RECTANGLE")){
            return new Rectangle();

        } else if(shapeType.equalsIgnoreCase("SQUARE")){
            return new Square();
        }
        return null;
    }

}
