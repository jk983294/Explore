package com.victor.lib.commons.lang;

import org.apache.commons.lang3.RandomStringUtils;
import org.apache.commons.lang3.RandomUtils;
import org.apache.commons.lang3.math.NumberUtils;

public class NumberUtilsDemo {
	
	public static void main(String[] args) {
		String str = "12.7";  
		
        NumberUtils.isDigits(str);  
        NumberUtils.isNumber(str);  
  
        System.out.println(NumberUtils.max(10, 20, 30)); 
        System.out.println(NumberUtils.min(10, 20, 30));  
  
        // cast string to number, support float, long, short
        System.out.println(NumberUtils.toInt(str));  
  
        // cast string to BigDecimal, support float, long, short 
        NumberUtils.createBigDecimal(str);  

        /* 
         * range random number generate
         */  
        RandomUtils.nextDouble(0,1);  
        RandomUtils.nextLong(0,10);  
        RandomUtils.nextInt(0,1000);  
        System.out.println("generate alpha and number mixed random : " + RandomStringUtils.randomAlphanumeric(15)); 
	}
}
