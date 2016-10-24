package com.victor.script.core.loading;

/**
 * implicit loading
 * when first object created (like GB)
 * when static method or field referenced
 */
public class ImplicitLoadingOrder {

    GB gb;

    public ImplicitLoadingOrder() {
        this.gb = new GB();
    }

    public static void main(String[] args) {
        System.out.println("very beginning...");
        ImplicitLoadingOrder order = new ImplicitLoadingOrder();
        System.out.println("order alive...");
    }
}
