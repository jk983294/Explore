package com.victor.lib.commonsmath;

import org.apache.commons.math3.random.CorrelatedRandomVectorGenerator;
import org.apache.commons.math3.random.GaussianRandomGenerator;
import org.apache.commons.math3.random.JDKRandomGenerator;
import org.apache.commons.math3.random.RandomDataGenerator;
import org.apache.commons.math3.random.RandomGenerator;

public class DataGeneration {

	
	public static void randomNumber() {
		RandomDataGenerator randomData = new RandomDataGenerator(); 
		for (int i = 0; i < 10; i++) {
			System.out.println(randomData.nextLong(1, 1000000));
		}
	}
	
	public static void randomVector() {
		// Create and seed a RandomGenerator (could use any of the generators in the random package here)
		RandomGenerator rg = new JDKRandomGenerator();
		rg.setSeed(17399225432l);  // Fixed seed means same results every time

		// Create a GassianRandomGenerator using rg as its source of randomness
		GaussianRandomGenerator rawGenerator = new GaussianRandomGenerator(rg);

		double mean = 0.0;
		double covariance = 1.0;
		
		// Create a CorrelatedRandomVectorGenerator using rawGenerator for the components
//		CorrelatedRandomVectorGenerator generator = new CorrelatedRandomVectorGenerator(mean, covariance, 1.0e-12 * covariance.getNorm(), rawGenerator);

		// Use the generator to generate correlated vectors
//		double[] randomVector = generator.nextVector();
	}
	
	public static void main(String[] args) {
		randomNumber();
	}
}
