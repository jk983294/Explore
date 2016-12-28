package com.victor.lib.commons.collections;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.collections4.MapUtils;
import org.apache.commons.collections4.SetUtils;
import org.apache.commons.lang3.ArrayUtils;

public class UtilsDemo {

	public static void setUtils() {
		System.out.println("-------------------setUtils-------------------------");
		SetUtils.emptySet();
		// SetUtils.transformedSet(set, transformer); //transform elements in
		// set
		// SetUtils.predicatedSet(set, predicate); //filter set using predicate
	}

	public static void mapUtils() {
		System.out.println("-------------------mapUtils-------------------------");
		Map<String, String> map = new HashMap<>();
		map.put("foo", "bar");
		MapUtils.verbosePrint(System.out, null, map);
	}

	public static void collectionUtils() {
		System.out.println("-------------------collectionUtils-------------------------");
		// CollectionUtils.
		String[] arrayA = new String[] { "1", "2", "3", "3", "4", "5" };
		String[] arrayB = new String[] { "3", "4", "4", "5", "6", "7" };

		List<String> a = Arrays.asList(arrayA);
		List<String> b = Arrays.asList(arrayB);

		Collection<String> union = CollectionUtils.union(a, b);
		Collection<String> intersection = CollectionUtils.intersection(a, b);
		Collection<String> disjunction = CollectionUtils.disjunction(a, b);
		Collection<String> subtract = CollectionUtils.subtract(a, b);

		Collections.sort((List<String>) union);
		Collections.sort((List<String>) intersection);
		Collections.sort((List<String>) disjunction);
		Collections.sort((List<String>) subtract);

		System.out.println("A: " + ArrayUtils.toString(a.toArray()));
		System.out.println("B: " + ArrayUtils.toString(b.toArray()));
		
		System.out.println("Union(A, B): " + ArrayUtils.toString(union.toArray()));
		System.out.println("Intersection(A, B): " + ArrayUtils.toString(intersection.toArray()));
		System.out.println("Disjunction(A, B): " + ArrayUtils.toString(disjunction.toArray()));
		System.out.println("Subtract(A, B): " + ArrayUtils.toString(subtract.toArray()));
		
		CollectionUtils.isEmpty(new ArrayList<Integer>());	// true
	}

	public static void main(String[] args) {
		setUtils();
		mapUtils();
		collectionUtils();
	}
}
