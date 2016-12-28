package com.victor.lib.guava.utilities;

import com.google.common.base.CaseFormat;
import com.google.common.primitives.*;
import com.victor.utilities.visual.VisualAssist;

import java.util.List;


/**
 * PrimitiveUtilities Bytes Shorts Ints Longs Floats Doubles Chars Booleans
 */
public class PrimitiveUtilitiesUsage {

    public static void main(String[] args) {
        bytes();
        shorts();
        ints();
        longs();
        floats();
        doubles();
        chars();
        booleans();
    }

    public static void bytes(){
        byte[] byteArray = {1,2,3,4,5,5,7,9,9};
        //convert array of primitives to array of objects
        List<Byte> objectArray = Bytes.asList(byteArray);
        System.out.println(objectArray.toString());
        //convert array of objects to array of primitives
        byteArray = Bytes.toArray(objectArray);
        VisualAssist.print("byte arrays", byteArray);
        byte data = 5;
        //check if element is present in the list of primitives or not
        System.out.println("5 is in list? " + Bytes.contains(byteArray, data));
        //Returns the index
        System.out.println("Index of 5: " + Bytes.indexOf(byteArray,data));
        //Returns the last index maximum
        System.out.println("Last index of 5: " + Bytes.lastIndexOf(byteArray,data));
    }

    public static void shorts(){
        short[] shortArray = {1,2,3,4,5,6,7,8,9};
        //convert array of primitives to array of objects
        List<Short> objectArray = Shorts.asList(shortArray);
        System.out.println(objectArray.toString());

        //convert array of objects to array of primitives
        shortArray = Shorts.toArray(objectArray);
        VisualAssist.print("short arrays", shortArray);
        short data = 5;
        //check if element is present in the list of primitives or not
        System.out.println("5 is in list? " + Shorts.contains(shortArray, data));
        //Returns the minimum
        System.out.println("Min: " + Shorts.min(shortArray));
        //Returns the maximum
        System.out.println("Max: " + Shorts.max(shortArray));
        data = 2400;

        //get the byte array from an integer
        byte[] byteArray = Shorts.toByteArray(data);
        VisualAssist.print("2400 byteArray", byteArray);
    }

    public static void ints(){
        int[] intArray = {1,2,3,4,5,6,7,8,9};
        //convert array of primitives to array of objects
        List<Integer> objectArray = Ints.asList(intArray);
        System.out.println(objectArray.toString());
        //convert array of objects to array of primitives
        intArray = Ints.toArray(objectArray);
        VisualAssist.print("ints " , intArray);
        //check if element is present in the list of primitives or not
        System.out.println("5 is in list? " + Ints.contains(intArray, 5));
        //Returns the minimum
        System.out.println("Min: " + Ints.min(intArray));
        //Returns the maximum
        System.out.println("Max: " + Ints.max(intArray));

        //get the byte array from an integer
        byte[] byteArray = Ints.toByteArray(20000);
        VisualAssist.print(byteArray);
    }

    public static void longs(){
        long[] longArray = {1,2,3,4,5,6,7,8,9};
        //convert array of primitives to array of objects
        List<Long> objectArray = Longs.asList(longArray);
        System.out.println(objectArray.toString());

        //convert array of objects to array of primitives
        longArray = Longs.toArray(objectArray);
        VisualAssist.print("longs ", longArray);

        //check if element is present in the list of primitives or not
        System.out.println("5 is in list? "+ Longs.contains(longArray, 5));
        //Returns the minimum
        System.out.println("Min: " + Longs.min(longArray));
        //Returns the maximum
        System.out.println("Max: " + Longs.max(longArray));
    }

    public static void floats(){
        float[] floatArray = {1.0f,2.0f,3.0f,4.0f,5.0f,6.0f,7.0f,8.0f,9.0f};
        //convert array of primitives to array of objects
        List<Float> objectArray = Floats.asList(floatArray);
        System.out.println(objectArray.toString());

        //convert array of objects to array of primitives
        floatArray = Floats.toArray(objectArray);
        VisualAssist.print("floats ", floatArray);
        //check if element is present in the list of primitives or not
        System.out.println("5.0 is in list? " + Floats.contains(floatArray, 5.0f));
        //return the index of element
        System.out.println("5.0 position in list " + Floats.indexOf(floatArray, 5.0f));
        //Returns the minimum
        System.out.println("Min: " + Floats.min(floatArray));
        //Returns the maximum
        System.out.println("Max: " + Floats.max(floatArray));
    }

    public static void doubles(){
        double[] doubleArray = {1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0};
        //convert array of primitives to array of objects
        List<Double> objectArray = Doubles.asList(doubleArray);
        System.out.println(objectArray.toString());

        //convert array of objects to array of primitives
        doubleArray = Doubles.toArray(objectArray);
        VisualAssist.print("doubles ", doubleArray);

        //check if element is present in the list of primitives or not
        System.out.println("5.0 is in list? " + Doubles.contains(doubleArray, 5.0f));
        //return the index of element
        System.out.println("5.0 position in list " + Doubles.indexOf(doubleArray, 5.0f));
        //Returns the minimum
        System.out.println("Min: " + Doubles.min(doubleArray));
        //Returns the maximum
        System.out.println("Max: " + Doubles.max(doubleArray));
    }

    public static void chars(){
        char[] charArray = {'a','b','c','d','e','f','g','h'};
        //convert array of primitives to array of objects
        List<Character> objectArray = Chars.asList(charArray);
        System.out.println(objectArray.toString());

        //convert array of objects to array of primitives
        charArray = Chars.toArray(objectArray);
        VisualAssist.print("Chars ", charArray);

        //check if element is present in the list of primitives or not
        System.out.println("c is in list? " + Chars.contains(charArray, 'c'));
        //return the index of element
        System.out.println("c position in list " + Chars.indexOf(charArray, 'c'));
        //Returns the minimum
        System.out.println("Min: " + Chars.min(charArray));
        //Returns the maximum
        System.out.println("Max: " + Chars.max(charArray));
    }

    public static void booleans(){
        boolean[] booleanArray = {true,true,false,true,true,false,false};
        //convert array of primitives to array of objects
        List<Boolean> objectArray = Booleans.asList(booleanArray);
        System.out.println(objectArray.toString());

        //convert array of objects to array of primitives
        booleanArray = Booleans.toArray(objectArray);
        VisualAssist.print("Booleans ", booleanArray);

        //check if element is present in the list of primitives or not
        System.out.println("true is in list? " + Booleans.contains(booleanArray, true));
        //return the first index of element
        System.out.println("true position in list " + Booleans.indexOf(booleanArray, true));
        //Returns the count of true values
        System.out.println("true occured: " + Booleans.countTrue());

        //Returns the comparisons
        System.out.println("false Vs true: " + Booleans.compare(false, true));
        System.out.println("false Vs false: " + Booleans.compare(false, false));
        System.out.println("true Vs false: " + Booleans.compare(true, false));
        System.out.println("true Vs true: " + Booleans.compare(true, true));
    }
}
