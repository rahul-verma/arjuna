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
package com.autocognite.arjuna.uiauto.plugins.sikuli;

import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

import javax.imageio.ImageIO;

import org.sikuli.script.App;
import org.sikuli.script.Finder;
import org.sikuli.script.Match;
import org.sikuli.script.Pattern;
import org.sikuli.script.Screen;

import com.autocognite.arjuna.uiauto.enums.ElementLoaderType;
import com.autocognite.arjuna.uiauto.enums.UiAutomationContext;
import com.autocognite.arjuna.uiauto.interfaces.UiDriver;
import com.autocognite.arjuna.uiauto.interfaces.UiElement;
import com.autocognite.arjuna.utils.batteries.FileSystemBatteries;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.batteries.exceptions.Problem;
import com.autocognite.pvt.sikuli.api.SikuliMediator;
import com.autocognite.pvt.sikuli.lib.base.DefaultSikuliMediator;
import com.autocognite.pvt.uiautomator.UiAutomator;
import com.autocognite.pvt.uiautomator.api.ElementMetaData;
import com.autocognite.pvt.uiautomator.api.Identifier;
import com.autocognite.pvt.uiautomator.api.identify.enums.ScreenIdentifyBy;
import com.autocognite.pvt.uiautomator.lib.DefaultUiDriver;
import com.autocognite.pvt.uiautomator.lib.DefaultUiElement;
import com.autocognite.pvt.uiautomator.lib.config.UiAutomatorPropertyType;

public class SikuliScreenUiDriver extends DefaultUiDriver implements UiDriver, SikuliUiDriver{
	
	public SikuliScreenUiDriver(){
		super(UiAutomationContext.SCREEN);
	}
	
	public SikuliScreenUiDriver(ElementLoaderType loaderType) {
		super(UiAutomationContext.SCREEN, loaderType);
	}
	
	public SikuliMediator createMediatorSkeleton(UiElement element) throws Exception {
		return new DefaultSikuliMediator(this, element);
	}

	@Override
	public Object getUiDriverEngine() throws Exception {
		return super.getUiDriverEngine();
	}

	@Override
	public Object getIdentifierType(HashMap<ScreenIdentifyBy, String> map) throws Exception {
		return ScreenIdentifyBy.IMAGE;
	}

	@Override
	public boolean areImagesSimilar(File leftImage, File rightImage, Double minScore) throws Exception {
	    boolean imagesMatch = false;
	    Double score = 0.0d;
		if (!leftImage.exists()){
			throwImageNotFoundException("areImagesSimilar", "Left", leftImage.getAbsolutePath());
		}
		
		if (!rightImage.exists()){
			throwImageNotFoundException("areImagesSimilar", "Right", rightImage.getAbsolutePath());
		}
	    BufferedImage bufferedLeftImage = ImageIO.read(leftImage);
	    BufferedImage bufferedRightImage = ImageIO.read(rightImage);
	    int leftImageHeight = bufferedLeftImage.getHeight();
	    int leftImageWidth = bufferedLeftImage.getWidth();
	    int rightImageHeight = bufferedRightImage.getHeight();
	    int rightImageWidth = bufferedRightImage.getWidth();
	
	    if (leftImageWidth >= rightImageWidth && leftImageHeight >= rightImageHeight) {
	        Finder finder = new Finder(leftImage.getAbsolutePath());
	        finder.find(new Pattern(rightImage.getAbsolutePath()));
	        if (finder.hasNext()) {
	            score = finder.next().getScore();
	            imagesMatch = true;
	        }
	    } else if (leftImageWidth <= rightImageWidth && rightImageHeight >= leftImageHeight) {
	        Finder finder = new Finder(rightImage.getAbsolutePath());
	        finder.find(new Pattern(leftImage.getAbsolutePath()));
	        if (finder.hasNext()) {
	            score = finder.next().getScore();
	            imagesMatch = true;
	        }
	    } else {
	    	throwImagesNotComparableException("areImagesSimilar", leftImage.getAbsolutePath(), rightImage.getAbsolutePath());
	    }
	
	    if (!imagesMatch){
	    	return false;
	    } else  if (score < minScore){
	    	return false;
	    } else {
	    	return true;
	    }
	}

	private double getDefaultMinScore() throws Exception {
		return Batteries.value(UiAutomatorPropertyType.SIKULI_COMPARISON_SCORE).asDouble();
	}

	@Override
	public boolean areImagesSimilar(String leftImagePath, File rightImage) throws Exception {
		return areImagesSimilar(new File(leftImagePath), rightImage, getDefaultMinScore());
	}

	@Override
	public boolean areImagesSimilar(String leftImagePath, File rightImage, Double minScore) throws Exception {
		return areImagesSimilar(new File(leftImagePath), rightImage, minScore);
	}

