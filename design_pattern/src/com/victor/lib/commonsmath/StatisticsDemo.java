package com.victor.lib.commonsmath;

import org.apache.commons.math3.stat.Frequency;
import org.apache.commons.math3.stat.StatUtils;
import org.apache.commons.math3.stat.correlation.Covariance;
import org.apache.commons.math3.stat.correlation.KendallsCorrelation;
import org.apache.commons.math3.stat.correlation.PearsonsCorrelation;
import org.apache.commons.math3.stat.correlation.SpearmansCorrelation;
import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;
import org.apache.commons.math3.stat.descriptive.StorelessUnivariateStatistic;
import org.apache.commons.math3.stat.descriptive.SummaryStatistics;
import org.apache.commons.math3.stat.descriptive.UnivariateStatistic;
import org.apache.commons.math3.stat.descriptive.moment.Mean;
import org.apache.commons.math3.stat.inference.TestUtils;
import org.apache.commons.math3.stat.ranking.NaNStrategy;
import org.apache.commons.math3.stat.ranking.NaturalRanking;
import org.apache.commons.math3.stat.ranking.TiesStrategy;
import org.apache.commons.math3.stat.regression.GLSMultipleLinearRegression;
import org.apache.commons.math3.stat.regression.OLSMultipleLinearRegression;
import org.apache.commons.math3.stat.regression.SimpleRegression;

import com.victor.utilities.visual.VisualAssist;

public class StatisticsDemo {

