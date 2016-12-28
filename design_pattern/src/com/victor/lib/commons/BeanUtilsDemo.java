package com.victor.lib.commons;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.beanutils.BeanUtils;
import org.apache.commons.beanutils.ConstructorUtils;
import org.apache.commons.beanutils.MethodUtils;
import org.apache.commons.beanutils.PropertyUtils;

public class BeanUtilsDemo {
	
	public static void main(String[] args) throws Exception {
		MyObject myObject = new MyObject("jk", 12);
		
		Map<String, String> values = new HashMap<>();
		values.put("1","234-222-1222211");
		values.put("2","021-086-1232323");
		
		List<String> list = new ArrayList<>();
		list.add("foo");
		list.add("bar");
		
		PropertyUtils.setProperty(myObject,"values",values);
		BeanUtils.setProperty(myObject,"list",list);
		System.out.println(BeanUtils.getProperty(myObject, "a"));
		System.out.println(BeanUtils.getProperty(myObject, "values(2)"));			//values.get("2")
		System.out.println(BeanUtils.getMappedProperty(myObject, "values", "2"));	//values.get("2")
		System.out.println(BeanUtils.getProperty(myObject, "list[1]"));
		
		MyObject myObject2 = new MyObject();
	    BeanUtils.copyProperties(myObject2, myObject);								//shallow copy
	    System.out.println(myObject2.toString());
	    
	    /**
	     * dynamic all function
	     */
	    MethodUtils.invokeMethod(myObject2, "print", "asdf");
	    
	    
	    /**
	     * Dynamic construct object
	     */
	    Object[] ctorArgs = new Object[2];
	    ctorArgs[0] = "aha";
	    ctorArgs[1] = 1024;
	    MyObject ahaObject = ConstructorUtils.invokeConstructor(MyObject.class, ctorArgs);
	    System.out.println(ahaObject.toString());
	}
}

