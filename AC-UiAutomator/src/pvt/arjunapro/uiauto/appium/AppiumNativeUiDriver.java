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
package pvt.arjunapro.uiauto.appium;

import pvt.appium.lib.base.AbstractAppiumUiDriver;
import pvt.arjunasdk.uiauto.enums.MobileNativeIdentifyBy;
import pvt.batteries.config.Batteries;
import pvt.uiautomator.lib.config.UiAutomatorPropertyType;

public class AppiumNativeUiDriver extends AbstractAppiumUiDriver {
	
	public AppiumNativeUiDriver() throws Exception{
		super(Batteries.value(UiAutomatorPropertyType.APP_MOBILE_PATH).asString());
	}
	
	public AppiumNativeUiDriver(String appPath) throws Exception{
		super(appPath);
	}
	
	protected boolean checkNullIdentifier(String identifier, String idValue) throws Exception{
		return MobileNativeIdentifyBy.valueOf(identifier) == null;
	}

	@Override
	public String getName() {
		return "Appium Native UiDriver";
	}
	
	@Override
	public void switchToNativeContext() throws Exception{
		// do nothing
	}

}
