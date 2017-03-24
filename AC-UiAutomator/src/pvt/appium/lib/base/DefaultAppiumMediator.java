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
package pvt.appium.lib.base;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.Select;

import com.arjunapro.uiauto.interfaces.UiElement;

import io.appium.java_client.MobileElement;
import pvt.appium.api.AppiumMediator;
import pvt.arjunapro.uiauto.appium.AppiumUiDriver;
import pvt.uiauto.enums.ElementLoaderType;
import pvt.uiauto.enums.UiElementType;
import pvt.uiautomator.api.ElementMetaData;
import pvt.uiautomator.lib.base.BaseUiMediator;

public class DefaultAppiumMediator extends BaseUiMediator implements AppiumMediator {

	private AppiumUiDriver uiDriver = null;
	public MobileElement toolElement = null;
	private Select selectElement = null;
	private List<MobileElement> toolElements = null;
	private ArrayList<By> toolFindByQueue = null;
	
	public DefaultAppiumMediator(UiElement uiElement) {
		super(uiElement);
	}
	
	public DefaultAppiumMediator(AppiumUiDriver uiDriver, UiElement uiElement) {
		this(uiElement);
		this.uiDriver = uiDriver;
		this.setAutomatorName(uiDriver.getName());
	}
	
	@Override
	public AppiumUiDriver getAppiumUiDriver() {
		return uiDriver;
	}

	@Override
	public MobileElement getToolElement() throws Exception {
		return toolElement;
	}

