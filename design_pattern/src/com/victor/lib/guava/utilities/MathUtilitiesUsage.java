package com.victor.lib.guava.utilities;

import com.google.common.math.BigIntegerMath;
import com.google.common.math.IntMath;
import com.google.common.math.LongMath;

import java.math.BigInteger;
import java.math.RoundingMode;


/**
 * MathUtilitiesUsage IntMath LongMath BigIntegerMath
 */
public class MathUtilitiesUsage {

    public static void main(String[] args) {
        intMath();
        longMath();
        bigIntegerMath();
    }

    public static void intMath(){
        System.out.println(IntMath.binomial(5, 2));

        try {
            // provided it does not overflow.
            System.out.println(IntMath.checkedAdd(Integer.MAX_VALUE, Integer.MAX_VALUE));
            System.out.println(IntMath.checkedMultiply(Integer.MAX_VALUE, Integer.MAX_VALUE));
            System.out.println(IntMath.checkedPow(Integer.MAX_VALUE, Integer.MAX_VALUE));
            System.out.println(IntMath.checkedSubtract(Integer.MAX_VALUE, Integer.MAX_VALUE));
        }catch(ArithmeticException e){
            System.out.println("Error: " + e.getMessage());
        }

        System.out.println(IntMath.divide(100, 5, RoundingMode.UNNECESSARY));
        try {
            //exception will be thrown as 100 is not completely divisible by 3
            // thus rounding is required, and RoundingMode is set as UNNECESSARY
            System.out.println(IntMath.divide(100, 3, RoundingMode.UNNECESSARY));
        }catch(ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        }

        System.out.println("Log2(2): " + IntMath.log2(2, RoundingMode.HALF_EVEN));

        System.out.println("Log10(10): " + IntMath.log10(10, RoundingMode.HALF_EVEN));

        System.out.println("sqrt(100): " + IntMath.sqrt(IntMath.pow(10,2), RoundingMode.HALF_EVEN));

        System.out.println("gcd(100,50): " + IntMath.gcd(100,50));

        System.out.println("modulus(100,50): " + IntMath.mod(100,50));

        System.out.println("factorial(5): " + IntMath.factorial(5));

        System.out.println("isPowerOfTwo(8): " + IntMath.isPowerOfTwo(8));
    }

    public static void longMath(){
        try{
            System.out.println(LongMath.checkedAdd(Long.MAX_VALUE, Long.MAX_VALUE));
        }catch(ArithmeticException e){
            System.out.println("Error: " + e.getMessage());
        }

        System.out.println(LongMath.divide(100, 5, RoundingMode.UNNECESSARY));
        try {
            //exception will be thrown as 100 is not completely divisible by 3
            // thus rounding is required, and RoundingMode is set as UNNESSARY
            System.out.println(LongMath.divide(100, 3, RoundingMode.UNNECESSARY));
        }catch(ArithmeticException e){
            System.out.println("Error: " + e.getMessage());
        }

        System.out.println("Log2(2): " + LongMath.log2(2, RoundingMode.HALF_EVEN));

        System.out.println("Log10(10): " + LongMath.log10(10, RoundingMode.HALF_EVEN));

        System.out.println("sqrt(100): " + LongMath.sqrt(LongMath.pow(10,2), RoundingMode.HALF_EVEN));

        System.out.println("gcd(100,50): " + LongMath.gcd(100,50));

        System.out.println("modulus(100,50): " + LongMath.mod(100,50));

        System.out.println("factorial(5): " + LongMath.factorial(5));

        System.out.println("isPowerOfTwo(8): " + LongMath.isPowerOfTwo(8));
    }

    public static void bigIntegerMath(){
        System.out.println(BigIntegerMath.divide(BigInteger.TEN, new BigInteger("2"), RoundingMode.UNNECESSARY));

        try{
            //exception will be thrown as 100 is not completely divisible by 3
            // thus rounding is required, and RoundingMode is set as UNNESSARY
            System.out.println(BigIntegerMath.divide(BigInteger.TEN, new BigInteger("3"), RoundingMode.UNNECESSARY));
        }
        catch(ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        }

        System.out.println("Log2(2): " + BigIntegerMath.log2(new BigInteger("2"), RoundingMode.HALF_EVEN));

        System.out.println("Log10(10): " + BigIntegerMath.log10(BigInteger.TEN, RoundingMode.HALF_EVEN));

        System.out.println("sqrt(100): " + BigIntegerMath.sqrt(BigInteger.TEN.multiply(BigInteger.TEN), RoundingMode.HALF_EVEN));

        System.out.println("factorial(5): "+BigIntegerMath.factorial(5));
    }
}
