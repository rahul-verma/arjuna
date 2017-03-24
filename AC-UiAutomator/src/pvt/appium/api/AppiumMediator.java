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
package pvt.appium.api;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.Select;

import com.arjunapro.uiauto.interfaces.UiElement;

import io.appium.java_client.MobileElement;
import pvt.arjunapro.uiauto.appium.AppiumUiDriver;
import pvt.uiauto.enums.ElementLoaderType;
import pvt.uiautomator.api.ElementMetaData;
import pvt.uiautomator.api.UiMediator;

public interface AppiumMediator extends UiMediator{

	AppiumUiDriver getAppiumUiDriver();

	MobileElement getToolElement() throws Exception;

	MobileElement getToolElementWithRetry() throws Exception;

	Select getSelectElement();

	Select getSelectElementWithRetry() throws Exception;

	void setToolElement(MobileElement toolElement);

	void setToolElements(List<MobileElement> elements);

	List<MobileElement> getToolElements();

	void setRawToolElement(Object toolElementObject);

	void setRawToolElements(Object toolElementsObject);

	void setSelectElement(Select selectElement);

	ArrayList<By> getToolFindersQueue();

	ArrayList<By> getToolFindersQueueObject();

	void setFindersQueue(ArrayList<By> findByQueue);

	boolean isCompositeElementIdentified() throws Exception;

	boolean isSingularElementIdentified() throws Exception;

	int getElementCountForCompositeElement() throws Exception;

	void focus() throws Exception;

	void enterText(String text) throws Exception;

	void setText(String text) throws Exception;

	void clearText() throws Exception;

	boolean isPresent() throws Exception;

	void click() throws Exception;

	void check() throws Exception;

	void uncheck() throws Exception;

	void toggle() throws Exception;

	// Property API
	String getText() throws Exception;

	String getValue() throws Exception;

	String getAttribute(String attr) throws Exception;

	int getWaitTime() throws Exception;

	File takeScreenshot() throws Exception;

	void selectDropDownLabel(String label) throws Exception;

	void selectRadioLabel(String label) throws Exception;

	void selectDropDownValue(String value) throws Exception;

	void selectRadioValue(String value) throws Exception;

	void selectDropDownOptionAtIndex(int index) throws Exception;

	void selectRadioOptionAtIndex(int index) throws Exception;

	boolean isDropDownLabelSelected(String label) throws Exception;

	boolean isRadioLabelSelected(String label) throws Exception;

	boolean isDropDownValueSelected(String value) throws Exception;

	boolean isRadioValueSelected(String value) throws Exception;

	boolean isDropDownOptionSelectedAtIndex(int index) throws Exception;

	boolean isRadioOptionSelectedAtIndex(int index) throws Exception;

	ArrayList<String> getDropDownLabels() throws Exception;

	ArrayList<String> getRadioLabels() throws Exception;

	ArrayList<String> getDropDownValues() throws Exception;

	ArrayList<String> getRadioValues() throws Exception;

	int getDropDownOptionCount() throws Exception;

	int getRadioOptionCount() throws Exception;

	UiElement getUiElementWrapperForToolElement(MobileElement toolElement) throws Exception;

	// While returning element from a Composite UI Element, this method is used to create the wrapper
	UiElement getElementWrapper(ElementMetaData elementMetaData, MobileElement toolElement,
			ElementLoaderType elementLoaderType) throws Exception;

	void setElementForUiElement(MobileElement toolElement) throws Exception;

	void setElementsForUiElement(List<MobileElement> toolElements) throws Exception;

	void setElementForChildUiElement(UiElement childUiElement, MobileElement toolElement) throws Exception;

	void setElementsForChildUiElement(UiElement childUiElement, List<MobileElement> toolElements)
			throws Exception;

	void decorateSingleUiElement(UiElement uiElement, MobileElement toolElement) throws Exception;

	void identify() throws Exception;

	void identifyAll() throws Exception;

	void identifyAtIndex(int index) throws Exception;

	void assignElementAtIndexFromMatches(int index) throws Exception;

	UiElement getInstanceAtIndex(int index) throws Exception;

	UiElement getInstanceByText(String text) throws Exception;

	UiElement getInstanceByTextContent(String text) throws Exception;

	List<UiElement> getAllInstances() throws Exception;

	void setAppiumUiDriver (AppiumUiDriver uiDriver);

}
