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
package com.autocognite.pvt.uiautomator.lib;

import java.util.List;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.uiauto.enums.UiAutomationContext;
import com.autocognite.arjuna.uiauto.interfaces.UiElement;
import com.autocognite.pvt.uiautomator.UiAutomator;
import com.autocognite.pvt.uiautomator.api.ElementMetaData;

public class DefaultUiElement  extends DefaultACElement implements UiElement{
	private UiAutomationContext idType = null;

	public DefaultUiElement(ElementMetaData metaData) {
		super(metaData);
	}

	@Override
	public Object throwUnsupportedActionException(String action) throws Exception {
		return throwUnsupportedException(action);		
	}

	@Override
	public Object throwNegativeIndexException(String action) throws Exception {
		return throwExceptionFromMediator(UiAutomator.problem.ELEMENT_NEGATIVE_INEDX, action);
	}

	@Override
	public Object throwZeroOrdinalException(String action) throws Exception {
		return throwExceptionFromMediator(UiAutomator.problem.ELEMENT_ZERO_ORDINAL, action);
	}

	@Override
	public Object throwEmptyElementQueueException(String action) throws Exception {
		return throwExceptionFromMediator(UiAutomator.problem.ELEMENT_EMPTY_QUEUE, action);
	}

	@Override
	public Object throwUnsupportedSelectActionException(String action) throws Exception {
		return throwUnsupportedActionExceptionFromMediator(UiAutomator.problem.ELEMENT_UNSUPPORTED_SELECT_ACTION, action);
	}

	@Override
	public void hoverAndClickElement(UiElement uiElement) throws Exception {
		try{
			this.getMediator().hoverAndClickElement(uiElement);} catch (Exception e){
			throwElementException(
					e,
					UiAutomator.problem.ACTION_MULTIELEMENT_FAILURE,
					"hoverAndClickElement",
					RunConfig.getProblemText(
							UiAutomator.problem.ACTION_MULTIELEMENT_FAILURE,
							this.getMediator().getAutomatorName(),
							"hover on",
							this.getElementNameFillerForException(),
							this.getMetaData().getAllProperties().toString(),
							"click on",
							this.getElementNameFillerForException(uiElement),
							uiElement.getMetaData().getAllProperties().toString()	
							)
					);
		}
	}

	@Override
	public void rightClickAndClickElement(UiElement uiElement) throws Exception {
		try{
			this.getMediator().rightClickAndClickElement(uiElement);} catch (Exception e){
			throwElementException(
					e,
					UiAutomator.problem.ACTION_MULTIELEMENT_FAILURE,
					"rightClickAndClicElement",
					RunConfig.getProblemText(
							UiAutomator.problem.ACTION_MULTIELEMENT_FAILURE,
							this.getMediator().getAutomatorName(),
							"right click on",
							this.getElementNameFillerForException(),
							this.getMetaData().getAllProperties().toString(),
							"click on",
							this.getElementNameFillerForException(uiElement),
							uiElement.getMetaData().getAllProperties().toString()	
							)
					);
		}
	}

	public UiElement identify() throws Exception {
		try {
			this.getMediator().identify();
			return this;
		} catch (Exception e){
			return (UiElement) throwElementIdentificationException(e, "identify", "identify element");
		}
	}

	@Override
	public UiElement identifyAll() throws Exception {
		try {
			this.getMediator().identifyAll();
			return this;
		} catch (Exception e){
			return (UiElement) throwElementIdentificationException(e, "identify", "identify all elements");
		}
	}

	@Override
	public UiElement getInstanceAtIndex(int index) throws Exception {
		try {
			return this.getMediator().getInstanceAtIndex(index);
		} catch (Exception e){
			return (UiElement) throwElementGetInstanceException(e, "getInstanceAtIndex", String.format("get instance at index %d", index));
		}
	}

	@Override
	public UiElement get(int index) throws Exception {
		try {
			return this.getMediator().get(index);
		} catch (Exception e){
			return (UiElement) throwElementGetInstanceException(e, "get (index)", String.format("get instance at index %d", index));
		}
	}

	@Override
	public UiElement get() throws Exception {
		try {
			return this.getMediator().get();
		} catch (Exception e){
			return (UiElement) throwElementGetInstanceException(e, "get", String.format("get instance at index %d", 0));
		}
	}

	@Override
	public UiElement getInstanceAtOrdinal(int ordinal) throws Exception {
		try {
			return this.getMediator().getInstanceAtOrdinal(ordinal);
		} catch (Exception e){
			return (UiElement) throwElementGetInstanceException(e, "getInstanceAtOrdinal", String.format("get instance at ordinal %d", ordinal));
		}
	}

	@Override
	public UiElement getRandomInstance() throws Exception {
		try {
			return this.getMediator().getRandomInstance();
		} catch (Exception e){
			return (UiElement) throwElementGetInstanceException(e, "getRandomInstance", "get random instance");
		}
	}

	@Override
	public UiElement getFirstInstance() throws Exception {
		try {
			return this.getMediator().getFirstInstance();
		} catch (Exception e){
			return (UiElement) throwElementGetInstanceException(e, "getFirstInstance", "get first instance");
		}
	}

	@Override
	public UiElement getLastInstance() throws Exception {
		try {
			return this.getMediator().getLastInstance();
		} catch (Exception e){
			return (UiElement) throwElementGetInstanceException(e, "getLastInstance", "get last instance");
		}
	}

	@Override
	public List<UiElement> getAllInstances() throws Exception {
		try {
			return this.getMediator().getAllInstances();
		} catch (Exception e){
			return (List<UiElement>) throwElementGetInstanceException(e, "getAllInstances", "get all instances");
		}
	}

	@Override
	public UiElement getInstanceByText(String text) throws Exception {
		try {
			return this.getMediator().getInstanceByText(text);
		} catch (Exception e){
			return (UiElement) throwElementGetInstanceException(e, "getInstanceByText", String.format("get instance by text '%s'", text));
		}
	}

	@Override
	public UiElement getInstanceByTextContent(String textContent) throws Exception {
		try {
			return this.getMediator().getInstanceByTextContent(textContent);
		} catch (Exception e){
			return (UiElement) throwElementGetInstanceException(e, "getInstanceByTextContent", String.format("get instance by text content '%s'", textContent));
		}
	}

}
