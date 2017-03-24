/*******************************************************************************
 * Copyright 2015-16 AutoCognite Testing Research Pvt Ltd
 * 
 * Website: www.AutoCognite.com
 * Email: support [at] autocognite.com
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/
package com.arjunapro.testauto.assertions;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

import com.arjunapro.sysauto.batteries.DataBatteries;
import com.arjunapro.testauto.checks.Checks;

import pvt.arjunapro.interfaces.Check;
import pvt.batteries.utils.StackBatteries;
import pvt.unitee.validator.lib.check.DefaultCheck;

public class Assertions {

	public static void setCheckErrorForAssertionIssue(Check check, Exception e){
		check.setError();
		check.setExceptionMessage("Error in assertion: " + e.getClass().getSimpleName() + ":" + e.getMessage());		
	}

	public static void fail(String purpose) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		try{
			check.setExceptionMessage("fail() explicitly called.");
			check.setPurpose(purpose);
			check.setFailure();
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}
//
//	public static void fail() throws Exception {
//		fail(null);
//	}

	public static void error(String purpose) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		try{
			check.setExceptionMessage("error() explicitly called.");
			check.setPurpose(purpose);
			check.setError();
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void error() throws Exception {
//		error(null);
//	}

	public static void assertTrue(String purpose, boolean bool) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be True");
		try{
			check.setBenchmark("True");
			if (Checks.isTrue(bool)) {
				check.setActualObservation("True");
			} else {
				check.setActualObservation("False");
				check.setFailure();
				check.setExceptionMessage("Condition is false.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertTrue(boolean bool) throws Exception {
//		assertTrue(null, bool);
//	}

	public static void assertFalse(String purpose, boolean bool) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be False");
		try{
			check.setBenchmark("False");
			if (Checks.isTrue(bool)) {
				check.setActualObservation("True");
				check.setFailure();
				check.setExceptionMessage("Condition is true.");
			} else {
				check.setActualObservation("False");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
			
	}

//	public static void assertFalse(boolean bool) throws Exception {
//		assertFalse(null, bool);	
//	}

	/*
	 * Assertions for Equality of Single Objects
	 */

	public static void updateCheckForNullExpectedObject(Check check){
		check.setError();
		check.setBenchmark("null");
		check.setExceptionMessage("Expected object can not be null");
		check.setActualObservation("Error: An error occured before this could be evaluated.");
	}

	public static void assertEquals(String purpose, String actual, String expected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal.");
		boolean hasFailed = false;
		try{
			if (Checks.isNull(expected)) {
				if (Checks.isNull(actual)){
					//passed
				} else {
					hasFailed = true;
				}
			} else {
				if (Checks.isNotEqual(actual, expected)) {
					hasFailed = true;
				}
			}
			if (hasFailed){
				check.setFailure();
				check.setBenchmark("\"" + expected + "\"");
				check.setActualObservation("\"" + actual + "\"");
				check.setExceptionMessage("\"" + actual + "\" is not equal to " + "\"" + expected + "\"");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertEquals(String actual, String expected) throws Exception {
//		assertEquals(null, actual, expected);
//	}

	public static void assertEquals(String purpose, int actual, int expected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal.");
		try{
			check.setBenchmark( String.format("%d", expected));
			check.setActualObservation( String.format("%d", actual));
			if (Checks.isNotEqual(actual, expected)) {
				check.setFailure();
				check.setExceptionMessage(actual + " is not equal to " + expected);
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertEquals(int actual, int expected) throws Exception {
//		assertEquals(null, actual, expected);
//	}

	public static void assertEquals(String purpose, long actual, long expected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal.");
		try{
			check.setBenchmark(String.format("%d", expected));
			check.setActualObservation(String.format("%d", actual));
			if (Checks.isNotEqual(actual, expected)) {
				check.setFailure();
				check.setExceptionMessage(actual + " is not equal to " + expected);
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertEquals(long actual, long expected) throws Exception {
//		assertEquals(null, actual, expected);
//	}

	public double round2(double num) {
		double result = num * 100;
		result = Math.floor(result);
		result = result / 100;
		return result;
	}

	public static void assertEquals(String purpose, float actual, float expected, float delta) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		try{
			Float diff = Math.abs(expected - actual);
			Float delta2 = Math.abs(delta);
			String deltaStr = String.format("%f", delta2);	
			String diffStr = String.format("%f", diff);

			check.setText("Should be Equal. (with resolution =" + deltaStr + " )");
			check.setBenchmark(String.format("%f", expected));
			check.setActualObservation(String.format("%f", actual));
			if (diff > delta2) {
				check.setFailure();
				check.setExceptionMessage(actual + " is not equal to " + expected
						+ ". Delta is " + diffStr
						+ ". Maximum Delta specified: " + deltaStr);
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertEquals(float actual, float expected, float delta) throws Exception {
//		assertEquals(null, actual, expected, delta);
//	}

	public static void assertEquals(String purpose, double actual, double expected, double delta) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		try{
			Double diff =  Math.abs(expected - actual);
			Double delta2 = Math.abs(delta);
			DecimalFormat df = new DecimalFormat("0");
			df.setMaximumFractionDigits(340);
			String deltaStr = df.format(delta2);
			String diffStr = df.format(diff);
			DecimalFormat df2 = new DecimalFormat("0*.0*");
			df2.setMaximumFractionDigits(340);

			check.setText("Should be Equal. (with resolution =" + deltaStr + " )");
			check.setBenchmark(df2.format(expected));
			check.setActualObservation(df2.format(actual));
			if (diff > delta2) {
				check.setFailure();
				check.setExceptionMessage(actual + " is not equal to " + expected
						+ ". Delta is " + diffStr
						+ ". Maximum Delta specified: " + deltaStr);
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertEquals(double actual, double expected, double delta) throws Exception {
//		assertEquals(null, actual, expected, delta);
//	}

	/*
	 * By default .equals is same as == for an Object i.e. it checks if both objects are
	 * pointing to the same object. In essence, unless, .equals method is overriden
	 * the behavior of this assertion is same as AssertSame.
	 */
	public static void assertEquals(String purpose, Object actual, Object expected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal.");
		boolean hasFailed = false;
		try{
			if (Checks.isNull(expected)) {
				if (Checks.isNull(actual)){
					//passed
				} else {
					hasFailed = true;
				}
			} else {
				if (Checks.isNotEqual(actual, expected)) {
					hasFailed = true;
				}
			}
			if (hasFailed){
				check.setFailure();
				check.setBenchmark(expected.toString());
				check.setActualObservation(actual.toString());
				check.setExceptionMessage(actual + " is not equal to " + expected);
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertEquals(Object actual, Object expected) throws Exception {
//		assertEquals(null, actual, expected);
//	}

	public static void assertSame(String purpose, Object actual, Object expected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Same.");
		boolean hasFailed = false;
		try{
			if (Checks.isNull(expected)) {
				if (Checks.isNull(actual)){
					//passed
				} else {
					hasFailed = true;
				}
			} else {
				if (Checks.isNotSame(actual, expected)) {
					hasFailed = true;
				}
			}
			if (hasFailed){
				check.setFailure();
				check.setBenchmark("Object with hascode: " + expected.hashCode());
				check.setActualObservation("Object with hascode: " + actual.hashCode());
				check.setExceptionMessage("Object with id: " + actual.hashCode()
				+ " is not same as object with id: "
				+ expected.hashCode());
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertSame(Object actual, Object expected) throws Exception {
//		assertSame(null, actual, expected);
//	}

	/*
	 * Assertions for Non-Equality of Single Objects
	 */

	public static void assertNotEqual(String purpose, String actual, String unexpected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should NOT be Equal.");
		boolean hasFailed = false;
		try{
			if (Checks.isNull(unexpected)) {
				if (Checks.isNull(actual)){
					hasFailed = true;
				} else {
					//passed
				}
			} else {
				if (Checks.isEqual(actual, unexpected)) {
					hasFailed = true;
				}
			}
			if (hasFailed){
				check.setFailure();
				check.setBenchmark("\"" + unexpected + "\"");
				check.setActualObservation("\"" + actual + "\"");
				check.setExceptionMessage("\"" + actual + "\" is equal to " + "\"" + unexpected + "\"");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertNotEqual(String actual, String unexpected) throws Exception {
//		assertNotEqual(null, actual, unexpected);
//	}

	public static void assertNotEqual(String purpose, int actual, int unexpected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should NOT be Equal.");
		try{
			check.setBenchmark( String.format("%d", unexpected));
			check.setActualObservation( String.format("%d", actual));
			if (Checks.isEqual(actual, unexpected)) {
				check.setFailure();
				check.setExceptionMessage(actual + " is equal to " + unexpected);
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertNotEqual(int actual, int unexpected) throws Exception {
//		assertNotEqual(null, actual, unexpected);
//	}

	public static void assertNotEqual(String purpose, long actual, long unexpected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should NOT be Equal.");
		try{
			check.setBenchmark(String.format("%d", unexpected));
			check.setActualObservation(String.format("%d", actual));
			if (Checks.isEqual(actual, unexpected)) {
				check.setFailure();
				check.setExceptionMessage(actual + " is equal to " + unexpected);
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
			
	}

//	public static void assertNotEqual(long actual, long unexpected) throws Exception {
//		assertNotEqual(null, actual, unexpected);
//	}

	public static void assertNotEqual(String purpose, float actual, float unexpected, float delta) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		try{		
			Float diff = Math.abs(unexpected - actual);
			Float delta2 = Math.abs(delta);
			String deltaStr = String.format("%f", delta2);	
			String diffStr = String.format("%f", diff);

			check.setText("Should NOT be Equal. (with resolution =" + deltaStr + " )");
			check.setBenchmark(String.format("%f", unexpected));
			check.setActualObservation(String.format("%f", actual));
			if (diff <= delta) {
				check.setFailure();
				check.setExceptionMessage(actual + " is equal to " + unexpected
						+ ". Delta is " + diffStr
						+ ". Maximum Delta specified: " + deltaStr);
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}


//	public static void assertNotEqual(float actual, float unexpected, float delta) throws Exception {
//		assertNotEqual(null, actual, unexpected, delta);
//	}

	public static void assertNotEqual(String purpose, double actual, double unexpected, double delta) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		try{		
			Double diff =  Math.abs(unexpected - actual);
			Double delta2 = Math.abs(delta);
			DecimalFormat df = new DecimalFormat("0");
			df.setMaximumFractionDigits(340);
			String deltaStr = df.format(delta2);
			String diffStr = df.format(diff);
			DecimalFormat df2 = new DecimalFormat("0*.0*");
			df2.setMaximumFractionDigits(340);

			check.setText("Should NOT be Equal. (with resolution =" + deltaStr + " )");
			check.setBenchmark(df2.format(unexpected));
			check.setActualObservation(df2.format(actual));
			if (diff <= delta2) {
				check.setFailure();
				check.setExceptionMessage(actual + " is equal to " + unexpected
						+ ". Delta is " + diffStr
						+ ". Maximum Delta specified: " + deltaStr);
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertNotEqual(double actual, double unexpected, double delta) throws Exception {
//		assertNotEqual(null, actual, unexpected, delta);
//	}

	/*
	 * By default .equals is same as == for an Object i.e. it checks if both objects are
	 * pointing to the same object. In essence, unless, .equals method is overriden
	 * the behavior of this assertion is same as AssertSame.
	 */
	public static void assertNotEqual(String purpose, Object actual, Object unexpected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should NOT be Equal.");
		boolean hasFailed = false;
		try{
			if (Checks.isNull(unexpected)) {
				if (Checks.isNull(actual)){
					hasFailed = true;
				} else {
					//passed
				}
			} else {
				if (Checks.isEqual(actual, unexpected)) {
					hasFailed = true;
				}
			}
			if (hasFailed){
				check.setFailure();
				check.setBenchmark(unexpected.toString());
				check.setActualObservation(actual.toString());
				check.setExceptionMessage(actual + " is equal to " + unexpected);
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertNotEqual(Object actual, Object unexpected) throws Exception {
//		assertNotEqual(null, actual, unexpected);
//	}

	public static void assertNotSame(String purpose, Object actual, Object unexpected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should NOT be Same.");
		boolean hasFailed = false;
		try{
			if (Checks.isNull(unexpected)) {
				if (Checks.isNull(actual)){
					hasFailed = true;
				} else {
					//passed
				}
			} else {
				if (Checks.isEqual(actual, unexpected)) {
					hasFailed = true;
				}
			}
			if (hasFailed){
				check.setFailure();
				check.setBenchmark("Object with hascode: " + unexpected.hashCode());
				check.setActualObservation("Object with hascode: " + actual.hashCode());
				check.setExceptionMessage("Object with id: " + actual.hashCode()
				+ " is same as object with id: "
				+ unexpected.hashCode());
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertNotSame(Object actual, Object unexpected) throws Exception {
//		assertNotSame(null, actual, unexpected);
//	}

	/*
	 * Array Assertions
	 */
	public static void assertArrayEquals(String purpose, boolean[] actual, boolean[] expected) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal. Expected array can not be null.");
		try{
			if (Checks.isNull(expected)) {
				updateCheckForNullExpectedObject(check);
			}
			if (!Checks.isEqual(actual, expected)) {
				check.setFailure();
				check.setBenchmark(Arrays.toString(expected));
				check.setActualObservation(Arrays.toString(actual));
				check.setExceptionMessage(Arrays.toString(actual) + " array is not equal to " + Arrays.toString(expected) + " array.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
			
	}

//	public static void assertArrayEquals(boolean[] actual, boolean[] expected)throws Exception {
//		assertArrayEquals(null, actual, expected);		
//	}

	public static void assertArrayEquals(String purpose, byte[] actual, byte[] expected)throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal. Expected array can not be null.");
		try{
			if (Checks.isNull(expected)) {
				updateCheckForNullExpectedObject(check);
			}
			if (!Checks.isEqual(actual, expected)) {
				check.setFailure();
				check.setBenchmark(Arrays.toString(expected));
				check.setActualObservation(Arrays.toString(actual));
				check.setExceptionMessage(Arrays.toString(actual) + " array is not equal to " + Arrays.toString(expected) + " array.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertArrayEquals(byte[] actual, byte[] expected)throws Exception {
//		assertArrayEquals(null, actual, expected);	
//	}

	public static void assertArrayEquals(String purpose, char[] actual, char[] expected)throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal. Expected array can not be null.");
		try{
			if (Checks.isNull(expected)) {
				updateCheckForNullExpectedObject(check);
			}
			if (!Checks.isEqual(actual, expected)) {
				check.setFailure();
				check.setBenchmark(Arrays.toString(expected));
				check.setActualObservation(Arrays.toString(actual));
				check.setExceptionMessage(Arrays.toString(actual) + " array is not equal to " + Arrays.toString(expected) + " array.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
					
	}
//
//	public static void assertArrayEquals(char[] actual, char[] expected)throws Exception {
//		assertArrayEquals(null, actual, expected);		
//	}


	public static void assertArrayEquals(String purpose, double[] actual, double[] expected)throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal. Expected array can not be null.");
		try{
			if (Checks.isNull(expected)) {
				updateCheckForNullExpectedObject(check);
			}
			if (!Checks.isEqual(actual, expected)) {
				check.setFailure();
				check.setBenchmark(Arrays.toString(expected));
				check.setActualObservation(Arrays.toString(actual));
				check.setExceptionMessage(Arrays.toString(actual) + " array is not equal to " + Arrays.toString(expected) + " array.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}
//
//	public static void assertArrayEquals(double[] actual, double[] expected)throws Exception {
//		assertArrayEquals(null, actual, expected);		
//	}

	public static void assertArrayEquals(String purpose, float[] actual, float[] expected)throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal. Expected array can not be null.");
		try{
			if (Checks.isNull(expected)) {
				updateCheckForNullExpectedObject(check);
			}
			if (!Checks.isEqual(actual, expected)) {
				check.setFailure();
				check.setBenchmark(Arrays.toString(expected));
				check.setActualObservation(Arrays.toString(actual));
				check.setExceptionMessage(Arrays.toString(actual) + " array is not equal to " + Arrays.toString(expected) + " array.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}
//
//	public static void assertArrayEquals(float[] actual, float[] expected)throws Exception {
//		assertArrayEquals(null, actual, expected);		
//	}

	public static void assertArrayEquals(String purpose, int[] actual, int[] expected)throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal. Expected array can not be null.");
		try{
			if (Checks.isNull(expected)) {
				updateCheckForNullExpectedObject(check);
			}
			if (!Checks.isEqual(actual, expected)) {
				check.setFailure();
				check.setBenchmark(Arrays.toString(expected));
				check.setActualObservation(Arrays.toString(actual));
				check.setExceptionMessage(Arrays.toString(actual) + " array is not equal to " + Arrays.toString(expected) + " array.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
			
	}
//
//	public static void assertArrayEquals(int[] actual, int[] expected)throws Exception {
//		assertArrayEquals(null, actual, expected);	
//	}

	public static void assertArrayEquals(String purpose, long[] actual, long[] expected)throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal. Expected array can not be null.");
		try{
			if (Checks.isNull(expected)) {
				updateCheckForNullExpectedObject(check);
			}
			if (!Checks.isEqual(actual, expected)) {
				check.setFailure();
				check.setBenchmark(Arrays.toString(expected));
				check.setActualObservation(Arrays.toString(actual));
				check.setExceptionMessage(Arrays.toString(actual) + " array is not equal to " + Arrays.toString(expected) + " array.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
				
	}

//	public static void assertArrayEquals(short[] actual, short[] expected)throws Exception {
//		assertArrayEquals(null, actual, expected);		
//	}

	public static void assertArrayEquals(String purpose, short[] actual, short[] expected)throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal. Expected array can not be null.");
		try{
			if (Checks.isNull(expected)) {
				updateCheckForNullExpectedObject(check);
			}
			if (!Checks.isEqual(actual, expected)) {
				check.setFailure();
				check.setBenchmark(Arrays.toString(expected));
				check.setActualObservation(Arrays.toString(actual));
				check.setExceptionMessage(Arrays.toString(actual) + " array is not equal to " + Arrays.toString(expected) + " array.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
			
	}

//	public static void assertArrayEquals(long[] actual, long[] expected)throws Exception {
//		assertArrayEquals(null, actual, expected);		
//	}

	public static void assertArrayEquals(String purpose, Object[] actual, Object[] expected)throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be Equal. Expected array can not be null.");
		try{
			if (Checks.isNull(expected)) {
				updateCheckForNullExpectedObject(check);
			}
			if (!Checks.isEqual(actual, expected)) {
				check.setFailure();
				check.setBenchmark(Arrays.toString(expected));
				check.setActualObservation(Arrays.toString(actual));
				check.setExceptionMessage(Arrays.toString(actual) + " array is not equal to " + Arrays.toString(expected) + " array.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
			
	}

//	public static void assertArrayEquals(Object[] actual, Object[] expected)throws Exception {
//		assertArrayEquals(null, actual, expected);
//	}

	public static void assertNull(String purpose, Object obj) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should be null.");
		check.setBenchmark("null");
		try{
			if (Checks.isNotNull(obj)) {
				check.setFailure();
				check.setActualObservation("Object with hashCode: " + obj.hashCode());
				check.setExceptionMessage("Object with id: " + obj.hashCode() + " is not null.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertNull(Object obj) throws Exception {
//		assertNull(null, obj);
//	}

	public static void assertNotNull(String purpose, Object obj) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Should not be null.");
		check.setBenchmark("Any non-null object");
		try{
			if (Checks.isNull(obj)) {
				check.setFailure();
				check.setActualObservation("null");
				check.setExceptionMessage("Supplied object is null.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertNotNull(Object obj) throws Exception {
//		assertNotNull(null, obj);
//	}

	/*
	 * Container assertions
	 */

	public static void assertContains(String purpose, String parent, String child) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Sub-String should be Present.");
		try{
			if (Checks.isNull(parent)) {
				updateCheckForNullExpectedObject(check);
				check.setExceptionMessage("Parent object is null");
			}
			if (Checks.doesNotContain(parent, child)) {
				check.setFailure();
				check.setBenchmark(String.format("Any string containing: \"%s\"", child));
				check.setActualObservation("\"" + parent + "\"");
				check.setExceptionMessage("\"" + parent + "\" does not contain \"" + child + "\" string.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
			
	}

//	public static void assertContains(String parent, String child) throws Exception {
//		assertContains(null, parent, child);
//	}

	public static void assertContains(String purpose, ArrayList<String> parent, String child) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("ArrayList should contain given item.");
		try{
			if (Checks.isNull(parent)) {
				updateCheckForNullExpectedObject(check);
				check.setExceptionMessage("Parent object is null");
			}
			if (Checks.doesNotContain(parent, child)) {
				check.setFailure();
				check.setBenchmark( String.format("Any array list containing: \"%s\"", child));
				check.setActualObservation(DataBatteries.flatten(parent));
				check.setExceptionMessage(parent + " does not contain \"" + child + "\" string.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertContains(ArrayList<String> parent, String child) throws Exception {
//		assertContains(null, parent, child);
//	}

	public static void assertContains(String purpose, String[] parent, String child) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Array should contain given item.");
		try{
			if (Checks.isNull(parent)) {
				updateCheckForNullExpectedObject(check);
				check.setExceptionMessage("Parent object is null");
			}
			if (Checks.doesNotContain(parent, child)) {
				check.setFailure();
				check.setBenchmark( String.format("Any array containing: \"%s\"", child));
				check.setActualObservation(Arrays.toString(parent));
				check.setExceptionMessage(Arrays.toString(parent) + " does not contain \"" + child + "\" string.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertContains(String[] parent, String child) throws Exception {
//		assertContains(null,parent, child);
//	}

	public static void assertContains(String purpose, HashMap<String, Object> parent, String child) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("HashMap should contain given key.");
		try{
			if (Checks.isNull(parent)) {
				updateCheckForNullExpectedObject(check);
				check.setExceptionMessage("Parent object is null");
			}
			if (Checks.doesNotContain(parent, child)) {
				check.setFailure();
				check.setBenchmark( String.format("Any HashMap containing the key: \"%s\"", child));
				check.setActualObservation("Keys in HashMap: \n" + DataBatteries.flatten(parent.keySet()));
				check.setExceptionMessage(parent + " does not contain \"" + child + "\" key.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertContains(HashMap<String, Object> parent, String child) throws Exception {
//		assertContains(null,parent, child);
//	}

	public static void assertDoesNotContain(String purpose, String parent, String child) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Sub-String should NOT be Present.");
		try{
			if (Checks.isNull(parent)) {
				updateCheckForNullExpectedObject(check);
				check.setExceptionMessage("Parent object is null");
			}
			if (Checks.contains(parent, child)) {
				check.setFailure();
				check.setBenchmark(String.format("Any string NOT containing: \"%s\"", child));
				check.setActualObservation("\"" + parent + "\"");
				check.setExceptionMessage("\"" + parent + "\" contains \"" + child + "\" string.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
			
	}

//	public static void assertDoesNotContain(String parent, String child) throws Exception {
//		assertDoesNotContain(null, parent, child);
//	}

	public static void assertDoesNotContain(String purpose, ArrayList<String> parent, String child) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("ArrayList should NOT contain given item.");
		try{
			if (Checks.isNull(parent)) {
				updateCheckForNullExpectedObject(check);
				check.setExceptionMessage("Parent object is null");
			}
			if (Checks.contains(parent, child)) {
				check.setFailure();
				check.setBenchmark( String.format("Any array list NOT containing: \"%s\"", child));
				check.setActualObservation(DataBatteries.flatten(parent));
				check.setExceptionMessage(parent + " contains \"" + child + "\" string.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertDoesNotContain(ArrayList<String> parent, String child) throws Exception {
//		assertDoesNotContain(null, parent, child);
//	}

	public static void assertDoesNotContain(String purpose, String[] parent, String child) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("Array should NOT contain given item.");
		try{
			if (Checks.isNull(parent)) {
				updateCheckForNullExpectedObject(check);
				check.setExceptionMessage("Parent object is null");
			}
			if (Checks.contains(parent, child)) {
				check.setFailure();
				check.setBenchmark( String.format("Any array NOT containing: \"%s\"", child));
				check.setActualObservation(Arrays.toString(parent));
				check.setExceptionMessage(Arrays.toString(parent) + " contains \"" + child + "\" string.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertDoesNotContain(String[] parent, String child) throws Exception {
//		assertDoesNotContain(null, parent, child);
//	}

	public static void assertDoesNotContain(String purpose, HashMap<String, Object> parent, String child) throws Exception {
		Check check = new DefaultCheck(StackBatteries.getCurrentSimpleClasseName(), StackBatteries.getCurrentMethodName());
		check.setPurpose(purpose);
		check.setText("HashMap should NOT contain given key.");
		try{
			if (Checks.isNull(parent)) {
				updateCheckForNullExpectedObject(check);
				check.setExceptionMessage("Parent object is null");
			}
			if (Checks.contains(parent, child)) {
				check.setFailure();
				check.setBenchmark( String.format("Any HashMap NOT containing the key: \"%s\"", child));
				check.setActualObservation("Keys in HashMap: \n" + DataBatteries.flatten(parent.keySet()));
				check.setExceptionMessage(parent + " contains \"" + child + "\" key.");
			}
		} catch (Exception e){
			setCheckErrorForAssertionIssue(check, e);
		}

		check.evaluate();
		
	}

//	public static void assertDoesNotContain(HashMap<String, Object> parent, String child) throws Exception {
//		assertDoesNotContain(null, parent, child);
//	}
}
