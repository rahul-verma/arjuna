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
package com.arjunapro.uiauto.factories;

import com.arjunapro.uiauto.appium.AppiumHybridUiDriver;
import com.arjunapro.uiauto.appium.AppiumNativeUiDriver;
import com.arjunapro.uiauto.appium.AppiumWebUiDriver;
import com.arjunapro.uiauto.enums.UiAutomationContext;
import com.arjunapro.uiauto.interfaces.UiDriver;
import com.arjunapro.uiauto.selenium.SeleniumWebUiDriver;
import com.arjunapro.uiauto.sikuli.SikuliScreenUiDriver;

import pvt.batteries.config.Batteries;
import pvt.batteries.exceptions.Problem;
import pvt.uiautomator.UiAutomator;

public class UiDriverFactory {
	
	private static UiDriver getSelenium() throws Exception{
		return new SeleniumWebUiDriver();
	}
	
	private static UiDriver getAppiumWeb() throws Exception{
		return new AppiumWebUiDriver();
	}
	
	private static UiDriver getAppiumNative() throws Exception{
		return new AppiumNativeUiDriver();
	}
	
	private static UiDriver getAppiumNative(String appPath) throws Exception{
		return new AppiumNativeUiDriver(appPath);
	}
	
	private static UiDriver getAppiumHybrid() throws Exception{
		return new AppiumHybridUiDriver();
	}
	
	private static UiDriver getAppiumHybrid(String appPath) throws Exception{
		return new AppiumHybridUiDriver(appPath);
	}
	
	private static UiDriver getSikuli() throws Exception{
		return new SikuliScreenUiDriver();
	}
	
	public static UiDriver getWebUiDriver() throws Exception{
		return getSelenium();
	}
	
	public static UiDriver getMobileWebUiDriver() throws Exception{
		return getAppiumWeb();
	}

	public static UiDriver getMobileNativeUiDriver() throws Exception{
		return getAppiumNative();
	}
	
	public static UiDriver getMobileHybridUiDriver() throws Exception{
		return getAppiumHybrid();
	}
	
	public static UiDriver getMobileNativeUiDriver(String appPath) throws Exception{
		if (appPath == null){
			throw new Problem(
					Batteries.getComponentName("UI_AUTOMATOR"),
					"UiDriver Factory",
					"getMobileNativeAutomator",
					UiAutomator.problem.FACTORY_AUTOMATOR_MOBILE_NULL_APP_PATH,
					Batteries.getProblemText(UiAutomator.problem.FACTORY_AUTOMATOR_MOBILE_NULL_APP_PATH));
			}
		return getAppiumNative(appPath);
	}
	
	public static UiDriver getMobileHybridUiDriver(String appPath) throws Exception{
		if (appPath == null){
			throw new Problem(
					Batteries.getComponentName("UI_AUTOMATOR"),
					"UiDriver Factory",
					"getMobileNativeAutomator",
					UiAutomator.problem.FACTORY_AUTOMATOR_MOBILE_NULL_APP_PATH,
					Batteries.getProblemText(UiAutomator.problem.FACTORY_AUTOMATOR_MOBILE_NULL_APP_PATH));
			}
		return getAppiumHybrid(appPath);
	}
	
	public static UiDriver getScreenUiDriver() throws Exception{
		return getSikuli();
	}

	public static UiDriver getUiDriver(UiAutomationContext context) throws Exception {
		switch(context){
		case PC_WEB: return getSelenium();
		case MOBILE_WEB: return getAppiumWeb();
		case MOBILE_NATIVE: return getAppiumNative();
		case SCREEN: return getAppiumHybrid();
		default: 
			return throwUnsupportedAutomationContextException(context);
		}
	}
	
	public static UiDriver getUiDriver(UiAutomationContext context, String appPath) throws Exception {
		switch(context){
		case PC_WEB: throwAppPathFactoryMethodWronglyUsed(context);
		case MOBILE_WEB: throwAppPathFactoryMethodWronglyUsed(context);
		case MOBILE_NATIVE: return getAppiumHybrid(appPath);
		case SCREEN: throwAppPathFactoryMethodWronglyUsed(context);
		default: return throwUnsupportedAutomationContextException(context);
		}
	}
	
	public static UiDriver throwAppPathFactoryMethodWronglyUsed(UiAutomationContext context) throws Exception{
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
				"UiDriver Factory",
				"getUiDriver",
				UiAutomator.problem.FACTORY_METHOD_APPPATH_NOT_APPLICABLE,
				Batteries.getProblemText(
						UiAutomator.problem.FACTORY_METHOD_APPPATH_NOT_APPLICABLE,
						UiAutomator.getAutomationContextName(context))
			);		
	}
	
	public static UiDriver throwUnsupportedAutomationContextException(UiAutomationContext context) throws Exception{
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
				"UiDriver Factory",
				"getUiDriver",
				UiAutomator.problem.FACTORY_AUTOMATOR_UNSUPPORTED_CONTEXT,
				Batteries.getProblemText(
						UiAutomator.problem.FACTORY_AUTOMATOR_UNSUPPORTED_CONTEXT,
						UiAutomator.getAutomationContextName(context))
			);		
	}
}
