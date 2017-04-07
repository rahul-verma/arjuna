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
package pvt.unitee.reporter.lib.reportable;

import org.apache.log4j.Logger;

import com.arjunapro.testauto.console.Console;

import pvt.batteries.config.Batteries;
import pvt.batteries.utils.ExceptionBatteries;
import pvt.unitee.reporter.lib.event.Event;
import pvt.unitee.reporter.lib.event.EventBuilder;

public class ReportableFactory {
	private static Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	
//	private static FixtureResult getFixtureResult(TestVariables testVars, TestClassFixtureType type, Throwable e) throws Exception{
//		FixtureResultBuilder builder = new FixtureResultBuilder();
//		return builder
//		.testVariables(testVars)
//		.message(e.getMessage())
//		.trace(ExceptionBatteries.getStackTraceAsString(e))
//		.type(type)
//		.result(FixtureResultType.ERROR)
//		.build();
//	}
	
	private static Event getErrorAlert(Throwable e) throws Exception{
		EventBuilder builder = new EventBuilder();
		builder.message(e.getMessage());
		builder.trace(ExceptionBatteries.getStackTraceAsString(e));
		builder.suceedeed(false);
		return builder.build();
	}
	
	public static Event createAlert(String component, String text) throws Exception{
		EventBuilder builder = new EventBuilder();
		builder.component(component);
		builder.activity(text);
		builder.suceedeed(false);
		return builder.build();
	}
	
	public static Event createAlertForException(Throwable e) throws Exception {
		try{
			throw e;
		}
		catch (java.lang.reflect.InvocationTargetException g) {
			logger.debug("Java Error in Reflected Method.");
			logger.debug(g.getMessage());
			if (g.getTargetException().getCause() == null){
				return getErrorAlert(g.getTargetException());
			} else {
				return getErrorAlert(g.getTargetException().getCause());
			}
		} catch (Throwable h) {
			logger.debug("Java Error");
			Console.displayExceptionBlock(h);
			return getErrorAlert(h);
		}
	}
	
}
