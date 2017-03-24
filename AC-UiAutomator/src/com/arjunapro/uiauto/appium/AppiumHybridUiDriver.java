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
package com.arjunapro.uiauto.appium;

import pvt.appium.lib.base.AbstractAppiumUiDriver;
import pvt.batteries.config.Batteries;
import pvt.uiautomator.api.identify.enums.IdentifyBy;
import pvt.uiautomator.lib.config.UiAutomatorPropertyType;

public class AppiumHybridUiDriver extends AbstractAppiumUiDriver{
	
	public AppiumHybridUiDriver() throws Exception{
		super(Batteries.value(UiAutomatorPropertyType.APP_MOBILE_PATH).asString());
	}
	
	public AppiumHybridUiDriver(String appPath) throws Exception{
		super(appPath);
	}
	
	@Override
	public void switchToWebContext() throws Exception{
		getDriver().context("WEBVIEW");
	}
	
	@Override
	public void switchToNativeContext() throws Exception{
		getDriver().context("NATIVE");
	}
	
	protected boolean checkNullIdentifier(String identifier, String idValue) throws Exception{
		return IdentifyBy.valueOf(identifier) == null;
	}
	
	@Override
	public String getName() {
		return "Appium Hybrid UiDriver";
	}
}