	/**
	 * min, max, mean, geometric mean, n, sum, sum of squares, standard
	 * deviation, variance, percentiles, skewness, kurtosis, median
	 */
	public static void descriptive() {
		double[] values = new double[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
		UnivariateStatistic stat = new Mean();
		System.out.println("mean = " + stat.evaluate(values));
		System.out.println("mean = " + stat.evaluate(values, 0, 1)); // [ 0 , 1
																		// )
																		// useful
																		// for
																		// range

		StorelessUnivariateStatistic stat1 = new Mean();
		for (int i = 0; i < values.length; i++) {
			stat1.increment(values[i]);
		}
		System.out.println("mean after clear is NaN = " + stat1.getResult());

		/**
		 * use DescriptiveStatistics min, max, mean, geometric mean, n, sum, sum
		 * of squares, standard deviation, variance, percentiles, skewness,
		 * kurtosis, median
		 */
		DescriptiveStatistics descriptiveStatistics = new DescriptiveStatistics();
		for (int i = 0; i < values.length; i++) {
			descriptiveStatistics.addValue(values[i]);
		}
		System.out.println("std = "
				+ descriptiveStatistics.getStandardDeviation());
		System.out.println("median = "
				+ descriptiveStatistics.getPercentile(30));

		/**
		 * use SummaryStatistics, read only once, no store overhead min, max,
		 * mean, geometric mean, n, sum, sum of squares, standard deviation,
		 * variance
		 */
		SummaryStatistics summaryStat = new SummaryStatistics();
		for (int i = 0; i < values.length; i++) {
			descriptiveStatistics.addValue(values[i]);
		}
		System.out.println(summaryStat.getMean());
		System.out.println(summaryStat.getStandardDeviation());

		/**
		 * use StatUtils
		 */
		System.out.println(StatUtils.mean(values));
		System.out.println(StatUtils.variance(values));
		System.out.println(StatUtils.percentile(values, 50));
		System.out.println(StatUtils.mean(values, 0, 3)); // Compute the mean of
															// the first three
															// values in the
															// array

		/**
		 * use DescriptiveStats Maintain a "rolling mean" of the most recent 3
		 * values from an input stream
		 */
		DescriptiveStatistics descriptivestats = new DescriptiveStatistics();
		descriptivestats.setWindowSize(3);
		for (int i = 0; i < values.length; i++) {
			descriptivestats.addValue(values[i]);
			double[] rollingvalues = descriptivestats.getValues(); // this could
																	// give you
																	// the
																	// sliced
																	// data
			for (double d : rollingvalues)
				System.out.print(d + " ");
			System.out.println("\nrolling mean" + descriptivestats.getMean());
		}
	}

	/**
	 * maintaining counts and percentages of discrete values. produce histogram,
	 * map double to integer
	 */
	public static void frequency() {
		System.out
				.println("---------------------frequency---------------------------");
		Frequency f = new Frequency();
		f.addValue(1);
		f.addValue(new Integer(1));
		f.addValue(new Long(1));
		f.addValue(2);
		f.addValue(new Integer(-1));
		System.out.println(f.getCount(1)); // displays 3
		System.out.println(f.getCumPct(0)); // displays 0.2
		System.out.println(f.getPct(new Integer(1))); // displays 0.6
		System.out.println(f.getCumPct(-2)); // displays 0
		System.out.println(f.getCumPct(10)); // displays 1
	}

	/**
	 * y = intercept + slope * x
	 */
	public static void simpleRegression() {
		System.out.println("---------------------simple regression---------------------------");
		double[][] data = { { 1, 3 }, { 2, 5 }, { 3, 7 }, { 4, 14 }, { 5, 11 } };
		SimpleRegression regression = new SimpleRegression();
		regression.addData(data);
		regression.addData(3d, 3d);
		// Now all statistics are defined.
		System.out.println(regression.getIntercept()); // displays intercept of regression line
		System.out.println(regression.getSlope()); // displays slope of regression line
		System.out.println(regression.getSlopeStdErr()); // displays slope standard error
		System.out.println(regression.predict(1.5d)); // displays predicted y value for x = 1.5
	}

	/**
	 * Ordinary Least Squares Regression Y=X*b+u Y is regressand, X is a [n,k]
	 * matrix regressors, b is regression parameters and u is error terms or
	 * residuals
	 */
	public static void multipleLinearRegression() {
		System.out
				.println("---------------------OLSMultipleLinearRegression---------------------------");
		OLSMultipleLinearRegression regression = new OLSMultipleLinearRegression();
		double[] y = new double[] { 11.0, 12.0, 13.0, 14.0, 15.0, 16.0 };
		double[][] x = new double[6][];
		x[0] = new double[] { 0, 0, 0, 0, 0 };
		x[1] = new double[] { 2.0, 0, 0, 0, 0 };
		x[2] = new double[] { 0, 3.0, 0, 0, 0 };
		x[3] = new double[] { 0, 0, 4.0, 0, 0 };
		x[4] = new double[] { 0, 0, 0, 5.0, 0 };
		x[5] = new double[] { 0, 0, 0, 0, 6.0 };
		regression.newSampleData(y, x);
		double[] beta = regression.estimateRegressionParameters();
		double[] residuals = regression.estimateResiduals();
		double[][] parametersVariance = regression
				.estimateRegressionParametersVariance();
		double regressandVariance = regression.estimateRegressandVariance();
		double rSquared = regression.calculateRSquared();
		double sigma = regression.estimateRegressionStandardError();
		VisualAssist.print("beta is ", beta);
	}

	public static void multipleLinearRegression1() {
		System.out.println("---------------------GLSMultipleLinearRegression---------------------------");
		GLSMultipleLinearRegression regression = new GLSMultipleLinearRegression();
		double[] y = new double[] { 11.0, 12.0, 13.0, 14.0, 15.0, 16.0 };
		double[][] x = new double[6][];
		x[0] = new double[] { 0, 0, 0, 0, 0 };
		x[1] = new double[] { 2.0, 0, 0, 0, 0 };
		x[2] = new double[] { 0, 3.0, 0, 0, 0 };
		x[3] = new double[] { 0, 0, 4.0, 0, 0 };
		x[4] = new double[] { 0, 0, 0, 5.0, 0 };
		x[5] = new double[] { 0, 0, 0, 0, 6.0 };
		double[][] omega = new double[6][];
		omega[0] = new double[] { 1.1, 0, 0, 0, 0, 0 };
		omega[1] = new double[] { 0, 2.2, 0, 0, 0, 0 };
		omega[2] = new double[] { 0, 0, 3.3, 0, 0, 0 };
		omega[3] = new double[] { 0, 0, 0, 4.4, 0, 0 };
		omega[4] = new double[] { 0, 0, 0, 0, 5.5, 0 };
		omega[5] = new double[] { 0, 0, 0, 0, 0, 6.6 };
		regression.newSampleData(y, x, omega);
	}

	/**
	 * Some statistical algorithms require that input data be replaced by ranks
	 */
	public static void rankTransform() {
		System.out.println("---------------------GLSMultipleLinearRegression---------------------------");
		NaturalRanking ranking = new NaturalRanking(NaNStrategy.MINIMAL, TiesStrategy.AVERAGE);
		double[] data = { 20, 17, 30, 42.3, 17, 50, Double.NaN, Double.NEGATIVE_INFINITY, 17 };
		double[] ranks = ranking.rank(data);
		VisualAssist.print("rankTransform", ranks);
	}
	
	/**
	 * Unbiased covariance : cov(X, Y) = sum [(xi - E(X))(yi - E(Y))] / (n - 1)
	 * could be used by calculate stock with index correlation, index divide to period, stock with same period
	 */
	public static void correlationDemo() {
		System.out.println("---------------------correlation---------------------------");
		double[] x = { 20, 17, 30, 42.3, 17, 50 };
		double[] y = { 20, 17, 30, 42.3, 17, 50 };
		System.out.println(new Covariance().covariance(x, y));				// unbiased covariance
		System.out.println(new Covariance().covariance(x, y, false));		// non-bias-corrected covariances
		System.out.println(new PearsonsCorrelation().correlation(x, y));
		System.out.println(new SpearmansCorrelation().correlation(x, y));
		System.out.println(new KendallsCorrelation().correlation(x, y));
//		new Covariance().computeCovarianceMatrix(data);						//covariance matrix
	}
	
	public static void testDemo() {
		System.out.println("---------------------stats test---------------------------");
		double[] observed = {1d, 2d, 3d};
		double mu = 2.5d;
		double alpha = 0.05;
		System.out.println(TestUtils.t(mu, observed));
		System.out.println(TestUtils.tTest(mu, observed));
		System.out.println(TestUtils.tTest(mu, observed, alpha));
		
		long[] observed1 = {10, 9, 11};
		double[] expected1 = {10.1, 9.8, 10.3};
		System.out.println(TestUtils.chiSquare(expected1, observed1));
		
		double[] expected2 = new double[]{0.54d, 0.40d, 0.05d, 0.01d};
		long[] observed2 = new long[]{70, 79, 3, 4};
		System.out.println(TestUtils.g(expected2, observed2));
	}

	public static void main(String[] args) {
		descriptive();
		frequency();
		simpleRegression();
		multipleLinearRegression();
		multipleLinearRegression1();
		rankTransform();
		correlationDemo();
		testDemo();
	}
}
