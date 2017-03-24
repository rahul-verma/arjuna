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
package pvt.arjunapro.uiauto.appium;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.Select;

import com.arjunapro.uiauto.interfaces.UiElement;

import io.appium.java_client.MobileElement;
import pvt.appium.api.AppiumMediator;
import pvt.uiauto.enums.UiElementType;
import pvt.uiautomator.api.ElementMetaData;

public interface AppiumUiDriver{

	void focus(MobileElement appiumElement) throws Exception;
	void enterText(MobileElement appiumElement, String text)throws Exception;
	void setText(MobileElement appiumElement, String text) throws Exception;
	void clearText(MobileElement appiumElement) throws Exception;
	boolean isElementPresent(By appiumFindBy) throws Exception;
	void click(MobileElement appiumElement) throws Exception;
	void waitForElementPresence(By appiumFindBy) throws Exception;
	void check(MobileElement appiumElement) throws Exception;
	void uncheck(MobileElement appiumElement) throws Exception;
	void toggle(MobileElement appiumElement) throws Exception;
	String getText(MobileElement appiumElement) throws Exception;
	String getValue(MobileElement appiumElement) throws Exception;
	String getAttribute(MobileElement appiumElement, String attr) throws Exception;
	void selectDropDownLabel(Select selectControl, String text) throws Exception;
	void clickIfNotSelected(MobileElement element) throws Exception;
	void selectDropDownValue(Select selectControl, String value) throws Exception;
	MobileElement chooseElementBasedOnValue(List<MobileElement> elements,String value) throws Exception;
	void selectDropDownOptionAtIndex(Select selectControl, int index) throws Exception;
	boolean isDropDownSelectedText(Select selectControl, String text) throws Exception;
	boolean isSelectedElementParentText(List<MobileElement> elements, String text) throws Exception;
	boolean isDropDownSelectedValue(Select selectControl, String value) throws Exception;
	boolean isSelectedValue(List<MobileElement> elements, String value) throws Exception;
	boolean isDropDownSelectedIndex(Select selectControl, int index) throws Exception;
	boolean isSelectedIndex(List<MobileElement> elements, int index) throws Exception;
	ArrayList<String> getDropDownOptionLabels(Select selectControl) throws Exception;
	ArrayList<String> getRadioButtonLabels(List<MobileElement> elements) throws Exception;
	ArrayList<String> getDropDownOptionValues(Select selectControl) throws Exception;
	ArrayList<String> getRadioButtonValues(List<MobileElement> elements) throws Exception;
	int getDropDownOptionCount(Select selectControl) throws Exception;
	MobileElement chooseElementBasedOnParentText(List<MobileElement> elements,String text) throws Exception;
	int getWaitTime() throws Exception;
	File takeScreenshot() throws Exception;
	UiElementType getElementType(MobileElement appiumElement) throws Exception;
	List<MobileElement> findElements(By appiumFindBy) throws Exception;
	MobileElement findElement(By by) throws Exception;
	String getName();
	Select convertToSelectElement(MobileElement toolElement) throws Exception;
	void switchToWebContext() throws Exception;
	void switchToNativeContext() throws Exception;
	void switchToFrame(MobileElement appiumElement) throws Exception;
	AppiumMediator createMediatorSkeleton(UiElement element) throws Exception;
	UiElement declareElement(ElementMetaData elementMetaData) throws Exception;
	void waitForElementAbsence(By findBy) throws Exception;
	void waitForElementVisibility(By findBy) throws Exception;
	void waitForElementInvisibility(By findBy) throws Exception;
	boolean isElementAbsent(By findBy);
	boolean isElementVisible(By findBy);
	boolean isElementInvisible(By findBy);
}
