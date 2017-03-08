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
package com.autocognite.pvt.batteries.root;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;

public abstract class DefaultRoot {
	private static Logger logger = Logger.getLogger(RunConfig.getCentralLogName());

	protected Logger getLogger() {
		return logger;
	}

	public boolean isAutoCogniteClass() throws Exception {
		return this.getFullClassName().startsWith("com.autocognite");
	}

	public String getPackageName() throws Exception {
		int index = this.getFullClassName().lastIndexOf(this.getClass().getSimpleName());
		if (index == 0) {
			return "default";
		} else {
			return this.getFullClassName().substring(0, index - 1);
		}
	}

	public String getNameForLog() throws Exception {
		return this.getFullClassName() + ": ";
	}

	public String getFullClassName() {
		return this.getClass().getName();
	}

	public String getClassName() {
		String[] parts = this.getClass().getName().split("\\.");
		return parts[parts.length - 1];
	}
}
