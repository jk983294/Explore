package com.victor.script.jdk8;

import com.victor.utilities.visual.VisualAssist;

/**
 * Interface Default Demo
 */
public class ExtensionMethodDemo {

    interface Formula {

        double calculate(int a);

        default double sqrt(int a) {
            return Math.sqrt(a);
        }
    }

    public static void main(String[] args){
        Formula formula = new Formula() {
            @Override
            public double calculate(int a) {
                return sqrt(a * 100);
            }
        };

        VisualAssist.print(formula.calculate(100));     // 100.0
        VisualAssist.print(formula.sqrt(100));          // 10.0

        /**
         * lambda could not call extension method in interface
         */
        //Formula formula = (a) -> sqrt( a * 100);
    }


}
