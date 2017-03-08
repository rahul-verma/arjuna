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

import java.util.ArrayList;

public class ArjunaException extends Exception {
	private String screenshotPath = null;
	private ArrayList<Throwable> childThrowables = new ArrayList<Throwable>();
	private static final long serialVersionUID = -6553255112253599186L;

	// Parameterless Constructor
	public ArjunaException(String message) {
		super(message);
	}

	public ArjunaException(String message, String screenshotPath) {
		this(message);
		this.screenshotPath = screenshotPath;

	}

	public ArjunaException(String message, Throwable child) {
		super(message);
		try {
			throw child;
		} catch (ArjunaException f) {
			extractChildThrowables(f);
		} catch (java.lang.reflect.InvocationTargetException f) {
			if (ArjunaException.class.isAssignableFrom(f.getTargetException().getClass())) {
				ArjunaException z = (ArjunaException) f.getTargetException();
				extractChildThrowables(z);
			} else {
				insertChildThrowable(f);
			}
		} catch (Exception g) {
			insertChildThrowable(g);
		} catch (Throwable g) {
			insertChildThrowable(g);
		}
	}

	public ArjunaException(String message, Throwable child, String screenshotPath) {
		this(message, child);
		this.screenshotPath = screenshotPath;
	}

	public boolean containsScreenshot() {
		return screenshotPath != null;
	}

	public String getScreenshotPath() {
		return screenshotPath;
	}

	public String setScreenshotPath(String path) {
		return this.screenshotPath = path;
	}

	public void insertChildThrowable(Throwable e) {
		this.childThrowables.add(0, e);
	}

	public void appendChildThrowable(Throwable e) {
		this.childThrowables.add(0, e);
	}

	public void extractChildThrowables(ArjunaException e) {
		childThrowables = e.getChildThrowables();
		insertChildThrowable(e);
	}

	public ArrayList<Throwable> getChildThrowables() {
		return this.childThrowables;
	}
}
