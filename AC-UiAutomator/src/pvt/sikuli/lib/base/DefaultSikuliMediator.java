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
package pvt.sikuli.lib.base;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.sikuli.script.Match;

import com.arjunapro.uiauto.enums.ElementLoaderType;
import com.arjunapro.uiauto.interfaces.UiElement;
import com.arjunapro.uiauto.sikuli.SikuliUiDriver;

import pvt.sikuli.api.SikuliMediator;
import pvt.uiautomator.api.ElementMetaData;
import pvt.uiautomator.lib.base.BaseUiScreenMediator;

public class DefaultSikuliMediator extends BaseUiScreenMediator implements SikuliMediator{

	private SikuliUiDriver uiDriver = null;
	private Match toolElement = null;
	private List<Match> toolElements = null;
	String imagePath = null;

	public DefaultSikuliMediator(SikuliUiDriver uiDriver, UiElement uiElement) throws Exception {
		super(uiElement);
		this.setSikuliUiDriver(uiDriver);
		this.setImagePath(uiElement.getImagePath());
	}

	@Override
	public String getImagePath() {
		return this.imagePath;
	}

	@Override
	public void setImagePath(String imagePath) throws Exception {
		this.imagePath = imagePath;
	}

	@Override
	public SikuliUiDriver getSikuliUiDriver() {
		return uiDriver;
	}

	@Override
	public void setSikuliUiDriver(SikuliUiDriver uiDriver) {
		this.uiDriver = uiDriver;
	}

	@Override
	public Match getToolElement() throws Exception {
		return this.toolElement;
	}

	@Override
	public Match getToolElementWithRetry() throws Exception {
		identifyIfNull();
		return this.getToolElement();
	}

	@Override
	public void setToolElement(Match element) {
		this.toolElement = element;
	}

	@Override
	public void setToolElements(List<Match> elements) {
		this.toolElements = elements;
	}

	@Override
	public List<Match> getToolElements() {
		return toolElements;
	}

	@Override
	public void setRawToolElement(Object toolElementObject) {
		setToolElement((Match) toolElementObject);
	}

	@Override
	public void setRawToolElements(Object toolElementsObject) {
		setToolElements((List<Match>) toolElementsObject);
	}

