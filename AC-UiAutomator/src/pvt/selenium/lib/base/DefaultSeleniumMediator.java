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
package pvt.selenium.lib.base;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;

import arjunasdk.uiauto.interfaces.SeleniumUiDriver;
import arjunasdk.uiauto.interfaces.UiElement;
import pvt.arjunasdk.uiauto.api.ElementMetaData;
import pvt.arjunasdk.uiauto.enums.ElementLoaderType;
import pvt.arjunasdk.uiauto.enums.UiElementType;
import pvt.selenium.api.WDMediator;
import pvt.uiautomator.lib.base.BaseUiMediator;

public class DefaultSeleniumMediator extends BaseUiMediator implements WDMediator{
	
	private SeleniumUiDriver uiDriver = null;
	private WebElement toolElement = null;
	private Select selectElement = null;
	private List<WebElement> toolElements = null;
	private ArrayList<By> toolFindByQueue = null;
	
	public DefaultSeleniumMediator(SeleniumUiDriver uiDriver, UiElement uiElement){
		super(uiElement);
		this.setSeleniumUiDriver(uiDriver);
	}

	@Override
	public SeleniumUiDriver getSeleniumUiDriver() {
		return uiDriver;
	}

	@Override
	public void setSeleniumUiDriver(SeleniumUiDriver uiDriver) {
		this.uiDriver = uiDriver;
	}

	@Override
	public WebElement getToolElement() throws Exception {
		return toolElement;
	}

	@Override
	public WebElement getToolElementWithRetry() throws Exception {
		WebElement element = this.getToolElement();
		if (element == null){
			identify();
			return this.getToolElement();
		} else {
			return element;
		}
	}

	@Override
	public List<WebElement> getToolElements() {
		return toolElements;
	}

	@Override
	public Select getSelectElement() {
		return selectElement;
	}

	@Override
	public Select getSelectElementWithRetry() throws Exception {
		Select element = this.getSelectElement();
		if (element == null){
			identify();
			return this.getSelectElement();
		} else {
			return element;
		}
	}

	@Override
	public void setToolElement(WebElement toolElement) {
		this.toolElement = toolElement;
	}

	@Override
	public void setToolElements(List<WebElement> elements) {
		this.toolElements = elements;
	}

	@Override
	public void setRawToolElement(Object toolElementObject) throws Exception {
		setToolElement((WebElement) toolElementObject);
	}

	@Override
	public void setRawToolElements(Object toolElementsObject) {
		setToolElements((List<WebElement>) toolElementsObject);
	}

	@Override
	public void setSelectElement(Select selectElement) {
		this.selectElement = selectElement;
	}

	@Override
	public ArrayList<By> getToolFindersQueue() {
		return toolFindByQueue;		
	}

	@Override
	public ArrayList<By> getToolFindersQueueObject() {
		return getToolFindersQueue();		
	}

	@Override
	public void setFindersQueue(ArrayList<By> findByQueue) {
		this.toolFindByQueue = findByQueue;
	}

	@Override
	public boolean isCompositeElementIdentified() throws Exception {
		if (!this.isComposite()){
			return false;
		} else {
			return ((this.getToolElements() != null) && (this.getToolElements().size() > 0));
		}
	}

	@Override
	public boolean isSingularElementIdentified() throws Exception {
		if (this.getElementType() == UiElementType.DROPDOWN){
			return this.getSelectElement() != null;
		} else {
			return this.getToolElement() != null;
		}
	}

	@Override
	public int getElementCountForCompositeElement() throws Exception {
		if (isCompositeElementIdentified()){
			return this.getToolElements().size();
		} else {
			return 0;
		}
	}

	@Override
	public UiElement getUiElementWrapperForToolElement(WebElement toolElement) throws Exception {
		return getElementWrapper(this.getUiElement().getMetaData(), toolElement, this.getUiElement().getLoaderType());
	}

