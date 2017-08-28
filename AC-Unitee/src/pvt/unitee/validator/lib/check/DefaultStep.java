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
package pvt.unitee.validator.lib.check;

import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.interfaces.Step;
import unitee.exceptions.Error;
import unitee.exceptions.Failure;

public class DefaultStep implements Step{
	private String purpose = "NOT_SET";
	private String benchmark = "NOT_SET";
	private String actual = "NOT_SET";
	private String message = "NOT_SET";
	private String assertion = "NOT_SET";
	private boolean isFailed = false;
	private boolean isError = false;
	private String parentTestThreadName = null;
	
	
	public DefaultStep(){
		this.parentTestThreadName = Thread.currentThread().getName();
	}
	
	public DefaultStep(String parentThreadName){
		this.parentTestThreadName = parentThreadName;
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
		if ((purpose != null) && (purpose.length() > 25000)){
			this.purpose = "TEXT_EXCEEDS_25000CHARRS";
		} else {
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
		if ((benchmark != null) && (benchmark.length() > 25000)){
			this.benchmark = "BENCHMARK_EXCEEDS_25000CHARRS";
		} else {
			this.benchmark = benchmark;
		}
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
		if ((actual != null) && (actual.length() > 25000)){
			this.actual = "ACTUAL_EXCEEDS_25000CHARRS";
		} else {
			this.actual = actual;
		}
	}
	
	@Override
	public String getText() {
		return assertion;
	}
	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setText(java.lang.String)
	 */
	@Override
	public void setText(String assertion) {
		if ((assertion != null) && (assertion.length() > 25000)){
			this.assertion = "TEXT_EXCEEDS_25000CHARRS";
		} else {
			this.assertion = assertion;
		}
	}

	private boolean passed(){
		return ((!this.failed()) && (!this.erred()));
	}


	private boolean erred(){
		return this.isError;
	}
	
	private boolean failed(){
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

	@Override
	public void evaluate() throws Exception{
		if (failed()){
			throw new Failure(this);
		} else if (erred()){
			throw new Error(this);
		} else {
			ArjunaInternal.getGlobalState().getThreadState(parentTestThreadName).addStepSuccessForPassedStep(this);
		}
	}

	/* (non-Javadoc)
	 * @see com.autocognite.pvt.unitee.validator.lib.check.IC#setExceptionMessage(java.lang.String)
	 */
	@Override
	public void setExceptionMessage(String message) {
		if ((message != null) && (message.length() > 25000)){
			this.message = "MESSAGE_EXCEEDS_25000CHARRS";
		} else {
			this.message  = message;
		}
	}
}
