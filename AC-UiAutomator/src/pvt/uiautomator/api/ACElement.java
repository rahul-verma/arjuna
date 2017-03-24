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
package pvt.uiautomator.api;

import pvt.uiauto.enums.ElementLoaderType;
import pvt.uiauto.enums.UiElementType;
import pvt.uiautomator.api.actions.BasicActionHandler;

public interface ACElement extends BasicActionHandler{
	String getName();
	void setName(String name);
	String getCompositePageName();
	void setCompositePageName(String name);
	UiElementType getType();
	boolean isComposite();
//	HashMap<String,String> getRawMetaData();
	String property(String propName);
	String getProperty(String propName);
	void setProperty(String propName, String value);
	void switchOnCompositeFlag();
	void switchOffCompositeFlag();
	void setType(UiElementType type);
	
	void setElement(Object element);
	Object getElement();
	void setElements(Object elements);
	Object getElements();
	
	void reset() throws Exception ;
	
	UiMediator getMediator();
	void setMediator(UiMediator mediator) throws Exception;
	
	ElementMetaData getMetaData();
	void setMetaData(ElementMetaData map);
	
	void setLoaderType(ElementLoaderType type);
	ElementLoaderType getLoaderType();
	
	String getPageLabel();
	void setPageLabel(String label);
}