	@Override
	public UiElement getElementWrapper(ElementMetaData elementMetaData, WebElement toolElement, ElementLoaderType loaderType) throws Exception {
		UiElement childUiElement = this.getSeleniumUiDriver().declareElement(elementMetaData);
	
		// Set properties
		childUiElement.setName(this.getUiElement().getName() + " (instance)");
		//childUiElement.setMetaData(this.getUiElement().getMetaData()); // is set as a part of element construction
		childUiElement.setCompositePageName(this.getUiElement().getCompositePageName());
		childUiElement.setPageLabel(this.getUiElement().getPageLabel());
		setElementForChildUiElement(childUiElement, toolElement);
		return childUiElement;
	}

	@Override
	public void setElementForUiElement(WebElement toolElement) throws Exception {
		this.getUiElement().setElement(toolElement);
		this.getUiElement().switchOffCompositeFlag();
		this.setComposite(false);
		this.setToolElement(toolElement);
		decorateSingleUiElement(this.getUiElement(), toolElement);	
	}

	@Override
	public void setElementsForUiElement(List<WebElement> toolElements) throws Exception {
		this.getUiElement().setElements(toolElements);
		this.getUiElement().switchOnCompositeFlag();
		this.setComposite(true);
		this.setToolElements(toolElements);
	}

	@Override
	public void setElementForChildUiElement(UiElement childUiElement, WebElement toolElement) throws Exception {
		childUiElement.setElement(toolElement);
		childUiElement.switchOffCompositeFlag();
		childUiElement.getMediator().setRawToolElement(toolElement);
		decorateSingleUiElement(childUiElement, toolElement);	
	}

	@Override
	public void setElementsForChildUiElement(UiElement childUiElement, List<WebElement> toolElements) throws Exception {
		childUiElement.setElements(toolElements);
		childUiElement.switchOnCompositeFlag();
		childUiElement.getMediator().setRawToolElements(toolElements);
	}

	@Override
	public void decorateSingleUiElement(UiElement uiElement, WebElement toolElement) throws Exception {
		SeleniumUiDriver automator = getSeleniumUiDriver();
		switch (automator.getElementType(toolElement)){
		case DROPDOWN: 
			Select select = automator.convertToSelectElement(toolElement);
			uiElement.setElement(select);
			uiElement.setType(UiElementType.DROPDOWN);
			this.setSelectElement(select);
			this.setElementType(UiElementType.DROPDOWN);
			break;
		case RADIO:
			List<WebElement> elements  = null;
			for (By by: getToolFindersQueue()){
				try{
					elements = automator.findElements(by);
					break;
				} catch (Exception e){
					//Do nothing
				}
			}
			if (elements == null){
				throw new Exception("Not able to find radio elements.");
			}
			uiElement.setElements(elements);
			uiElement.setType(UiElementType.RADIO);
			this.setToolElements(elements);
			this.setElementType(UiElementType.RADIO);
			break;
		default: uiElement.setType(UiElementType.GENERIC); this.setElementType(UiElementType.GENERIC);
		}		
	}

	@Override
	public void identify() throws Exception {
		SeleniumUiDriver automator = getSeleniumUiDriver();
		WebElement wdElement  = null;
		for (By by: getToolFindersQueue()){
			try{
				wdElement = automator.findElement(by);
				break;
			} catch (Exception e){
				//Do nothing
			}
		}
		if (wdElement == null){
			throw new Exception("Element Identification failed.");
		}
		setElementForUiElement(wdElement);
	}

	@Override
	public void identifyAll() throws Exception {
		SeleniumUiDriver automator = getSeleniumUiDriver();
		List<WebElement> wdElements  = null;
		for (By by: getToolFindersQueue()){
			try{
				wdElements = automator.findElements(by);
				break;
			} catch (Exception e){
				//Do nothing
			}
		}
		if (wdElements == null){
			throw new Exception("Multiple Element identification failed.");
		}
		setElementsForUiElement(wdElements);
	}

	@Override
	public void identifyAtIndex(int index) throws Exception {
		this.prepareIndexIndetification(index);
		this.setElementForUiElement(this.getToolElements().get(index));
	}

	@Override
	public void assignElementAtIndexFromMatches(int index) throws Exception {
		this.setElementForUiElement(this.getToolElements().get(index));
	}

