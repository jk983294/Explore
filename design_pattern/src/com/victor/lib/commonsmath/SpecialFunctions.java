package com.victor.lib.commonsmath;

import org.apache.commons.math3.special.Beta;
import org.apache.commons.math3.special.Gamma;

public class SpecialFunctions {

	public static void main(String[] args) {
		/**
		 * Γ(x)
		 */
		System.out.println(Gamma.gamma(0.5));
		
		/**
		 * log Γ(x) 
		 */
		System.out.println(Gamma.logGamma(0.5));
		
		System.out.println(Gamma.regularizedGammaP(0.5, 0.5));
		
		System.out.println(Beta.logBeta(0.5, 0.5));
		System.out.println(Beta.regularizedBeta(0.5, 0.5, 0.5));
	}
}
