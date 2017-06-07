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
import java.util.ArrayList;
import java.util.HashMap;

import org.sikuli.script.Match;

import pvt.arjunasdk.uiauto.api.ElementMetaData;
import pvt.arjunasdk.uiauto.enums.ScreenIdentifyBy;
import pvt.sikuli.api.SikuliMediator;

public interface SikuliUiDriver {
	void focusOnApp() throws Exception;
	Object getIdentifierType(HashMap<ScreenIdentifyBy, String> map) throws Exception;
	void click(String imagePath) throws Exception;
	void doubleClick(String imagePath) throws Exception;
	void rightClick(String imagePath) throws Exception;
	void hover(String imagePath) throws Exception;
	void hoverAndClick(String imagePath1) throws Exception;
	void hoverAndClickElement(String imagePath1, String imagePath2) throws Exception;
	void rightClickAndClickElement(String imagePath1, String imagePath2) throws Exception;
	void setText(String imagePath, String text) throws Exception;
	void enterText(String imagePath, String text) throws Exception;
	void dragAndDrop(String imagePathToDrag, String imagePathForDrop) throws Exception;
	void mouseWheelDown(int downCount) throws Exception;
	void mouseWheelDown() throws Exception;
	void mouseWheelUp(int upCount) throws Exception;
	void mouseWheelUp() throws Exception;
	void waitForElementVisibility(String imagePath) throws Exception;
	void waitForElementInvisibility(String imagePath) throws Exception;
	boolean isElementPresent(String imagePath) throws Exception;
	boolean isElementAbsent(String imagePath) throws Exception;
	Match findElement(String imagePath) throws Exception;
	ArrayList<Match> findElements(String imagePath) throws Exception;
	void sendKeysToScreen(String text) throws Exception;
	void waitForElementPresence(String imagePath) throws Exception;
	void waitForElementAbsence(String imagePath) throws Exception;
	void clickIfPresent(String imagePath) throws Exception;
	void enterText(Match sikuliElement, String text) throws Exception;
	void setText(Match sikuliElement, String text) throws Exception;
	Object getUnderlyingEngine() throws Exception;
	boolean areImagesSimilar(File leftImage, File rightImage, Double minScore) throws Exception;
	boolean areImagesSimilar(String leftImagePath, File rightImage) throws Exception;
	boolean areImagesSimilar(String leftImagePath, File rightImage, Double minScore) throws Exception;
	boolean areImagesSimilar(String leftImagePath,String rightImagePath) throws Exception;
	boolean areImagesSimilar(File leftImage, File rightImage) throws Exception;
	void throwImageNotFoundException(String methodName, String whichSide, String filePath) throws Exception;
	void throwImagesNotComparableException(String methodName, String leftImagePath, String rightImagePath) throws Exception;

	int getWaitTime() throws Exception;
	File takeScreenshot() throws Exception;
	void clearText(String imagePath) throws Exception;
	
	SikuliMediator createMediatorSkeleton(UiElement element) throws Exception;
	UiElement declareElement(ElementMetaData elementMetaData) throws Exception;
}
