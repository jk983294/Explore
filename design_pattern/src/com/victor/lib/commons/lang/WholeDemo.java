package com.victor.lib.commons.lang;

import java.util.Date;

import org.apache.commons.lang3.ClassUtils;
import org.apache.commons.lang3.SystemUtils;
import org.apache.commons.lang3.time.DateFormatUtils;
import org.apache.commons.lang3.time.DateUtils;

public class WholeDemo {
	
	public static void main(String[] args) {
        System.out.println("get class name : " + ClassUtils.getShortClassName(WholeDemo.class)); 
        System.out.println("get package name : " + ClassUtils.getPackageName(WholeDemo.class)); 

        System.out.println("JavaHome : " + SystemUtils.getJavaHome()); 
        System.out.println("temp dir : " + SystemUtils.getJavaIoTmpDir()); 
         
         
        System.out.println("format date : " + DateFormatUtils.format(new Date(), "yyyy-MM-dd HH:mm:ss")); 
        System.out.println("add days : " + DateFormatUtils.format(DateUtils.addDays(new Date(), 7), "yyyy-MM-dd HH:mm:ss"));
         
	}
}
