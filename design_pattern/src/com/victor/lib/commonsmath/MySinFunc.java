package com.victor.lib.commonsmath;

import org.apache.commons.math3.analysis.DifferentiableUnivariateFunction;
import org.apache.commons.math3.analysis.UnivariateFunction;

public class MySinFunc  implements DifferentiableUnivariateFunction{
	
	public double value(double x) {
		return Math.sin(x);
	}

	@Override
	public UnivariateFunction derivative() {
		return new DifferentiableUnivariateFunction() {
			public double value(double x) {
				return Math.cos(x);
			}

			@Override
			public UnivariateFunction derivative() {
				return new MySinFunc();
			}
		};
	}

}
