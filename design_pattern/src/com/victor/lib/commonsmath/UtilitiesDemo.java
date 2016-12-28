package com.victor.lib.commonsmath;

import java.util.Iterator;

import org.apache.commons.math3.util.ArithmeticUtils;
import org.apache.commons.math3.util.Combinations;
import org.apache.commons.math3.util.CombinatoricsUtils;
import org.apache.commons.math3.util.DoubleArray;
import org.apache.commons.math3.util.FastMath;
import org.apache.commons.math3.util.MathArrays;
import org.apache.commons.math3.util.MathUtils;
import org.apache.commons.math3.util.OpenIntToDoubleHashMap;
import org.apache.commons.math3.util.ResizableDoubleArray;

import com.victor.utilities.visual.VisualAssist;

public class UtilitiesDemo {

	/**
	 * high performance rolling window array
	 */
	public static void DoubleArrayUtilities() {
		System.out.println("---------------------Double Array---------------------------");
		DoubleArray da = new ResizableDoubleArray();
		for (int i = 0; i < 5; i++) {
            da.addElement(i);
        }
		da.addElementRolling(2.0);
		VisualAssist.print("DoubleArray : ", da.getElements());
	}
	
	/**
	 * high performance number hash map for int to double, uses open addressing and primitive arrays
	 */
	public static void numberHashMap() {
		System.out.println("---------------------Open Int To Double HashMap---------------------------");
		OpenIntToDoubleHashMap map = new OpenIntToDoubleHashMap();
		for (int i = 0; i < 5; i++) {
			map.put(i, i * 1.0 );
		}
		System.out.println(map.get(2));
		System.out.println(map.containsKey(2));
		OpenIntToDoubleHashMap.Iterator iterator = map.iterator();
        for (int i = 0; i < map.size(); ++i) {
            iterator.advance();
            System.out.println(iterator.key() + " : " + iterator.value());
        }
	}
	
	@SuppressWarnings("deprecation")
	public static void ArithmeticUtils() {
		System.out.println("---------------------ArithmeticUtils---------------------------");
        System.out.println("greatest common divisor : " + ArithmeticUtils.gcd(30, 50));	
        System.out.println("least common multiple : " + ArithmeticUtils.lcm(30, 50));
        System.out.println("21 pow 7 : " + ArithmeticUtils.pow(21, 7));
        System.out.println("Binomial coefficients 5 choose 2 : " + CombinatoricsUtils.binomialCoefficient(5, 2));
        System.out.println("Stirling 5 and 2 : " + CombinatoricsUtils.stirlingS2(5, 2)); 
        System.out.println("Factorials 5! : " + CombinatoricsUtils.factorial(5));
	}
	
	/**
	 * FastMath speed is achieved by relying heavily on optimizing compilers to native code present  
	 * and use of large Precomputed literal arrays tables. first load may slow, but only once
	 */
	public static void fastMath() {
		System.out.println("---------------------fastMath---------------------------");
		System.out.println(FastMath.E);	
		System.out.println(FastMath.PI);
		System.out.println(FastMath.expm1(1.0));		// exp(1) -1	
	}
	
	public static void combinations() {
		System.out.println("---------------------combinations---------------------------");
		Combinations c = new Combinations(3,2);
		for (int[] iterate : c) {
			VisualAssist.print( iterate);
		}
		System.out.println("---------------------combinations another iter---------------------------");
		Iterator<int[]> iter= c.iterator();
		while (iter.hasNext()) {
			int[] is = (int[]) iter.next();
			VisualAssist.print( is);
		}
	}
	
	public static void mathArray() {
		System.out.println("---------------------mathArray---------------------------");
		double[] a = new double[]{ 1.0, 2.0, 3.0 };
		VisualAssist.print(MathArrays.copyOf(a));
		VisualAssist.print(MathArrays.normalizeArray(a, 1));
		VisualAssist.print(MathArrays.natural(5));
		int[] b = MathArrays.natural(5);
		MathArrays.shuffle(b);
		VisualAssist.print(b);
		VisualAssist.print(MathArrays.linearCombination(1, 2, 3, 4));	// ax + by
		VisualAssist.print("norm2 " , MathArrays.safeNorm(a));
		
		System.out.println("---------------------MathUtils---------------------------");
		VisualAssist.print( MathUtils.equals(1e-6, 1e-7));
		VisualAssist.print( MathUtils.reduce(5.0, 3.0, 1.0) );
	}
	
	public static void main(String[] args) {
		DoubleArrayUtilities();
		numberHashMap();
		ArithmeticUtils();
		fastMath();
		combinations();
		mathArray();
	}
}
