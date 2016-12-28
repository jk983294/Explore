package com.victor.lib.commonsmath;

import org.apache.commons.math3.distribution.NormalDistribution;
import org.apache.commons.math3.distribution.PoissonDistribution;

public class DistributionTest {
	public static void main(String[] args) {
		test();
		System.out.println("-----------------------------------------------");
		poisson();
		System.out.println("-----------------------------------------------");
		normal();
	}
	
	private static void test() {
		NormalDistribution normal = new NormalDistribution(600, 3);
		System.out.println("P(X<590) = " + normal.cumulativeProbability(590));
		System.out.println("P(X>605) = "
				+ (1 - normal.cumulativeProbability(605)));
	}

	private static void poisson() {
		PoissonDistribution dist = new PoissonDistribution(4.0);
		System.out.println("P(X<=2.0) = " + dist.cumulativeProbability(2));
		System.out.println("mean value is " + dist.getMean());
		System.out.println("P(X=1.0) = " + dist.probability(1));
		System.out.println("P(X=x)=0.8 where x = "
				+ dist.inverseCumulativeProbability(0.8));
	}

	private static void normal() {
		NormalDistribution normal = new NormalDistribution(0, 1);
		System.out.println("P(X<2.0) = "+ normal.cumulativeProbability(2.0));
		System.out.println("mean value is " + normal.getMean());
		System.out.println("standard deviation is "+ normal.getStandardDeviation());
		System.out.println("P(X=1) = " + normal.density(1.0));
		System.out.println("P(X<x)=0.8 where x = "+ normal.inverseCumulativeProbability(0.8));
	}
}
