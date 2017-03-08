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
package com.autocognite.pvt.batteries.exceptions;

public class Problem extends ArjunaException {
	/**
	 * 
	 */
	private static final long serialVersionUID = -3029394135447054950L;
	private String problemComponent = null;
	private String problemObject = null;
	private String problemMethod = null;
	private String problemCode = null;

	/**
	 * 
	 */

	// Parameterless Constructor
	private Problem(String text) {
		super(text);
	}

	private Problem(String text, Throwable e) {
		super(text, e);
	}

	private Problem(String text, String screenshotPath) {
		super(text, screenshotPath);
	}

	private Problem(String text, Throwable e, String screenshotPath) {
		super(text, e, screenshotPath);
	}

	// Constructor that accepts a message
	public Problem(final String component, final String objectName, final String methodName, final String code,
			final String text) {
		this(component + "::" + objectName + "::" + text);
		this.problemObject = objectName;
		this.problemMethod = methodName;
		this.problemComponent = component;
		this.problemCode = code;
	}

	public Problem(final String component, final String objectName, final String methodName, final String code,
			final String text, Throwable e) {
		this(component + "::" + objectName + "::" + text, e);
		this.problemObject = objectName;
		this.problemMethod = methodName;
		this.problemComponent = component;
		this.problemCode = code;
	}

	// Constructor that accepts a message and screenshot
	public Problem(final String component, final String objectName, final String methodName, final String code,
			final String text, final String screenshotPath) {
		this(component + "::" + objectName + "::" + text, screenshotPath);
		this.problemComponent = component;
		this.problemObject = objectName;
		this.problemMethod = methodName;
		this.problemCode = code;
	}

	public Problem(final String component, final String objectName, final String methodName, final String code,
			final String text, final String screenshotPath, Throwable e) {
		this(component + "::" + objectName + "::" + text, e, screenshotPath);
		this.problemComponent = component;
		this.problemObject = objectName;
		this.problemMethod = methodName;
		this.problemCode = code;
	}

	public String getProblemComponent() {
		return problemComponent;
	}

	public String getProblemObject() {
		return problemObject;
	}

	public String getProblemMethod() {
		return problemMethod;
	}

	public String getProblemCode() {
		return problemCode;
	}

	public String getProblemText() {
		return this.getMessage();
	}
}