	@Override
	public UiElement getInstanceAtIndex(int index) throws Exception {
		identifyAllIfNull();
		WebElement toolElement = this.getToolElements().get(index);
		return this.getUiElementWrapperForToolElement(toolElement);
	}

	@Override
	public UiElement getInstanceByText(String text) throws Exception {
		identifyAllIfNull();
		for (WebElement element: this.getToolElements()){
			if (element.getText().equals(text)){
				return this.getUiElementWrapperForToolElement(element);
			}
		}
		throw new Exception("None of the element instances has the specified text.");
	}

	@Override
	public UiElement getInstanceByTextContent(String text) throws Exception {
		identifyAllIfNull();
		for (WebElement element: this.getToolElements()){
			if (element.getText().contains(text)){
				return this.getUiElementWrapperForToolElement(element);
			}
		}
		throw new Exception("None of the element instances has the specified text content.");
	}

	@Override
	public List<UiElement> getAllInstances() throws Exception {
		identifyAllIfNull();
		List<UiElement> uiElements = new ArrayList<UiElement>();
		for (WebElement toolElement: this.getToolElements()){
			uiElements.add(this.getUiElementWrapperForToolElement(toolElement));
		}
		return uiElements;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#focus()
	 */
	@Override
	public void focus() throws Exception {
		getSeleniumUiDriver().focus(this.getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#enterText(java.lang.String)
	 */
	@Override
	public void enterText(String text) throws Exception {
		getSeleniumUiDriver().enterText(this.getToolElementWithRetry(), text);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#setText(java.lang.String)
	 */
	@Override
	public void setText(String text) throws Exception {
		getSeleniumUiDriver().setText(this.getToolElementWithRetry(), text);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#clearText()
	 */
	@Override
	public void clearText() throws Exception {
		getSeleniumUiDriver().clearText(this.getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#switchToFrame()
	 */
	@Override
	public void switchToFrame() throws Exception{
		getSeleniumUiDriver().switchToFrame(getToolElementWithRetry());
	}
	
	/* (non-Javadoc)
	 * @see  com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#isPresent()
	 */
	@Override
	public boolean isPresent() throws Exception {
		boolean present = false;
		SeleniumUiDriver automator = getSeleniumUiDriver();
		for(By by: this.getToolFindersQueue()){
			try{
				present = automator.isElementPresent(by);
				if (present) break;
			} catch (Exception e){
				// Do nothing
			}
		}

		return present;
	}
	
	@Override
	public boolean isAbsent() throws Exception {
		boolean present = false;
		SeleniumUiDriver automator = getSeleniumUiDriver();
		for(By by: this.getToolFindersQueue()){
			try{
				present = automator.isElementAbsent(by);
				if (present) break;
			} catch (Exception e){
				// Do nothing
			}
		}

		return present;
	}
	
	@Override
	public boolean isVisible() throws Exception {
		boolean present = false;
		SeleniumUiDriver automator = getSeleniumUiDriver();
		for(By by: this.getToolFindersQueue()){
			try{
				present = automator.isElementVisible(by);
				if (present) break;
			} catch (Exception e){
				// Do nothing
			}
		}

		return present;
	}

	@Override
	public boolean isInvisible() throws Exception {
		boolean present = false;
		SeleniumUiDriver automator = getSeleniumUiDriver();
		for(By by: this.getToolFindersQueue()){
			try{
				present = automator.isElementInvisible(by);
				if (present) break;
			} catch (Exception e){
				// Do nothing
			}
		}

		return present;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#click()
	 */
	@Override
	public void click() throws Exception {
		getSeleniumUiDriver().click(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#waitForPresence()
	 */
	@Override
	public void waitForPresence() throws Exception {
		SeleniumUiDriver automator = getSeleniumUiDriver();
		for(By by: this.getToolFindersQueue()){
			try{
				automator.waitForElementPresence(by);
				return;
			} catch (Exception e){
				// Do nothing
			}
		}
		throw new Exception("Not able to establish element presence after polling for it.");
	}
	
	@Override
	public void waitForAbsence() throws Exception {
		try{
			waitForPresence();
			throw new Exception("Not able to establish element absence after polling for it.");
		} catch (Exception e){
			// Element is absent as expected. Do nothing.
		}		
	}
	
	@Override
	public void waitForVisibility() throws Exception {
		SeleniumUiDriver automator = getSeleniumUiDriver();
		for(By by: this.getToolFindersQueue()){
			try{
				automator.waitForElementVisibility(by);
				return;
			} catch (Exception e){
				// Do nothing
			}
		}
		throw new Exception("Not able to establish element presence after polling for it.");
	}
	
	@Override
	public void waitForInvisibility() throws Exception {
		SeleniumUiDriver automator = getSeleniumUiDriver();
		for(By by: this.getToolFindersQueue()){
			try{
				automator.waitForElementInvisibility(by);
				return;
			} catch (Exception e){
				// Do nothing
			}
		}
		throw new Exception("Not able to establish element presence after polling for it.");
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#check()
	 */
	@Override
	public void check() throws Exception {
		getSeleniumUiDriver().check(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#uncheck()
	 */
	@Override
	public void uncheck() throws Exception {
		getSeleniumUiDriver().uncheck(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#toggle()
	 */
	@Override
	public void toggle() throws Exception {
		getSeleniumUiDriver().toggle(getToolElementWithRetry());
	}

	// Property API
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#getText()
	 */
	@Override
	public String getText() throws Exception {
		return getSeleniumUiDriver().getText(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#getValue()
	 */
	@Override
	public String getValue() throws Exception {
		return getSeleniumUiDriver().getValue(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#getAttribute(java.lang.String)
	 */
	@Override
	public String getAttribute(String attr) throws Exception {
		return getSeleniumUiDriver().getAttribute(getToolElementWithRetry(), attr);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#hover()
	 */
	@Override
	public void hover() throws Exception {
		getSeleniumUiDriver().hover(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#hoverAndClick()
	 */
	@Override
	public void hoverAndClick() throws Exception {
		getSeleniumUiDriver().hoverAndClick(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#rightClick()
	 */
	@Override
	public void rightClick() throws Exception {
		getSeleniumUiDriver().rightClick(getToolElementWithRetry());
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#getWaitTime()
	 */
	@Override
	public int getWaitTime() throws Exception {
		return getSeleniumUiDriver().getWaitTime();
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#takeScreenshot()
	 */
	@Override
	public File takeScreenshot() throws Exception{
		return getSeleniumUiDriver().takeScreenshot();
	}

	/*
	 * Selection API
	 */

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#selectDropDownLabel(java.lang.String)
	 */
	@Override
	public void selectDropDownLabel(String label) throws Exception{
		getSeleniumUiDriver().selectDropDownLabel(this.getSelectElementWithRetry(), label);		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#selectRadioLabel(java.lang.String)
	 */
	@Override
	public void selectRadioLabel(String label) throws Exception{
		WebElement element = getSeleniumUiDriver().chooseElementBasedOnParentText(this.getToolElements(), label);
		getSeleniumUiDriver().clickIfNotSelected(element);		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#selectDropDownValue(java.lang.String)
	 */
	@Override
	public void selectDropDownValue(String value) throws Exception{
		getSeleniumUiDriver().selectDropDownValue(this.getSelectElementWithRetry(), value);		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#selectRadioValue(java.lang.String)
	 */
	@Override
	public void selectRadioValue(String value) throws Exception{
		WebElement element = getSeleniumUiDriver().chooseElementBasedOnValue(this.getToolElements(), value);
		getSeleniumUiDriver().clickIfNotSelected(element);		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#selectDropDownOptionAtIndex(int)
	 */
	@Override
	public void selectDropDownOptionAtIndex(int index) throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		getSeleniumUiDriver().selectDropDownOptionAtIndex(selectControl, index);		
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#selectRadioOptionAtIndex(int)
	 */
	@Override
	public void selectRadioOptionAtIndex(int index) throws Exception{
		getSeleniumUiDriver().clickIfNotSelected(this.getToolElements().get(index));		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#isDropDownLabelSelected(java.lang.String)
	 */
	@Override
	public boolean isDropDownLabelSelected(String label) throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getSeleniumUiDriver().isDropDownSelectedText(selectControl, label);		
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#isRadioLabelSelected(java.lang.String)
	 */
	@Override
	public boolean isRadioLabelSelected(String label) throws Exception{
		return getSeleniumUiDriver().isSelectedElementParentText(this.getToolElements(), label);		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#isDropDownValueSelected(java.lang.String)
	 */
	@Override
	public boolean isDropDownValueSelected(String value) throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getSeleniumUiDriver().isDropDownSelectedValue(selectControl, value);	
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#isRadioValueSelected(java.lang.String)
	 */
	@Override
	public boolean isRadioValueSelected(String value) throws Exception{
		return getSeleniumUiDriver().isSelectedValue(this.getToolElements(), value);	
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#isDropDownOptionSelectedAtIndex(int)
	 */
	@Override
	public boolean isDropDownOptionSelectedAtIndex(int index) throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getSeleniumUiDriver().isDropDownSelectedIndex(selectControl, index);		
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#isRadioOptionSelectedAtIndex(int)
	 */
	@Override
	public boolean isRadioOptionSelectedAtIndex(int index) throws Exception{
		return getSeleniumUiDriver().isSelectedIndex(this.getToolElements(), index);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#getDropDownLabels()
	 */
	@Override
	public ArrayList<String> getDropDownLabels() throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getSeleniumUiDriver().getDropDownOptionLabels(selectControl);		
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#getRadioLabels()
	 */
	@Override
	public ArrayList<String> getRadioLabels() throws Exception{
		return getSeleniumUiDriver().getRadioButtonLabels(this.getToolElements());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#getDropDownValues()
	 */
	@Override
	public ArrayList<String> getDropDownValues() throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getSeleniumUiDriver().getDropDownOptionValues(selectControl);		
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#getRadioValues()
	 */
	@Override
	public ArrayList<String> getRadioValues() throws Exception{
		return getSeleniumUiDriver().getRadioButtonValues(this.getToolElements());		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#getDropDownOptionCount()
	 */
	@Override
	public int getDropDownOptionCount() throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getSeleniumUiDriver().getDropDownOptionCount(selectControl);		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#getRadioOptionCount()
	 */
	@Override
	public int getRadioOptionCount() throws Exception{
		return getElementCountForCompositeElement();	
	}

	

	//========================================================================================
	/*
	 * APIs that are called by an Element either for lazy identification or repeated identification.
	 *
	 */

	

	/*
	 * Composite Controls
	 */

	

	/*
	 * Chain actions
	 */

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#hoverAndClickElement(com.autocognite.unitee.pvt.uiautomator.element.IDefaultElement)
	 */
	@Override
	public void hoverAndClickElement(UiElement uiElement) throws Exception{
		boolean success = false;
		SeleniumUiDriver automator = getSeleniumUiDriver();
		for (By by1: this.getToolFindersQueue()){
			for(By by2: (ArrayList<By>) uiElement.getMediator().getToolFindersQueueObject()){
				try{
					automator.hoverAndClick(by1, by2);
					success = true;
					break;
				} catch (Exception e){
					// do nothing
				}
			}
			
			// The inner break comes here. Break outer loop if success.
			if(success) break;
		}

		if (!success){
			throw new Exception("Hover and Click Element failed.");
		}

	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.webdriver.IWDMediator#rightClickAndClickElement(com.autocognite.unitee.pvt.uiautomator.element.IDefaultElement)
	 */
	@Override
	public void rightClickAndClickElement(UiElement uiElement) throws Exception {
		boolean success = false;
		SeleniumUiDriver automator = getSeleniumUiDriver();
		for (By by1: this.getToolFindersQueue()){
			for(By by2: (ArrayList<By>) uiElement.getMediator().getToolFindersQueueObject()){
				try{
					automator.rightClickAndClick(by1, by2);
					success = true;
					break;
				} catch (Exception e){
					// do nothing
				}
			}
			
			// The inner break comes here. Break outer loop if success.
			if(success) break;
		}

		if (!success){
			throw new Exception("Right click and Click Element failed.");
		}
	}

}
