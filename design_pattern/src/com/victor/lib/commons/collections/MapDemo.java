package com.victor.lib.commons.collections;

import org.apache.commons.collections4.BidiMap;
import org.apache.commons.collections4.IterableMap;
import org.apache.commons.collections4.MapIterator;
import org.apache.commons.collections4.MultiMap;
import org.apache.commons.collections4.OrderedMap;
import org.apache.commons.collections4.bidimap.TreeBidiMap;
import org.apache.commons.collections4.map.HashedMap;
import org.apache.commons.collections4.map.LinkedMap;
import org.apache.commons.collections4.map.MultiValueMap;

public class MapDemo {

	public static void mapIteration() {
		System.out.println("---------------mapIteration------------------");
		IterableMap<String,String> map = new HashedMap<>();
		map.put("foo", "bar");
		MapIterator<String,String> it = map.mapIterator();
		while (it.hasNext()) {
			String key = it.next();
			String value = it.getValue();	  
			it.setValue("a");
		}
		System.out.println(map.toString());
	}
	
	public static void orderedMap() {
		System.out.println("---------------orderedMap------------------");
		OrderedMap<String,String> map = new LinkedMap<>();
		map.put("FIVE", "5");
		map.put("SIX", "6");
		map.put("SEVEN", "7");
		System.out.println(map.firstKey());  					// returns "FIVE"
		System.out.println(map.nextKey("FIVE"));  				// returns "SIX"
		System.out.println(map.nextKey("SIX"));  				// returns "SEVEN"
	}
	
	public static void BidirectionalMaps() {
		System.out.println("---------------BidirectionalMaps------------------");
		BidiMap<String,String> bidi = new TreeBidiMap<>();
		bidi.put("SIX", "6");
		bidi.put("FIVE", "5");
		bidi.get("SIX");  										// returns "6"
		bidi.getKey("6");  										// returns "SIX"
		bidi.removeValue("6");  								// removes the mapping
		BidiMap inverse = bidi.inverseBidiMap();  				// returns a map with keys and values swapped
		System.out.println(bidi.toString());
		System.out.println(inverse.toString());
	}
	
	public static void multiMap() {
		System.out.println("---------------multiMap------------------");
		MultiMap<String,String> map=new MultiValueMap<>();
        map.put("key", "value1");
        map.put("key", "value2");
        map.put("key", "value2");
        System.out.println(map.get("key"));
	}
	
	public static void main(String[] args) {
		mapIteration();
		orderedMap();
		BidirectionalMaps();
		multiMap();
	}
}
