package com.victor.lib.commonsmath;

import org.apache.commons.math3.analysis.polynomials.PolynomialFunction;
import org.apache.commons.math3.analysis.polynomials.PolynomialSplineFunction;

public class PolinomialsDemo {

	public static void main(String[] args) {
		polynomialsSpline();
		System.out.println("-----------------------------------------------");
		polynomials();
	}
	
	public static void polynomialsSpline() {
		//分段函数
		PolynomialFunction[] polynomials = {
				new PolynomialFunction(new double[] { 0d, 1d, 1d }),
				new PolynomialFunction(new double[] { 2d, 1d, 1d }),
				new PolynomialFunction(new double[] { 4d, 1d, 1d }) };
		double[] knots = { -1, 0, 1, 2 };
		PolynomialSplineFunction spline = new PolynomialSplineFunction(knots, polynomials);
		// output directly
		System.out.println("poly spline func is " + spline);
		// get the value when x = 0.5
		System.out.println("f(0.5) = " + spline.value(0.5));
		// the number of spline segments
		System.out.println("spline segments number is " + spline.getN());
		// the polynomials functions
		for (int i = 0; i < spline.getN(); i++) {
			System.out.println("spline:f" + i + "(x) = " + spline.getPolynomials()[i]);
		}
		// function derivative
		System.out.println("spline func derivative is " + spline.derivative());
	}

	private static void polynomials() {
		//f(x)=coeff[0] + coeff[1]x + coeff[2]x^2 + … + coeff[n]x^n
		double[] f1_coeff = { 3.0, 6.0, -2.0, 1.0 };
		double[] f2_coeff = { 1.0, 2.0, -1.0, -2.0 };
		PolynomialFunction f1 = new PolynomialFunction(f1_coeff);
		PolynomialFunction f2 = new PolynomialFunction(f2_coeff);
		// output directly
		System.out.println("f1(x) is : " + f1);
		System.out.println("f2(x) is : " + f2);
		// polynomial degree
		System.out.println("f1(x)'s degree is " + f1.degree());
		// get the value when x = 2
		System.out.println("f1(2) = " + f1.value(2));
		// function add
		System.out.println("f1(x)+f2(x) = " + f1.add(f2));
		// function substract
		System.out.println("f1(x)-f2(x) = " + f1.subtract(f2));
		// function multiply
		System.out.println("f1(x)*f2(x) = " + f1.multiply(f2));
		// function derivative
		System.out.println("f1'(x) = " + f1.derivative());
		System.out.println("f2''(x) = " + ((PolynomialFunction) f2.derivative()).derivative());

	}
}
