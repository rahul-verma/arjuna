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
package pvt.arjunapro.uiauto.pageobject;

import java.util.HashMap;

import com.arjunapro.uiauto.interfaces.Page;
import com.arjunapro.uiauto.interfaces.UiDriver;

import pvt.arjunapro.uiauto.factories.PageMapperFactory;
import pvt.arjunapro.uiauto.interfaces.App;
import pvt.arjunapro.uiauto.interfaces.PageMapper;
import pvt.batteries.config.Batteries;
import pvt.batteries.exceptions.Problem;
import pvt.uiauto.enums.UiAutomationContext;
import pvt.uiautomator.UiAutomator;

public class BaseApp implements App{
	private String name = null;
	private HashMap<String, Page> pageMap = new HashMap<String, Page>();

	public BaseApp(String templateName){
		this.setName(templateName);
	}

	public void registerPage(String uiLabel, UiDriver uiDriver, String mapPath) throws Exception {
		if (uiDriver != null){
			Page ui = new BasePage(uiLabel, uiDriver);
			ui.populate(PageMapperFactory.getFileMapper(mapPath));
			getPageMap().put(uiLabel.toUpperCase(), ui); // to provide case insensitive access	
		} else {
			throwNullAutomatorException("registerUi", UiAutomationContext.GENERIC);
		}		
	}
	
	public void registerPage(String uiLabel, UiDriver uiDriver, PageMapper mapper) throws Exception {
		if (uiDriver != null){
			Page ui = new BasePage(uiLabel, uiDriver);
			ui.populate(mapper);
			this.getPageMap().put(uiLabel.toUpperCase(), ui); // to provide case insensitive access	
		} else {
			throwNullAutomatorException("registerUi", UiAutomationContext.GENERIC);
		}		
	}


	protected void throwNullAutomatorException(String method, UiAutomationContext context) throws Exception{
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
			this.getName(),
			method,
			UiAutomator.problem.COMPOSITE_PAGE_NULL_AUTOMATOR,
			Batteries.getProblemText(UiAutomator.problem.COMPOSITE_PAGE_NULL_AUTOMATOR, UiAutomator.getAutomationContextName(context) )
		);
	}
	
	protected Page throwUndefinedUiException(String method, String uiLabel) throws Exception{
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
			this.getName(),
			method,
			UiAutomator.problem.COMPOSITE_PAGE_NONEXISTING_LABEL,
			Batteries.getProblemText(UiAutomator.problem.COMPOSITE_PAGE_NONEXISTING_LABEL, uiLabel, this.getName())
		);
	}
	
	protected Page throwNullUiException(String method) throws Exception{
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
			this.getName(),
			method,
			UiAutomator.problem.COMPOSITE_PAGE_NULL_LABEL,
			Batteries.getProblemText(UiAutomator.problem.COMPOSITE_PAGE_NULL_LABEL, this.getName() )
		);
	}

	@Override
	public String getName() {
		return this.name;
	}

	@Override
	public void setName(String name) {
		this.name = name;
	}



	@Override
	public void addElement(String elementName, HashMap<String,String> elementProps) throws Exception {
		for (String name: getPageMap().keySet()){
			getPageMap().get(name.toUpperCase()).addElement(elementName, elementProps);
		}
	}

	@Override
	public void addElement(String uiLabel, String elementName, HashMap<String, String> elemMap) throws Exception {
		if (uiLabel == null){
			throwNullUiException("addElement");
		}
		
		if (getPageMap().containsKey(uiLabel.toUpperCase())){
			getPageMap().get(uiLabel.toUpperCase()).addElement(elementName, elemMap);
		} else{
			throwUndefinedUiException("addElement", uiLabel);
		}
	}
	
	public Page page(String uiName) throws Exception {
		if (uiName != null){
			if (getPageMap().containsKey(uiName.toUpperCase())){
				return getPageMap().get(uiName.toUpperCase());
			} else{
				return throwUndefinedUiException("ui", uiName);
			}
		} else {
			return throwNullUiException("ui");
		}
	}

	protected HashMap<String, Page> getPageMap() {
		return pageMap;
	}

	protected void setPageMap(HashMap<String, Page> pageMap) {
		this.pageMap = pageMap;
	}
	
}

//test