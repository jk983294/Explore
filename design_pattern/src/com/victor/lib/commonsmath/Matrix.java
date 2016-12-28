package com.victor.lib.commonsmath;

import org.apache.commons.math3.linear.*;

public class Matrix {

	

	private static void matrixDecomposite() {
		double[][] testData = { { 1.0, 2.0, 3.0 }, { 2.0, 5.0, 3.0 },
				{ 1.0, 0.0, 8.0 } };

		RealMatrix matrix = MatrixUtils.createRealMatrix(testData);
		// LUP decomposition
		LUDecomposition LU = new LUDecomposition(matrix);
		RealMatrix l = LU.getL();
		RealMatrix u = LU.getU();
		RealMatrix p = LU.getP();
		System.out.println("L is : " + l);
		System.out.println("U is : " + u);
		System.out.println("P is : " + p);
		System.out.println("PA is " + (p.multiply(matrix)));
		System.out.println("LU is " + (l.multiply(u)));
		System.out.println("PA = LU is "
				+ p.multiply(matrix).equals(l.multiply(u)));
		// matrix singular
		System.out.println("LU is not singular : "
				+ LU.getSolver().isNonSingular());
		// matrix determinant
		System.out.println("matrix determinant is : " + LU.getDeterminant());
		// matrix solver
		RealMatrix b = MatrixUtils.createRealMatrix(new double[][] { { 1, 0 },
				{ 2, -5 }, { 3, 1 } });
		DecompositionSolver solver = LU.getSolver();
		System.out.println("solve Ax = b (when b is matrix) is x = " + solver.solve(b));
		System.out.println("solve Ax = b (when b is vector) is x = "
				+ new ArrayRealVector(solver.solve(new ArrayRealVector(b.getColumn(0)))));
		// matrix inverse
		System.out.println("matrix inverse is " + solver.getInverse());
	}

	public static void matrix() {
		double[][] data1 = { { 1d, 2d, 3d }, { 2d, 5d, 3d }, { 1d, 0d, 8d } };
		double[][] t_data = { { -40d, 16d, 9d }, { 13d, -5d, -3d },
				{ 5d, -2d, -1d } };
		Array2DRowRealMatrix matrix1 = new Array2DRowRealMatrix(data1);
		Array2DRowRealMatrix t_mat = new Array2DRowRealMatrix(t_data);
		// is square
		System.out.println("it is square matrix! : " + matrix1.isSquare());
		// dimension of row and column
		System.out.println("row dimension is " + matrix1.getRowDimension());
		System.out.println("column dimension is "
				+ matrix1.getColumnDimension());
		// matrix add
		System.out.println("mat1 + mat1 = " + matrix1.add(matrix1));
		System.out.println("mat1 + 5 = " + matrix1.scalarAdd(5.0));
		// matrix sub
		System.out.println("mat1 - mat1 = " + matrix1.subtract(matrix1));
		// matrix norm
		System.out.println("the maximum absolute row sum norm is "
				+ matrix1.getNorm());
		// matrix multiply
		System.out.println("mat1 * t_mat = " + matrix1.multiply(t_mat));
		System.out.println("mat1 * 5.0 = " + matrix1.scalarMultiply(5));
		System.out.println("t_mat * mat1 = " + matrix1.preMultiply(t_mat));
		// matrix trace
		System.out.println("the trace is " + matrix1.getTrace());
		// matrix transpose
		System.out.println("the transpose of mat1 is " + matrix1.transpose());
		// matrix to vector
		System.out
				.println("the first row vector is " + matrix1.getRowVector(0));
		// matrix get sub matrix of selected rows and columns
		System.out.println("sub matrix of mat1 is "
				+ matrix1.getSubMatrix(new int[] { 0, 2 }, new int[] { 1, 2 }));
	}
	
	/**
	 * Matrix addition, subtraction, multiplication
	 * Scalar addition and multiplication
	 * transpose
	 * Norm and Trace
	 * Operation on a vector
	 */
	public static void matrix1() {
		// Create a real matrix with two rows and three columns, using a factory
		// method that selects the implementation class for us.
		double[][] matrixData = { {1d,2d,3d}, {2d,5d,3d}};
		RealMatrix m = MatrixUtils.createRealMatrix(matrixData);

		// One more with three rows, two columns, this time instantiating the
		// RealMatrix implementation class directly.
		double[][] matrixData2 = { {1d,2d}, {2d,5d}, {1d, 7d}};
		RealMatrix n = new Array2DRowRealMatrix(matrixData2);

		// Note: The constructor copies  the input double[][] array in both cases.

		// Now multiply m by n
		RealMatrix p = m.multiply(n);
		System.out.println(p.getRowDimension());    // 2
		System.out.println(p.getColumnDimension()); // 2

		// Invert p, using LU decomposition
		RealMatrix pInverse = new LUDecomposition(p).getSolver().getInverse();
	}
	
	private static void vector() {
		double[] vec1 = { 1d, 2d, 3d };
		double[] vec2 = { 4d, 5d, 6d };
		ArrayRealVector v1 = new ArrayRealVector(vec1);
		ArrayRealVector v2 = new ArrayRealVector(vec2);		
		System.out.println("size is " + v1.getDimension());			// dimension : size of vector		
		System.out.println("v1 + v2 = " + v1.add(v2));				// vector add	
		System.out.println("v1 - v2 = " + v1.subtract(v2));			// vector substract
		System.out.println("v1 * v2 = " + v1.ebeMultiply(v2));	// vector element by element multiply		
		System.out.println("v1 / v2 = " + v1.ebeDivide(v2));		// vector element by element divide
		System.out.println("v1[1] = " + v1.getEntry(1));				// get index at 1								
		System.out.println("v1 append v2 is " + v1.append(v2));// vector append
		
		// vector distance
		System.out.println("distance between v1 and v2 is "+ v1.getDistance(v2));		//Euclidean distance
		System.out.println("L1 distance between v1 and v2 is "+ v1.cosine(v2));			//cosine similarity distance
		System.out.println("L1 distance between v1 and v2 is "+ v1.getL1Distance(v2));
		
		System.out.println("norm of v1 is " + v1.getNorm());			// vector norm	
		System.out.println("dot product of v1 and v2 is " + v1.dotProduct(v2));		// vector dot product, it's a projection
		System.out.println("outer product of v1 and v2 is "+ v1.outerProduct(v2));	// vector outer product
		System.out.println("hogonal projection of v1 and v2 is "+ v1.projection(v2));		// vector orthogonal projection
		// vector map operations
//		System.out.println("Map the Math.abs(double) function to v1 is "+ v1.mapAbs());
//		v1.mapInvToSelf();
		System.out.println("Map the 1/x function to v1 itself is " + v1);
		// vector get sub vector
		System.out.println("sub vector of v1 is " + v1.getSubVector(0, 2));
	}
	
	public static void main(String[] args) {
		//ArrayRealVector and ArrayFieldVector ( generic ) implements RealVector interface
		vector();
		System.out.println("\n\n\n");
		matrix();
		System.out.println("\n\n\n");
		matrix1();
		System.out.println("\n\n\n");
		matrixDecomposite();
	}
}