	@Override
	public MobileElement getToolElementWithRetry() throws Exception {
		MobileElement element = this.getToolElement();
		if (element == null){
			identify();
			return this.getToolElement();
		} else {
			return element;
		}
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
	public void setToolElement(MobileElement toolElement) {
		this.toolElement = toolElement;
	}

	@Override
	public void setToolElements(List<MobileElement> elements) {
		this.toolElements = elements;
	}

	@Override
	public List<MobileElement> getToolElements() {
		return toolElements;
	}

	@Override
	public void setRawToolElement(Object toolElementObject) {
		setToolElement((MobileElement) toolElementObject);
	}

	@Override
	public void setRawToolElements(Object toolElementsObject) {
		setToolElements((List<MobileElement>) toolElementsObject);
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
	public UiElement getUiElementWrapperForToolElement(MobileElement toolElement) throws Exception {
		return getElementWrapper(this.getUiElement().getMetaData(), toolElement, this.getUiElement().getLoaderType());	
	}

	@Override
	public UiElement getElementWrapper(ElementMetaData elementMetaData, MobileElement toolElement, ElementLoaderType elementLoaderType) throws Exception {
			UiElement childUiElement = getAppiumUiDriver().declareElement(elementMetaData);
			// Set properties
			childUiElement.setName(this.getUiElement().getName() + " (instance)");
	//		childUiElement.setMetaData(this.getUiElement().getMetaData());
			childUiElement.setCompositePageName(this.getUiElement().getCompositePageName());
			childUiElement.setPageLabel(this.getUiElement().getPageLabel());
			
			setElementForChildUiElement(childUiElement, toolElement);
			return childUiElement;
		}

	@Override
	public void setElementForUiElement(MobileElement toolElement) throws Exception {
		this.getUiElement().setElement(toolElement);
		this.getUiElement().switchOffCompositeFlag();
		this.setToolElement(toolElement);
		decorateSingleUiElement(this.getUiElement(), toolElement);		
	}

	@Override
	public void setElementsForUiElement(List<MobileElement> toolElements) throws Exception {
		this.getUiElement().setElements(toolElements);
		this.getUiElement().switchOnCompositeFlag();
		this.setToolElements(toolElements);
	}

	@Override
	public void setElementForChildUiElement(UiElement childUiElement, MobileElement toolElement) throws Exception {
		childUiElement.setElement(toolElement);
		childUiElement.switchOffCompositeFlag();
		childUiElement.getMediator().setRawToolElement(toolElement);
		decorateSingleUiElement(childUiElement, toolElement);	
	}

	@Override
	public void setElementsForChildUiElement(UiElement childUiElement, List<MobileElement> toolElements) throws Exception {
		childUiElement.setElements(toolElements);
		childUiElement.switchOnCompositeFlag();
		childUiElement.getMediator().setRawToolElements(toolElements);
	}

	@Override
	public void decorateSingleUiElement(UiElement uiElement, MobileElement toolElement) throws Exception {
		AppiumUiDriver automator = getAppiumUiDriver();
		switch (automator.getElementType(toolElement)){
		case DROPDOWN: 
			Select select = automator.convertToSelectElement(toolElement);
			uiElement.setElement(select);
			uiElement.setType(UiElementType.DROPDOWN);
			this.setSelectElement(select);
			this.setElementType(UiElementType.DROPDOWN);
			break;
		case RADIO:
			List<MobileElement> elements  = null;
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
		AppiumUiDriver automator = this.getAppiumUiDriver();
		MobileElement toolElement  = null;
		for (By by: getToolFindersQueue()){
			try{
				toolElement = automator.findElement(by);
				break;
			} catch (Exception e){
				//Do nothing
			}
		}
		if (toolElement == null){
			throw new Exception("Element Identification failed.");
		}
		setElementForUiElement(toolElement);
	}

	@Override
	public void identifyAll() throws Exception {
		AppiumUiDriver automator = this.getAppiumUiDriver();
		List<MobileElement> toolElements  = null;
		for (By by: getToolFindersQueue()){
			try{
				toolElements = automator.findElements(by);
				break;
			} catch (Exception e){
				//Do nothing
			}
		}
		if (toolElements == null){
			throw new Exception("Multiple Element identification failed.");
		}
		setElementsForUiElement(toolElements);
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
		MobileElement appiumElement = this.getToolElements().get(index);
		return this.getUiElementWrapperForToolElement(appiumElement);
	}

	@Override
	public UiElement getInstanceByText(String text) throws Exception {
		identifyAllIfNull();
		for (MobileElement element: this.getToolElements()){
			if (element.getText().equals(text)){
				return this.getUiElementWrapperForToolElement(element);
			}
		}
		throw new Exception("None of the element instances has the specified text.");
	}

	@Override
	public UiElement getInstanceByTextContent(String text) throws Exception {
		identifyAllIfNull();
		for (MobileElement element: this.getToolElements()){
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
		for (MobileElement appiumElement: this.getToolElements()){
			uiElements.add(this.getUiElementWrapperForToolElement(appiumElement));
		}
		return uiElements;
	}

	@Override
	public void setAppiumUiDriver(AppiumUiDriver automator) {
		this.uiDriver = automator;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#focus()
	 */
	@Override
	public void focus() throws Exception {
		getAppiumUiDriver().focus(this.getToolElementWithRetry());
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#enterText(java.lang.String)
	 */
	@Override
	public void enterText(String text) throws Exception {
		getAppiumUiDriver().enterText(this.getToolElementWithRetry(), text);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#setText(java.lang.String)
	 */
	@Override
	public void setText(String text) throws Exception {
		getAppiumUiDriver().setText(this.getToolElementWithRetry(), text);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#clearText()
	 */
	@Override
	public void clearText() throws Exception {
		getAppiumUiDriver().clearText(this.getToolElementWithRetry());
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#isPresent()
	 */
	@Override
	public boolean isPresent() throws Exception {
		boolean present = false;
		AppiumUiDriver automator = getAppiumUiDriver();
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
		AppiumUiDriver automator = getAppiumUiDriver();
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
		AppiumUiDriver automator = getAppiumUiDriver();
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
		AppiumUiDriver automator = getAppiumUiDriver();
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
	
	@Override
	public void waitForPresence() throws Exception {
		AppiumUiDriver automator = getAppiumUiDriver();
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
		AppiumUiDriver automator = getAppiumUiDriver();
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
		AppiumUiDriver automator = getAppiumUiDriver();
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
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#click()
	 */
	@Override
	public void click() throws Exception {
		getAppiumUiDriver().click(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#check()
	 */
	@Override
	public void check() throws Exception {
		getAppiumUiDriver().check(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#uncheck()
	 */
	@Override
	public void uncheck() throws Exception {
		getAppiumUiDriver().uncheck(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#toggle()
	 */
	@Override
	public void toggle() throws Exception {
		getAppiumUiDriver().toggle(getToolElementWithRetry());
	}

	// Property API
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#getText()
	 */
	@Override
	public String getText() throws Exception {
		return getAppiumUiDriver().getText(getToolElementWithRetry());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#getValue()
	 */
	@Override
	public String getValue() throws Exception {
		return getAppiumUiDriver().getValue(getToolElementWithRetry());
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#getAttribute(java.lang.String)
	 */
	@Override
	public String getAttribute(String attr) throws Exception {
		return getAppiumUiDriver().getAttribute(getToolElementWithRetry(), attr);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#getWaitTime()
	 */
	@Override
	public int getWaitTime() throws Exception {
		return getAppiumUiDriver().getWaitTime();
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#takeScreenshot()
	 */
	@Override
	public File takeScreenshot() throws Exception{
		return getAppiumUiDriver().takeScreenshot();
	}
	
	/*
	 * Selection API
	 */
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#selectDropDownLabel(java.lang.String)
	 */
	@Override
	public void selectDropDownLabel(String label) throws Exception{
		getAppiumUiDriver().selectDropDownLabel(this.getSelectElementWithRetry(), label);		
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#selectRadioLabel(java.lang.String)
	 */
	@Override
	public void selectRadioLabel(String label) throws Exception{
		MobileElement element = getAppiumUiDriver().chooseElementBasedOnParentText(this.getToolElements(), label);
		getAppiumUiDriver().clickIfNotSelected(element);		
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#selectDropDownValue(java.lang.String)
	 */
	@Override
	public void selectDropDownValue(String value) throws Exception{
		getAppiumUiDriver().selectDropDownValue(this.getSelectElementWithRetry(), value);		
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#selectRadioValue(java.lang.String)
	 */
	@Override
	public void selectRadioValue(String value) throws Exception{
		MobileElement element = getAppiumUiDriver().chooseElementBasedOnValue(this.getToolElements(), value);
		getAppiumUiDriver().clickIfNotSelected(element);		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#selectDropDownOptionAtIndex(int)
	 */
	@Override
	public void selectDropDownOptionAtIndex(int index) throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		getAppiumUiDriver().selectDropDownOptionAtIndex(selectControl, index);		
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#selectRadioOptionAtIndex(int)
	 */
	@Override
	public void selectRadioOptionAtIndex(int index) throws Exception{
		getAppiumUiDriver().clickIfNotSelected(this.getToolElements().get(index));		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#isDropDownLabelSelected(java.lang.String)
	 */
	@Override
	public boolean isDropDownLabelSelected(String label) throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getAppiumUiDriver().isDropDownSelectedText(selectControl, label);		
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#isRadioLabelSelected(java.lang.String)
	 */
	@Override
	public boolean isRadioLabelSelected(String label) throws Exception{
		return getAppiumUiDriver().isSelectedElementParentText(this.getToolElements(), label);		
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#isDropDownValueSelected(java.lang.String)
	 */
	@Override
	public boolean isDropDownValueSelected(String value) throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getAppiumUiDriver().isDropDownSelectedValue(selectControl, value);	
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#isRadioValueSelected(java.lang.String)
	 */
	@Override
	public boolean isRadioValueSelected(String value) throws Exception{
		return getAppiumUiDriver().isSelectedValue(this.getToolElements(), value);	
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#isDropDownOptionSelectedAtIndex(int)
	 */
	@Override
	public boolean isDropDownOptionSelectedAtIndex(int index) throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getAppiumUiDriver().isDropDownSelectedIndex(selectControl, index);		
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#isRadioOptionSelectedAtIndex(int)
	 */
	@Override
	public boolean isRadioOptionSelectedAtIndex(int index) throws Exception{
		return getAppiumUiDriver().isSelectedIndex(this.getToolElements(), index);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#getDropDownLabels()
	 */
	@Override
	public ArrayList<String> getDropDownLabels() throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getAppiumUiDriver().getDropDownOptionLabels(selectControl);		
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#getRadioLabels()
	 */
	@Override
	public ArrayList<String> getRadioLabels() throws Exception{
		return getAppiumUiDriver().getRadioButtonLabels(this.getToolElements());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#getDropDownValues()
	 */
	@Override
	public ArrayList<String> getDropDownValues() throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getAppiumUiDriver().getDropDownOptionValues(selectControl);		
	}
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#getRadioValues()
	 */
	@Override
	public ArrayList<String> getRadioValues() throws Exception{
		return getAppiumUiDriver().getRadioButtonValues(this.getToolElements());		
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#getDropDownOptionCount()
	 */
	@Override
	public int getDropDownOptionCount() throws Exception{
		Select selectControl = this.getSelectElementWithRetry();
		return getAppiumUiDriver().getDropDownOptionCount(selectControl);		
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.appium.IAppiumMediator#getRadioOptionCount()
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
}