	@Override
	public boolean areImagesSimilar(String leftImagePath, String rightImagePath) throws Exception {
		return areImagesSimilar(new File(leftImagePath), new File(rightImagePath), getDefaultMinScore());
	}

	@Override
	public boolean areImagesSimilar(File leftImage, File rightImage) throws Exception {
		return areImagesSimilar(leftImage, rightImage, getDefaultMinScore());
	}

	protected void throwScreenAutomatorException(String action, String code, String message) throws Exception {
				throw new Problem(
						Batteries.getConfiguredName("COMPONENT_NAMES", "SIKULI_AUTOMATOR"),
				this.getClass().getSimpleName(),
				action,
				code,
				message
				);		
	}

	@Override
	public void throwImageNotFoundException(String methodName, String whichSide, String filePath) throws Exception {
		throwScreenAutomatorException(
				methodName,
				UiAutomator.problem.COMPARISON_IMAGE_NOT_FOUND,
				Batteries.getProblemText(
						UiAutomator.problem.COMPARISON_IMAGE_NOT_FOUND,
						whichSide,
						filePath
				)
		);
	}

	@Override
	public void throwImagesNotComparableException(String methodName, String leftImagePath, String rightImagePath) throws Exception {
		throwScreenAutomatorException(
				methodName,
				UiAutomator.problem.COMPARISON_NOT_POSSIBLE,
				Batteries.getProblemText(
						UiAutomator.problem.COMPARISON_NOT_POSSIBLE,
						FileSystemBatteries.getCanonicalPath(leftImagePath),
						FileSystemBatteries.getCanonicalPath(rightImagePath)
				)
		);
	}

