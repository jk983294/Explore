package com.victor.lib.commons.lang;

import org.apache.commons.lang3.StringEscapeUtils;
import org.apache.commons.lang3.StringUtils;

public class StringUtilsDemo {

	public static void main(String[] args) {
		String[] test = { "33", "ddffd" };
		System.out.println("judge the string is blank : "+StringUtils.isBlank("   "));  
        System.out.println("concatenate with semicolon : "+ StringUtils.join(test, ", "));
        System.out.println("padding in right so that the total length is six : "+ StringUtils.rightPad("abc", 6, 'T')); 
        System.out.println("capitalize first character : "+ StringUtils.capitalize("abc"));  
        System.out.println("Deletes all whitespaces from a String : "+ StringUtils.deleteWhitespace("   ab  c  ")); 
        System.out.println("judge if string contain substring : "+ StringUtils.contains("abc", "ab")); 
        System.out.println("get left 2 chars : "+ StringUtils.left("abc", 2)); 
        System.out.println("get right 3 chars : "+ StringUtils.right("abcd", 3)); 
        
		// data setup
		String str1 = "";
		String str2 = " ";
		String str3 = "/t";
		String str4 = null;
		String str5 = "123";
		String str6 = "ABCDEFG";
		String str7 = "It feels good to use Jakarta Commons./r/n";

		// check for empty strings
		System.out.println("==============================");
		System.out.println("Is str1 blank? " + StringUtils.isBlank(str1));
		System.out.println("Is str2 blank? " + StringUtils.isBlank(str2));
		System.out.println("Is str3 blank? " + StringUtils.isBlank(str3));
		System.out.println("Is str4 blank? " + StringUtils.isBlank(str4));

		// check for numerics
		System.out.println("==============================");
		System.out.println("Is str5 numeric? " + StringUtils.isNumeric(str5));
		System.out.println("Is str6 numeric? " + StringUtils.isNumeric(str6));
		
		// reverse strings / whole words
		System.out.println("==============================");
		System.out.println("str6: " + str6);
		System.out.println("str6 reversed: " + StringUtils.reverse(str6));
		System.out.println("str7: " + str7);
		String str8 = StringUtils.chomp(str7);
		str8 = StringUtils.reverseDelimited(str8, ' ');
		System.out.println("str7 reversed whole words : /r/n" + str8);

		// build header (useful to print log messages that are easy to locate)
		System.out.println("==============================");
		System.out.println("print header:");
		String padding = StringUtils.repeat("=", 50);
		String msg = StringUtils.center(" Customised Header ", 50, "%");
		Object[] raw = new Object[] { padding, msg, padding };
		String header = StringUtils.join(raw, "/r/n");
		System.out.println(header);
		
		
		// 7.StringEscapeUtils 
        System.out.println(StringEscapeUtils.escapeHtml3("</html>")); 	// result is : &lt;html&gt;         
        System.out.println(StringEscapeUtils.escapeJava("String"));
        System.out.println(StringEscapeUtils.escapeJava("中国"));
        System.out.println(StringEscapeUtils.unescapeHtml4("&lt;a&gt;dddd&lt;/a&gt;")); 
        System.out.println(StringEscapeUtils.escapeEcmaScript("<script>alert('1111')</script>"));   //&lt;script&gt;alert('111')&lt;/script&gt;
	}
}
