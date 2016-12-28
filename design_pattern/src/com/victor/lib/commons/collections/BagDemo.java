package com.victor.lib.commons.collections;

import java.util.Iterator;

import org.apache.commons.collections4.Bag;
import org.apache.commons.collections4.bag.HashBag;
import org.apache.commons.collections4.bag.TreeBag;

/**
 * contain many equal things, count them 
 */
public class BagDemo {

	public static void hashBag() {
		System.out.println("---------------hashBag------------------");
		Bag<String> bag1=new HashBag<>();
        bag1.add("book1",10);		// add ten book1
        bag1.add("book2",20);
       
        Bag<String> bag2=new HashBag<>();
        bag2.add("book2",5);
        bag2.add("book3",10);
       
        bag1.add("book1");
        bag1.remove("book1",2);   //remove 2 book1
        bag1.removeAll(bag2);
       
        System.out.println("book1: "+bag1.getCount("book1"));
        System.out.println("book2: "+bag1.getCount("book2")+"\n");

        bag1.retainAll(bag2);		// bag1 intersection  with bag2
        System.out.println("book1: "+bag1.getCount("book1"));
        System.out.println("book2: "+bag1.getCount("book2"));
        System.out.println("book3: "+bag1.getCount("book3"));
	}
	
	/**
	 * tree bag maintain its sequence that put into bag
	 */
	public static void treeBag() {
		System.out.println("---------------treeBag------------------");
		Bag<String> bag1=new TreeBag<>();
        bag1.add("book1",2);
        bag1.add("book2",1);
        bag1.add("book3",2);
        bag1.add("book4",1);
        bag1.add("book5",1);
       
        Iterator<String> iterator=bag1.iterator();
        while(iterator.hasNext()){
            System.out.println(iterator.next());
        }
	}
	
	public static void main(String[] args) {
		hashBag();
		treeBag();
	}
}
