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
package com.autocognite.pvt.unitee.validator.lib.check;

import com.autocognite.pvt.arjuna.interfaces.Check;
import com.autocognite.pvt.unitee.validator.lib.exceptions.Error;
import com.autocognite.pvt.unitee.validator.lib.exceptions.Failure;

public class DefaultCheck implements Check {
	private String methodName = "NOT_SET";
	private String className = "NOT_SET";
	private String purpose = "NOT_SET";
	private String benchmark = "NOT_SET";
	private String actual = "NOT_SET";
	private String assertion = "NOT_SET";
	//private Throwable exception = null;
	private String message = "NOT_SET";
	private boolean isFailed = false;
	private boolean isError = false;
	
	public DefaultCheck(String className, String methodName){
		this.className = className;
		this.methodName = methodName;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#getSourceMethodName()
	 */
	@Override
	public String getSourceMethodName() {
		return methodName;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setSourceMethodName(java.lang.String)
	 */
	@Override
	public void setSourceMethodName(String methodName) {
		this.methodName = methodName;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#getSourceClassName()
	 */
	@Override
	public String getSourceClassName() {
		return className;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setSourceClassName(java.lang.String)
	 */
	@Override
	public void setSourceClassName(String className) {
		this.className = className;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#getPurpose()
	 */
	@Override
	public String getPurpose() {
		return purpose;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setPurpose(java.lang.String)
	 */
	@Override
	public void setPurpose(String purpose) {
		if (purpose != null){
			this.purpose = purpose;
		}
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#getBenchmark()
	 */
	@Override
	public String getBenchmark() {
		return benchmark;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setBenchmark(java.lang.String)
	 */
	@Override
	public void setBenchmark(String benchmark) {
		this.benchmark = benchmark;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#getActualObservation()
	 */
	@Override
	public String getActualObservation() {
		return actual;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setActualObservation(java.lang.String)
	 */
	@Override
	public void setActualObservation(String actual) {
		this.actual = actual;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#getText()
	 */
	@Override
	public String getText() {
		return assertion;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setText(java.lang.String)
	 */
	@Override
	public void setText(String assertion) {
		this.assertion = assertion;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#passed()
	 */
	@Override
	public boolean passed(){
		return ((!this.failed()) && (!this.erred()));
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#failed()
	 */
	@Override
	public boolean failed(){
		return this.isFailed;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setFailure()
	 */
	@Override
	public void setFailure(){
		this.isFailed = true;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#erred()
	 */
	@Override
	public boolean erred(){
		return this.isError;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setError()
	 */
	@Override
	public void setError(){
		this.isError = true;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#getExceptionMessage()
	 */
	@Override
	public String getExceptionMessage(){
		return this.message;
	}
	
//	public String getExceptionTraceAsString(){
//		if (passed()){
//			return "NOT_SET";
//		} else {
//			return ExceptionBatteries.getStackTraceAsString(this.exception);
//		}
//	}
	
//	public Throwable getException(){
//		return this.exception;
//	}
//
//	public void setException(Throwable e){
//		this.exception = e;
//	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#evaluate()
	 */
	@Override
	public void evaluate() throws Exception{
		if (failed()){
			throw new Failure(this);
		} else if (erred()){
			throw new Error(this);
		}
	}

	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setExceptionMessage(java.lang.String)
	 */
	@Override
	public void setExceptionMessage(String message) {
		this.message  = message;
	}
}
