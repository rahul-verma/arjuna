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
package com.autocognite.pvt.uiautomator.api.actions;

import java.util.List;

import com.autocognite.arjuna.uiauto.interfaces.UiElement;

public interface InstanceGetter {	
	// Get wrapped object from raw object, already identified ones
	UiElement getInstanceAtIndex(int index) throws Exception;
	UiElement get(int index) throws Exception;
	UiElement get() throws Exception;
	UiElement getInstanceAtOrdinal(int ordinal) throws Exception;
	UiElement getRandomInstance() throws Exception;
	UiElement getFirstInstance() throws Exception;
	UiElement getLastInstance() throws Exception;
	List<UiElement> getAllInstances() throws Exception;
	
	UiElement getInstanceByText(String text) throws Exception;
	UiElement getInstanceByTextContent(String text) throws Exception;
}
