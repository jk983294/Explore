package com.victor.script.keyword;


import com.victor.script.oo.Base;
import com.victor.script.oo.Derived;

public class InstanceOf {

    public static void main(String[] args) {
        Base b = new Derived("aaa", null, null, "d");

        if(b instanceof Derived){
            System.out.println("b is instanceof Derived");
        }
    }
}
