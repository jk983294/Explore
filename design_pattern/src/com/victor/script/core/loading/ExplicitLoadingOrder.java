package com.victor.script.core.loading;


public class ExplicitLoadingOrder {

    GB gb;

    public ExplicitLoadingOrder() {
        this.gb = new GB();
    }

    public static void main(String[] args) {

        try {
            Class<?> cls = Class.forName("com.victor.script.core.loading.GB");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

        System.out.println("very beginning...");
        ExplicitLoadingOrder order = new ExplicitLoadingOrder();
        System.out.println("order alive...");
    }
}
