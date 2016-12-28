package com.victor.lib.commonsmath;

import java.util.ArrayList;

import org.apache.commons.math3.analysis.MultivariateFunction;
import org.apache.commons.math3.analysis.UnivariateFunction;
import org.apache.commons.math3.optim.InitialGuess;
import org.apache.commons.math3.optim.MaxEval;
import org.apache.commons.math3.optim.PointValuePair;
import org.apache.commons.math3.optim.linear.LinearConstraint;
import org.apache.commons.math3.optim.linear.LinearConstraintSet;
import org.apache.commons.math3.optim.linear.LinearObjectiveFunction;
import org.apache.commons.math3.optim.linear.NonNegativeConstraint;
import org.apache.commons.math3.optim.linear.PivotSelectionRule;
import org.apache.commons.math3.optim.linear.Relationship;
import org.apache.commons.math3.optim.linear.SimplexSolver;
import org.apache.commons.math3.optim.nonlinear.scalar.GoalType;
import org.apache.commons.math3.optim.nonlinear.scalar.MultivariateFunctionMappingAdapter;
import org.apache.commons.math3.optim.nonlinear.scalar.ObjectiveFunction;
import org.apache.commons.math3.optim.nonlinear.scalar.noderiv.AbstractSimplex;
import org.apache.commons.math3.optim.nonlinear.scalar.noderiv.NelderMeadSimplex;
import org.apache.commons.math3.optim.nonlinear.scalar.noderiv.SimplexOptimizer;
import org.apache.commons.math3.optim.univariate.BrentOptimizer;
import org.apache.commons.math3.optim.univariate.SearchInterval;
import org.apache.commons.math3.optim.univariate.UnivariateObjectiveFunction;
import org.apache.commons.math3.optim.univariate.UnivariateOptimizer;
import org.apache.commons.math3.optim.univariate.UnivariatePointValuePair;

import com.victor.utilities.visual.VisualAssist;
import org.junit.Assert;

public class OptimizationDemo {
	
	public static void main(String[] args) {
		UnivariateOptimizerDemo();
		linearProgramming();
        directSearch();
	}
	
	public static void UnivariateOptimizerDemo() {
		final UnivariateFunction f = new UnivariateFunction() {
            public double value(double x) {
                return x * x + 4 * x + 3;
            }
        };
	    UnivariateOptimizer optimizer = new BrentOptimizer(1e-10, 1e-8);
	    UnivariatePointValuePair result = optimizer.optimize(new MaxEval(10000),
                                             new UnivariateObjectiveFunction(f),
                                             GoalType.MINIMIZE,
                                             new SearchInterval(-1000, 1000));
	    System.out.println("UnivariateOptimizer for x*x + 4*x + 3 : " + result.getPoint() + " : " + result.getValue() );
	}
	
	public static void linearProgramming() {
        //      maximize 10 x1 - 57 x2 - 9 x3 - 24 x4
        //      subject to
        //          1/2 x1 - 11/2 x2 - 5/2 x3 + 9 x4  <= 0
        //          1/2 x1 -  3/2 x2 - 1/2 x3 +   x4  <= 0
        //              x1                  <= 1
        //      x1,x2,x3,x4 >= 0

        LinearObjectiveFunction f = new LinearObjectiveFunction(new double[] { 10, -57, -9, -24}, 0);
        
        ArrayList<LinearConstraint> constraints = new ArrayList<LinearConstraint>();

        constraints.add(new LinearConstraint(new double[] {0.5, -5.5, -2.5, 9}, Relationship.LEQ, 0));
        constraints.add(new LinearConstraint(new double[] {0.5, -1.5, -0.5, 1}, Relationship.LEQ, 0));
        constraints.add(new LinearConstraint(new double[] {  1,    0,    0, 0}, Relationship.LEQ, 1));
        
        SimplexSolver solver = new SimplexSolver();
        PointValuePair solution = solver.optimize(f, new LinearConstraintSet(constraints),
                                                  GoalType.MAXIMIZE,
                                                  new NonNegativeConstraint(true),
                                                  PivotSelectionRule.BLAND);
        VisualAssist.print("linearProgramming  points : ", solution.getPoint());
        System.out.println("linearProgramming  value : "  + solution.getValue() );      
	}

    /**
     * used when either the computation of the derivative is impossible (noisy functions, unpredictable discontinuities)
     * or difficult (complexity, computation cost).
     */
    public static void directSearch() {
        BiQuadratic biQuadratic = new BiQuadratic(4.0, 0.0, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY,
                Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY);
        final MultivariateFunctionMappingAdapter wrapped = new MultivariateFunctionMappingAdapter(biQuadratic,
                biQuadratic.getLower(), biQuadratic.getUpper());

        SimplexOptimizer optimizer = new SimplexOptimizer(1e-10, 1e-30);
        final AbstractSimplex simplex = new NelderMeadSimplex(new double[][] {
                wrapped.boundedToUnbounded(new double[] { 1.5, 2.75 }),
                wrapped.boundedToUnbounded(new double[] { 1.5, 2.95 }),
                wrapped.boundedToUnbounded(new double[] { 1.7, 2.90 })
        });

        final PointValuePair optimum = optimizer.optimize(new MaxEval(300),
                new ObjectiveFunction(wrapped),
                simplex,
                GoalType.MINIMIZE,
                new InitialGuess(wrapped.boundedToUnbounded(new double[] { 1.5, 2.25 })));
        final double[] bounded = wrapped.unboundedToBounded(optimum.getPoint());
        VisualAssist.print("find optimum : ", bounded);
        VisualAssist.print("optimum : ", biQuadratic.getBoundedXOptimum());
        VisualAssist.print(biQuadratic.getBoundedYOptimum());
    }

    private static class BiQuadratic implements MultivariateFunction {

        private final double xOptimum;
        private final double yOptimum;

        private final double xMin;
        private final double xMax;
        private final double yMin;
        private final double yMax;

        public BiQuadratic(final double xOptimum, final double yOptimum,
                           final double xMin, final double xMax,
                           final double yMin, final double yMax) {
            this.xOptimum = xOptimum;
            this.yOptimum = yOptimum;
            this.xMin     = xMin;
            this.xMax     = xMax;
            this.yMin     = yMin;
            this.yMax     = yMax;
        }

        public double value(double[] point) {
            // the function should never be called with out of range points
            Assert.assertTrue(point[0] >= xMin);
            Assert.assertTrue(point[0] <= xMax);
            Assert.assertTrue(point[1] >= yMin);
            Assert.assertTrue(point[1] <= yMax);

            final double dx = point[0] - xOptimum;
            final double dy = point[1] - yOptimum;
            return dx * dx + dy * dy;

        }

        public double[] getLower() {
            return new double[] { xMin, yMin };
        }

        public double[] getUpper() {
            return new double[] { xMax, yMax };
        }

        public double getBoundedXOptimum() {
            return (xOptimum < xMin) ? xMin : ((xOptimum > xMax) ? xMax : xOptimum);
        }

        public double getBoundedYOptimum() {
            return (yOptimum < yMin) ? yMin : ((yOptimum > yMax) ? yMax : yOptimum);
        }
    }


}
