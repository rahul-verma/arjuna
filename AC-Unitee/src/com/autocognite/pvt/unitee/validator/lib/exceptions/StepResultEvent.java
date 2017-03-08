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
package com.autocognite.pvt.unitee.validator.lib.exceptions;

import com.autocognite.pvt.arjuna.interfaces.Check;
import com.autocognite.pvt.batteries.exceptions.ArjunaException;

public class StepResultEvent extends ArjunaException {
	/**
	 * 
	 */
	private static final long serialVersionUID = -3029394135447054950L;
	private Check check = null;
	    /**
	 * 
	 */
	
	//Constructor that accepts a message
	public StepResultEvent(Check check){
		super(check.getExceptionMessage());
		this.check = check;
	}
	
	public String getMethodName(){
		return check.getSourceMethodName();
	}
	
	public String getClassName(){
		return check.getSourceClassName();
	}
	
	public String getPurpose(){
		return check.getPurpose();
	}

	public String getBenchmark() {
		return check.getBenchmark();
	}

	public String getActualObservation() {
		return check.getActualObservation();
	}

	public String getCheckText() {
		return check.getText();
	}
}
