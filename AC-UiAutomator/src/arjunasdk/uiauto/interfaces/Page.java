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

import java.util.Map;

import arjunasdk.uiauto.enums.UiAutomationContext;
import pvt.arjunasdk.uiauto.api.BaseUiDriver;
import pvt.arjunasdk.uiauto.api.CentralPageMap;
import pvt.arjunasdk.uiauto.api.appactions.BrowserActionHandler;
import pvt.arjunasdk.uiauto.api.appactions.ElementCreationHandler;
import pvt.arjunasdk.uiauto.api.appactions.ImageComparator;
import pvt.arjunasdk.uiauto.api.appactions.NativeWindowActionHandler;

public interface Page extends BaseUiDriver, ElementCreationHandler, 
ImageComparator, NativeWindowActionHandler, BrowserActionHandler{
	CentralPageMap getUiMap();
	
	String getName();
	void setName(String name);
	
	void populate(PageMapper mapper) throws Exception;
	void addElement(String uiElementName, Map<String, String> elemMap) throws Exception;
//	void processUiProperties(String elementName, Map<String,String> properties) throws Exception;
	
//	String getImagesDirectory();
	
	UiAutomationContext getContext() throws Exception;
	boolean isAutomatorPresent() throws Exception;
	
	Page getParent() throws Exception;;
	void setParent(Page page) throws Exception;
	
	String getLabel() throws Exception;
	void setLabel(String label)  throws Exception;
	
	//IDefaultElement declareElement(IElementMetaData elementMetaData, ElementLoaderType loaderType) throws Exception;
	UiElement element(String name) throws Exception;
	UiDriver getUiDriver() throws Exception;
	
	void setUiDriver(UiDriver automator) throws Exception;
	void setContext(UiAutomationContext context) throws Exception;
	
	public void switchToWebContext() throws Exception;
	public void switchToNativeContext() throws Exception;

	void processElementProperties(String elementName, Map<String, String> properties) throws Exception;
//	void processElementPropertiesForLabel(String uiName, String elementName, Map<String, String> properties)
//			throws Exception;
}
