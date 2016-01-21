package com.victor.design.behavioral.template;

/**
 * an abstract class exposes defined way(s)/template(s) to execute its methods.
 * Its subclasses can override the method implementation as per need
 * but the invocation is to be in the same way as defined by an abstract class.
 */
public class TemplatePatternDemo {
    public static void main(String[] args) {

        Game game = new Cricket();
        game.play();
        System.out.println();
        game = new Football();
        game.play();
    }
}
