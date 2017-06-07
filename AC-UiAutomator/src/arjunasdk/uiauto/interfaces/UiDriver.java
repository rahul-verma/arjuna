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
package arjunasdk.uiauto.interfaces;

import pvt.arjunasdk.uiauto.api.BaseUiDriver;
import pvt.arjunasdk.uiauto.api.ElementMetaData;
import pvt.arjunasdk.uiauto.api.appactions.BrowserActionHandler;
import pvt.arjunasdk.uiauto.api.appactions.ElementCreationHandler;
import pvt.arjunasdk.uiauto.api.appactions.ImageComparator;
import pvt.arjunasdk.uiauto.api.appactions.NativeWindowActionHandler;
import pvt.arjunasdk.uiauto.enums.ElementLoaderType;
import pvt.arjunasdk.uiauto.enums.UiAutomationContext;

public interface UiDriver extends BaseUiDriver, NativeWindowActionHandler, ElementCreationHandler, BrowserActionHandler, ImageComparator{
	
	UiElement declareElement(ElementMetaData elementMetaData) throws Exception;

	void setContext(UiAutomationContext screen);

	void switchToWebContext() throws Exception;
	void switchToNativeContext() throws Exception;
	ElementLoaderType getElementLoaderType() throws Exception;
	void setElementLoaderType(ElementLoaderType loaderType) throws Exception;
}
