package com.victor.design.aop;

public class DogImp implements AnimalInterface {

    @Seven(value = "dogie")
    private String name;

    private String Property;

    public DogImp() {
    }

    @Override
    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String getName() {
        return this.name;
    }

    @Override
    public void say() {
        System.err.println("dog: wang wang wang.....");
    }

    @Override
    @Seven(Property = "warrior")
    public void setProperty(String Property) {
        this.Property = Property;
    }

    @Override
    public void getProperty() {
        System.err.println(this.name + this.Property);
    }
}
