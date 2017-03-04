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
package com.autocognite.arjuna.uiauto.interfaces;

import java.util.HashMap;

public interface App{
	
	String getName();
	void setName(String name);

	void addElement(String uiElementName, HashMap<String, String> elemMap) throws Exception;
	void addElement(String uiLabel, String uiElementName, HashMap<String, String> elemMap) throws Exception;

	void registerPage(String uiLabel, UiDriver uiDriver, String mapPath) throws Exception;
	void registerPage(String uiLabel, UiDriver uiDriver, PageMapper mapper) throws Exception;

	Page page(String name) throws Exception;
	
}