	@Override
	public Object getToolFindersQueueObject() {
		return null;
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
		return this.getToolElement() != null;
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
	public UiElement getUiElementWrapperForToolElement(Match toolElement) throws Exception {
		return getElementWrapper(this.getUiElement().getMetaData(), toolElement, this.getUiElement().getLoaderType());		
	}

	@Override
	public UiElement getElementWrapper(ElementMetaData elementMetaData, Match toolElement, ElementLoaderType type) throws Exception {
		UiElement childUiElement = this.getSikuliUiDriver().declareElement(elementMetaData);
		
		// Set properties
		childUiElement.setName(this.getUiElement().getName() + " (instance)");
		childUiElement.setCompositePageName(this.getUiElement().getCompositePageName());
		childUiElement.setPageLabel(this.getUiElement().getPageLabel());
		
		setElementForChildUiElement(childUiElement, toolElement);
		return childUiElement;
	}

	@Override
	public void setElementForUiElement(Match toolElement) throws Exception {
		this.getUiElement().setElement(toolElement);
		this.getUiElement().switchOffCompositeFlag();
		this.setToolElement(toolElement);
	}

	@Override
	public void setElementsForUiElement(List<Match> toolElements) throws Exception {
		this.getUiElement().setElements(toolElements);
		this.getUiElement().switchOnCompositeFlag();
		this.setToolElements(toolElements);
	}

	@Override
	public void setElementForChildUiElement(UiElement childUiElement, Match toolElement) throws Exception {
		childUiElement.setElement(toolElement);
		childUiElement.switchOffCompositeFlag();
		childUiElement.getMediator().setRawToolElement(toolElement);
	}

	@Override
	public void setElementsForChildUiElement(UiElement childUiElement, List<Match> toolElements) throws Exception {
		childUiElement.setElements(toolElements);
		childUiElement.switchOnCompositeFlag();
		childUiElement.getMediator().setRawToolElements(toolElements);
	}

	@Override
	public void identify() throws Exception {
		SikuliUiDriver automator = this.getSikuliUiDriver();
		Match sikuliElement = null;
		try{
			sikuliElement = automator.findElement(getImagePath());
		} catch (Exception e){
			throw new Exception("Element Identification failed.");
		}
		
		if (sikuliElement == null){
			throw new Exception("Element Identification failed.");
		}
		setElementForUiElement(sikuliElement);
	}

	@Override
	public void identifyAll() throws Exception {
		SikuliUiDriver automator = this.getSikuliUiDriver();
		ArrayList<Match> sikuliElements = null;
		try{
			sikuliElements = automator.findElements(getImagePath());
		} catch (Exception e){
			throw new Exception("Multiple Element identification failed.");
		}
		
		if (sikuliElements == null){
			throw new Exception("Multiple Element identification failed.");
		}
		setElementsForUiElement(sikuliElements);
	}

	@Override
	public void assignElementAtIndexFromMatches(int index) throws Exception {
		this.setElementForUiElement(this.getToolElements().get(index));
	}

	@Override
	public void identifyAtIndex(int index) throws Exception {
		this.prepareIndexIndetification(index);
		this.setElementForUiElement(this.getToolElements().get(index));
	}

	@Override
	public UiElement getInstanceAtIndex(int index) throws Exception {
		identifyAllIfNull();
		Match toolElement = this.getToolElements().get(index);
		return this.getUiElementWrapperForToolElement(toolElement);
	}

	@Override
	public List<UiElement> getAllInstances() throws Exception {
		identifyAllIfNull();
		List<UiElement> uiElements = new ArrayList<UiElement>();
		for (Match toolElement: this.getToolElements()){
			uiElements.add(this.getUiElementWrapperForToolElement(toolElement));
		}
		return uiElements;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#enterText(java.lang.String)
	 */
	@Override
	public void enterText(String text) throws Exception {
		identifyIfNull();
		getSikuliUiDriver().enterText(this.getImagePath(), text);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#setText(java.lang.String)
	 */
	@Override
	public void setText(String text) throws Exception {
		identifyIfNull();
		getSikuliUiDriver().setText(this.getImagePath(), text);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#clearText()
	 */
	@Override
	public void clearText() throws Exception {
		identifyIfNull();
		getSikuliUiDriver().clearText(this.getImagePath());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#isPresent()
	 */
	@Override
	public boolean isPresent() throws Exception {
		identifyIfNull();
		return getSikuliUiDriver().isElementPresent(this.getImagePath());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#click()
	 */
	@Override
	public void click() throws Exception {
		identifyIfNull();
		getSikuliUiDriver().click(this.getImagePath());
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#hoverAndClick()
	 */
	@Override
	public void hoverAndClick() throws Exception {
		getSikuliUiDriver().hoverAndClick(this.getImagePath());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#rightClick()
	 */
	@Override
	public void rightClick() throws Exception {
		getSikuliUiDriver().rightClick(this.getImagePath());
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#getWaitTime()
	 */
	@Override
	public int getWaitTime() throws Exception {
		return getSikuliUiDriver().getWaitTime();
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#takeScreenshot()
	 */
	@Override
	public File takeScreenshot() throws Exception{
		return getSikuliUiDriver().takeScreenshot();
	}
	
	
	
	//========================================================================================
	/*
	 * APIs that are called by an Element either for lazy identification or repeated identification.
	 *
	 */

	
	
	/*
	 * Composite Controls
	 */
	
	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#hoverAndClickElement(com.autocognite.unitee.pvt.uiautomator.element.IDefaultElement)
	 */
	@Override
	public void hoverAndClickElement(UiElement uiElement) throws Exception{
		this.getSikuliUiDriver().hoverAndClickElement(this.getImagePath(), uiElement.getMediator().getImagePath());
	}

	/* (non-Javadoc)
	 * @see com.autocognite.unitee.pvt.uiautomator.sikuli.ISikuliMediator#rightClickAndClickElement(com.autocognite.unitee.pvt.uiautomator.element.IDefaultElement)
	 */
	@Override
	public void rightClickAndClickElement(UiElement uiElement) throws Exception {
		this.getSikuliUiDriver().rightClickAndClickElement(this.getImagePath(), uiElement.getMediator().getImagePath());
	}
}
