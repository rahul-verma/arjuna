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
package arjunasdk.uiauto.interfaces;

import java.io.File;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;

import pvt.arjunasdk.uiauto.api.ElementMetaData;
import pvt.arjunasdk.uiauto.enums.UiElementType;

public interface SeleniumUiDriver {

	void focus(WebElement WebElement) throws Exception;
	void enterText(WebElement WebElement, String text)throws Exception;
	void setText(WebElement WebElement, String text) throws Exception;
	void clearText(WebElement WebElement) throws Exception;
	boolean isElementPresent(By appiumFindBy) throws Exception;
	void click(WebElement WebElement) throws Exception;
	void waitForElementPresence(By appiumFindBy) throws Exception;
	void check(WebElement WebElement) throws Exception;
	void uncheck(WebElement WebElement) throws Exception;
	void toggle(WebElement WebElement) throws Exception;
	String getText(WebElement WebElement) throws Exception;
	String getValue(WebElement WebElement) throws Exception;
	String getAttribute(WebElement WebElement, String attr) throws Exception;
	void selectDropDownLabel(Select selectControl, String text) throws Exception;
	void clickIfNotSelected(WebElement element) throws Exception;
	void selectDropDownValue(Select selectControl, String value) throws Exception;
	WebElement chooseElementBasedOnValue(List<WebElement> elements,String value) throws Exception;
	void selectDropDownOptionAtIndex(Select selectControl, int index) throws Exception;
	boolean isDropDownSelectedText(Select selectControl, String text) throws Exception;
	boolean isSelectedElementParentText(List<WebElement> elements, String text) throws Exception;
	boolean isDropDownSelectedValue(Select selectControl, String value) throws Exception;
	boolean isSelectedValue(List<WebElement> elements, String value) throws Exception;
	boolean isDropDownSelectedIndex(Select selectControl, int index) throws Exception;
	boolean isSelectedIndex(List<WebElement> elements, int index) throws Exception;
	List<String> getDropDownOptionLabels(Select selectControl) throws Exception;
	List<String> getRadioButtonLabels(List<WebElement> elements) throws Exception;
	List<String> getDropDownOptionValues(Select selectControl) throws Exception;
	List<String> getRadioButtonValues(List<WebElement> elements) throws Exception;
	int getDropDownOptionCount(Select selectControl) throws Exception;
	WebElement chooseElementBasedOnParentText(List<WebElement> elements,String text) throws Exception;
	int getWaitTime() throws Exception;
	File takeScreenshot() throws Exception;
	UiElementType getElementType(WebElement wdElement) throws Exception;
	List<WebElement> findElements(By appiumFindBy) throws Exception;
	void rightClickAndClick(By by1, By by2) throws Exception;
	WebElement findElement(By by) throws Exception;
	void hoverAndClick(By by1, By by2) throws Exception;
	UiElement declareElement(ElementMetaData elementMetaData) throws Exception;
	void rightClick(WebElement wdElement)  throws Exception;
	void hoverAndClick(WebElement wdElement) throws Exception;
	Select convertToSelectElement(WebElement toolElement) throws Exception;
	void hover(WebElement element) throws Exception;
	void switchToFrame(WebElement wdElement) throws Exception;
	//WDMediator createMediatorSkeleton(UiElement uiElement) throws Exception;
	void waitForElementAbsence(By findBy) throws Exception;
	void waitForElementVisibility(By findBy) throws Exception;
	void waitForElementInvisibility(By findBy) throws Exception;
	boolean isElementAbsent(By findBy);
	boolean isElementVisible(By findBy);
	boolean isElementInvisible(By findBy);

}
