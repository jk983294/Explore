package com.victor.lib.commonsmath;

import org.apache.commons.math3.analysis.UnivariateFunction;
import org.apache.commons.math3.analysis.interpolation.HermiteInterpolator;
import org.apache.commons.math3.analysis.interpolation.SplineInterpolator;
import org.apache.commons.math3.analysis.interpolation.UnivariateInterpolator;
import org.apache.commons.math3.analysis.solvers.AllowedSolution;
import org.apache.commons.math3.analysis.solvers.BracketingNthOrderBrentSolver;
import org.apache.commons.math3.analysis.solvers.BrentSolver;
import org.apache.commons.math3.analysis.solvers.PegasusSolver;
import org.apache.commons.math3.analysis.solvers.UnivariateSolver;
import org.apache.commons.math3.analysis.solvers.UnivariateSolverUtils;

public class NumericalAnalysis {

	/**
	 * UnivariateSolver							univariate real-valued functions
	 * UnivariateDifferentiableSolver			differentiable univariate real-valued functions
	 * PolynomialSolver 						polynomial functions
	 * 
	 * f(c) = 0.0  and min <= c <= max
	 */
	public static void rootFind() {
		class myfunc implements UnivariateFunction {
			@Override
			public double value(double x) {
				return x * x -9;
			}	
		}
		UnivariateFunction function = new myfunc();
		final double relativeAccuracy = 1.0e-12;
		final double absoluteAccuracy = 1.0e-8;
		final int    maxOrder         = 5;
		UnivariateSolver solver   = new BracketingNthOrderBrentSolver(relativeAccuracy, absoluteAccuracy, maxOrder);
		double c = solver.solve(100, function, 0.0, 5.0);
		System.out.println("solution : " + c);
		
		
		UnivariateSolver nonBracketing = new BrentSolver(relativeAccuracy, absoluteAccuracy);
		double baseRoot = nonBracketing.solve(100, function, 1.0, 5.0);
		double c1 = UnivariateSolverUtils.forceSide(100, function,
		                                           new PegasusSolver(relativeAccuracy, absoluteAccuracy),
		                                           baseRoot, -5.0, 5.0, AllowedSolution.LEFT_SIDE);
		System.out.println("solution : " + c1);
	}
	
	/**
	 * UnivariateInterpolator is used to find a univariate real-valued function f 
	 * which for a given set of ordered pairs (xi,yi) yields f(xi)=yi to the best accuracy possible.
	 * interpolating polynomials is a perfect approximation of a function at interpolation points
	 */
	public static void interpolation() {
		double x[] = { 0.0, 1.0, 2.0 };
		double y[] = { 1.0, -1.0, 2.0 };
		UnivariateInterpolator interpolator1 = new SplineInterpolator();		// polynomials of degree 3 
		UnivariateFunction function = interpolator1.interpolate(x, y);
		double interpolationX = 0.5;
		double interpolatedY = function.value(interpolationX);
		System.out.println("f(" + interpolationX + ") = " + interpolatedY);
		
		
		HermiteInterpolator interpolator = new HermiteInterpolator();
		// at x = 0, we provide both value and first derivative
		interpolator.addSamplePoint(0.0, new double[] { 1.0 }, new double[] { 2.0 });
		// at x = 1, we provide only function value
		interpolator.addSamplePoint(1.0, new double[] { 4.0 });
		// at x = 2, we provide both value and first derivative
		interpolator.addSamplePoint(2.0, new double[] { 5.0 }, new double[] { 2.0 });
		// should print "value at x = 0.5: 2.5625"
		System.out.println("value at x = 0.5: " + interpolator.value(0.5)[0]);
		// should print "interpolation polynomial: 1 + 2 x + 4 x^2 - 4 x^3 + x^4"
		System.out.println("interpolation polynomial: " + interpolator.getPolynomials()[0]);
		
		/**
		 * high degree interpolate
		 * BivariateGridInterpolator
		 * bicubic interpolation
		 * TrivariateGridInterpolator 
		 * tricubic interpolation
		 */
	}
	
	public static void integrate() {
		
	}
	
	public static void differentiate() {
		
	}
	
	public static void main(String[] args) {
		rootFind();
		interpolation();
	}
}