	@Override
	public UiElement declareElement(ElementMetaData  elementMetaData) throws Exception {
		UiElement uiElement = createDefaultElementSkeleton(elementMetaData);
		// This needs to be done in a better way for image recognition based libraries.
		// Some equivalent of By needs to be coded for consistency.
		for (Identifier id: elementMetaData.getIdentifiers()){
			if (id.NAME.equals("IMAGE")){
				uiElement.setImagePath(
						FileSystemBatteries.getCanonicalPath(Batteries.value(UiAutomatorPropertyType.DIRECTORY_UI_IMAGES).asString() + "/" + id.VALUE));
			}
		}
		SikuliMediator mediator = createMediatorSkeleton(uiElement);
		uiElement.setMediator(mediator);
		uiElement.setLoaderType(this.getElementLoaderType());
		mediator.setAutomatorName("Sikuli Automator");
		return uiElement;
	}

	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#focusOnApp()
	 */
	@Override
	public void focusOnApp() throws Exception{
		App app = new App(this.getAppTitle());
		app.focus();
	}

	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#click(java.lang.String)
	 */
	@Override
	public void click(String imagePath) throws Exception{
		waitForElementVisibility(imagePath);
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		screen.click(pattern);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#doubleClick(java.lang.String)
	 */
	@Override
	public void doubleClick(String imagePath)  throws Exception{
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		screen.doubleClick(pattern);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#rightClick(java.lang.String)
	 */
	@Override
	public void rightClick(String imagePath)  throws Exception{
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		screen.rightClick(pattern);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#hover(java.lang.String)
	 */
	@Override
	public void hover(String imagePath)  throws Exception{
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		screen.hover(pattern);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#hoverAndClick(java.lang.String)
	 */
	@Override
	public void hoverAndClick(String imagePath1) throws Exception{
		Screen screen = new Screen();
		Pattern pattern1 = new Pattern(imagePath1);
		screen.hover(pattern1);
		screen.click(pattern1);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#hoverAndClickElement(java.lang.String, java.lang.String)
	 */
	@Override
	public void hoverAndClickElement(String imagePath1, String imagePath2) throws Exception{
		Screen screen = new Screen();
		Pattern pattern1 = new Pattern(imagePath1);
		Pattern pattern2 = new Pattern(imagePath1);
		screen.hover(pattern1);
		screen.click(pattern2);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#righClickAndClickElement(java.lang.String, java.lang.String)
	 */
	@Override
	public void rightClickAndClickElement(String imagePath1, String imagePath2) throws Exception {
		Screen screen = new Screen();
		Pattern pattern1 = new Pattern(imagePath1);
		Pattern pattern2 = new Pattern(imagePath1);
		screen.rightClick(pattern1);
		screen.click(pattern2);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#setText(java.lang.String, java.lang.String)
	 */
	@Override
	public void setText(String imagePath, String text)  throws Exception{
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		screen.paste(pattern, text);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#enterText(java.lang.String, java.lang.String)
	 */
	@Override
	public void enterText(String imagePath, String text)  throws Exception{
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		screen.type(pattern, text);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#dragAndDrop(java.lang.String, java.lang.String)
	 */
	@Override
	public void dragAndDrop(String imagePathToDrag, String imagePathForDrop)  throws Exception{
		Screen screen = new Screen();
		Pattern pattern1 = new Pattern(imagePathToDrag);
		Pattern pattern2 = new Pattern(imagePathForDrop);
		screen.dragDrop(pattern1, pattern2);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#mouseWheelDown(int)
	 */
	@Override
	public void mouseWheelDown(int downCount)  throws Exception{
		Screen screen = new Screen();
		screen.mouseDown(downCount);
	}
	
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#mouseWheelDown()
	 */
	@Override
	public void mouseWheelDown() throws Exception{
		mouseWheelDown(5);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#mouseWheelUp(int)
	 */
	@Override
	public void mouseWheelUp(int upCount)  throws Exception{
		Screen screen = new Screen();
		screen.mouseUp(upCount);
	}
	
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#mouseWheelUp()
	 */
	@Override
	public void mouseWheelUp()  throws Exception{
		mouseWheelUp(5);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#waitForElementVisibility(java.lang.String)
	 */
	@Override
	public void waitForElementVisibility(String imagePath)  throws Exception{
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		// Get the sleep time from configuration
		screen.wait(pattern, (double) (60 / 1000));
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#waitForElementInvisibility(java.lang.String)
	 */
	@Override
	public void waitForElementInvisibility(String imagePath) throws Exception{
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		// Get the sleep time from configuration
		screen.waitVanish(pattern, (double) (60 / 1000));
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#isElementPresent(java.lang.String)
	 */
	@Override
	public boolean isElementPresent(String imagePath)  throws Exception{
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		Match m = screen.exists(pattern);
		if (m != null) {
			return true;

		} else {
			return false;
		}
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#isElementAbsent(java.lang.String)
	 */
	@Override
	public boolean isElementAbsent(String imagePath)  throws Exception{
		return !isElementPresent(imagePath);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#findElement(java.lang.String)
	 */
	@Override
	public Match findElement(String imagePath) throws Exception{
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		return screen.find(pattern);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#findElements(java.lang.String)
	 */
	@Override
	public ArrayList<Match> findElements(String imagePath)  throws Exception{
		Screen screen = new Screen();
		Pattern pattern = new Pattern(imagePath);
		Iterator<Match> matches = screen.findAll(pattern);
		if (matches != null){
			ArrayList<Match> matchedElements = new ArrayList<Match>();
			while(matches.hasNext()){
				matchedElements.add(matches.next());
			}
			return matchedElements;
		} else {
			return null;
		}
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#sendKeysToScreen(java.lang.String)
	 */
	@Override
	public void sendKeysToScreen(String text) throws Exception{
		Screen screen = new Screen();
		screen.type(text);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#waitForElementPresence(java.lang.String)
	 */
	@Override
	public void waitForElementPresence(String imagePath) throws Exception{
		waitForElementVisibility(imagePath);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#waitForElementAbsence(java.lang.String)
	 */
	@Override
	public void waitForElementAbsence(String imagePath) throws Exception{
		waitForElementInvisibility(imagePath);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#clickIfPresent(java.lang.String)
	 */
	@Override
	public void clickIfPresent(String imagePath) throws Exception {
		click(imagePath);
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#enterText(org.sikuli.script.Match, java.lang.String)
	 */
	@Override
	public void enterText(Match sikuliElement, String text) throws Exception{
		sikuliElement.type(text);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#setText(org.sikuli.script.Match, java.lang.String)
	 */
	@Override
	public void setText(Match sikuliElement, String text) throws Exception{
		sikuliElement.paste(text);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#getUnderlyingEngine()
	 */
	@Override
	public Object getUnderlyingEngine() {
		// TODO Auto-generated method stub
		return null;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#takeScreenShot()
	 */
	@Override
	public File takeScreenshot() throws Exception{
		return null;
       //throw new Exception("Not supported yet.");
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.support.sikuli.lib.Itemp#getWaitTime()
	 */
	@Override
	public int getWaitTime() throws Exception{
		return Batteries.value(UiAutomatorPropertyType.SIKULI_MAXWAIT).asInt();
	}
	
	/*
	 * Exceptions
	 */
	
	public void close() {
		// TODO Auto-generated method stub
		
	}
	
	@Override
	public void clearText(String imagePath) throws Exception {
		this.setText(imagePath, "");
	}

	public UiElement createDefaultElementSkeleton(ElementMetaData elementMetaData) throws Exception {
		return new DefaultUiElement(elementMetaData);
	}

}
