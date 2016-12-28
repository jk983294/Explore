package com.victor.lib.commonsmath;

import org.apache.commons.math3.linear.Array2DRowRealMatrix;
import org.apache.commons.math3.linear.ArrayRealVector;
import org.apache.commons.math3.linear.DecompositionSolver;
import org.apache.commons.math3.linear.LUDecomposition;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.linear.RealVector;


public class SolvingLinearSystem {

	/**
	 * 2x + 3y - 2z = 1 
	 * -x + 7y + 6x = -2 
	 * 4x - 3y - 5z = 1 
	 * AX = b
	 * first the coefficient matrix is decomposed in some way 
	 * and then a solver built from the decomposition solves the system
	 * @param args
	 */
	public static void main(String[] args) {
		/**
		 * Name				coefficients matrix					problem type
		 * LU					square						exact solution only
		 * Cholesky			symmetric positive definite		exact solution only
		 * QR					any							least squares solution
		 * eigen decomposition	square						exact solution only
		 * SVD					any							least squares solution
		 * algorithms suited for least squares problems can also be used to solve exact problems
		 */
		RealMatrix coefficients = new Array2DRowRealMatrix(new double[][] {
				{ 2, 3, -2 }, { -1, 7, 6 }, { 4, -3, -5 } }, false);
		DecompositionSolver solver = new LUDecomposition(coefficients).getSolver();
		RealVector constants = new ArrayRealVector(new double[] { 1, -2, 1 }, false);
		RealVector solution = solver.solve(constants);
		System.out.println(solution);
	}
}
