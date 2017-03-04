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
package com.autocognite.batteries.checks;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class Checks {

	public static boolean isTrue(boolean bool) {
		if (bool == true) {
			return true;
		} else {
			return false;
		}
	}

	public static boolean isFalse(boolean bool) {
		if (bool == false) {
			return true;
		} else {
			return false;
		}
	}

	/*
	 * Assertions for Equality of Single Objects
	 */

	public static boolean isEqual(String actual, String expected) throws NullPointerException {
		return expected.equals(actual);
	}

	public static boolean isEqual(int actual, int expected) {
		return expected == actual;
	}

	public static boolean isEqual(long actual, long expected) {
		return expected == actual;
	}

	public double round2(double num) {
		double result = num * 100;
		result = Math.floor(result);
		result = result / 100;
		return result;
	}

	public static boolean isAlmostEqual(float actual, float expected, float delta) {
		Float diff = Math.abs(expected - actual);
		Float delta2 = Math.abs(delta);
		return diff <= delta2;
	}

	public static boolean isAlmostEqual(double actual, double expected, double delta) {
		Double diff = Math.abs(expected - actual);
		Double delta2 = Math.abs(delta);
		return diff <= delta2;
	}

	public static boolean isEqual(Object actual, Object expected) throws NullPointerException {
		return expected.equals(actual);
	}

	public static boolean isSame(Object actual, Object expected) throws NullPointerException {
		return expected == actual;
	}

	/*
	 * Assertions for In-Equality of Single Objects
	 */

	public static boolean isNotEqual(String actual, String expected) throws NullPointerException {
		return !(isEqual(actual, expected));
	}

	public static boolean isNotEqual(int actual, int expected) {
		return !(isEqual(actual, expected));
	}

	public static boolean isNotEqual(long actual, long expected) {
		return !(isEqual(actual, expected));
	}

	public static boolean isNotEqual(float actual, float expected, float delta) {
		return !(isAlmostEqual(actual, expected, delta));
	}

	public static boolean isNotEqual(double actual, double expected, double delta) {
		return !(isAlmostEqual(actual, expected, delta));
	}

	public static boolean isNotEqual(Object actual, Object expected) throws NullPointerException {
		return !(isEqual(actual, expected));
	}

	public static boolean isDifferent(Object actual, Object expected) throws NullPointerException {
		return !(isSame(actual, expected));
	}

	public static boolean isNotSame(Object actual, Object expected) throws NullPointerException {
		return !(isSame(actual, expected));
	}

	/*
	 * Array Assertions
	 */
	public static boolean isEqual(boolean[] actual, boolean[] expected) {
		return Arrays.equals(expected, actual);
	}

	public static boolean isEqual(byte[] actual, byte[] expected) {
		return Arrays.equals(expected, actual);
	}

	public static boolean isEqual(char[] actual, char[] expected) {
		return Arrays.equals(expected, actual);
	}

	public static boolean isEqual(double[] actual, double[] expected) {
		return Arrays.equals(expected, actual);
	}

	public static boolean isEqual(float[] actual, float[] expected) {
		return Arrays.equals(expected, actual);
	}

	public static boolean isEqual(int[] actual, int[] expected) {
		return Arrays.equals(expected, actual);
	}

	public static boolean isEqual(long[] actual, long[] expected) {
		return Arrays.equals(expected, actual);
	}

	public static boolean isEqual(short[] actual, short[] expected) {
		return Arrays.equals(expected, actual);
	}

	public static boolean isEqual(Object[] actual, Object[] expected) {
		return Arrays.equals(expected, actual);
	}

	/*
	 * Null assertions
	 */

	public static boolean isNull(Object obj) {
		return obj == null;
	}

	public static boolean isNotNull(Object obj) {
		return !(isNull(obj));
	}

	/*
	 * Container Checks
	 */
	public static boolean contains(String parent, String child) throws NullPointerException {
		return parent.contains(child);
	}

	public static boolean contains(ArrayList<String> parent, String child) throws NullPointerException {
		return parent.contains(child);
	}

	public static boolean contains(String[] parent, String child) throws NullPointerException {
		return Arrays.asList(parent).contains(child);
	}

	public static boolean contains(HashMap<String, Object> parent, String child) throws NullPointerException {
		return parent.keySet().contains(child);
	}

	public static boolean doesNotContain(String parent, String child) throws NullPointerException {
		return !contains(parent, child);
	}

	public static boolean doesNotContain(ArrayList<String> parent, String child) throws NullPointerException {
		return !contains(parent, child);
	}

	public static boolean doesNotContain(String[] parent, String child) throws NullPointerException {
		return !contains(parent, child);
	}

	public static boolean doesNotContain(HashMap<String, Object> parent, String child) throws NullPointerException {
		return !contains(parent, child);
	}
}
