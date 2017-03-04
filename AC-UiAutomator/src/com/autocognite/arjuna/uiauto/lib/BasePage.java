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
package com.autocognite.arjuna.uiauto.lib;

import java.io.File;
import java.util.HashMap;
import java.util.Random;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.uiauto.enums.ElementLoaderType;
import com.autocognite.arjuna.uiauto.enums.UiAutomationContext;
import com.autocognite.arjuna.uiauto.enums.UiDriverEngine;
import com.autocognite.arjuna.uiauto.enums.UiElementType;
import com.autocognite.arjuna.uiauto.exceptions.IgnoreElementException;
import com.autocognite.arjuna.uiauto.factories.PageMapperFactory;
import com.autocognite.arjuna.uiauto.interfaces.Page;
import com.autocognite.arjuna.uiauto.interfaces.PageMapper;
import com.autocognite.arjuna.uiauto.interfaces.UiDriver;
import com.autocognite.arjuna.uiauto.interfaces.UiElement;
import com.autocognite.batteries.config.RunConfig;
import com.autocognite.batteries.exceptions.Problem;
import com.autocognite.batteries.util.DataBatteries;
import com.autocognite.pvt.uiautomator.UiAutomator;
import com.autocognite.pvt.uiautomator.api.CentralPageMap;
import com.autocognite.pvt.uiautomator.api.ElementMetaData;
import com.autocognite.pvt.uiautomator.lib.DefaultElementMetaData;
import com.autocognite.pvt.uiautomator.lib.config.UiAutomatorPropertyType;
import com.autocognite.pvt.uiautomator.lib.config.UiAutomatorSingleton;

public class BasePage implements Page{
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private UiDriver automator = null;
	private HashMap<String, UiElement> uiElementMap = new HashMap<String, UiElement>();
	private UiAutomationContext context = null;
	private String label;
	private Page parent = null;
	private ElementLoaderType loaderType = null;
	private String imagesDirectory =  null;
	private String name = null;
	private CentralPageMap uiMap = null;
	
//	private HashMap<String, Object> childUiEntities = new  HashMap<String, Object>();
	
	public BasePage(){
	}
	
	public CentralPageMap getUiMap(){
		return uiMap;
	}
	
	public BasePage(String uiLabel) throws Exception{
		this();
		imagesDirectory = RunConfig.value(UiAutomatorPropertyType.DIRECTORY_UI_IMAGES).asString();
		Random rn = new Random();
		java.util.Date date= new java.util.Date();
		long millis = date.getTime();
		this.name = String.format(
									"%s (OIC:%d.%d)",
									uiLabel, // This is entity_name.ui_label
									rn.nextInt(10000),
									millis
								);
		loadMap();
	}
	
	public BasePage(
			String uiLabel,
			UiDriver automator) throws Exception{
		this(uiLabel);
		this.setContext(automator.getContext());
		this.setElementLoaderType(ElementLoaderType.PAGE);
		automator.setElementLoaderType(ElementLoaderType.PAGE);
		this.setUiDriver(automator);
		this.setLabel(uiLabel);
	}
	
	public BasePage(
			UiDriver automator) throws Exception{
		this("Default Page", automator);
	}

	public BasePage(
			String uiLabel, 
			Page parent, 
			UiDriver automator) throws Exception {
		this(uiLabel, automator);
		this.setParent(parent);
		this.setName(parent.getName() + "." + this.getName());
		this.setElementLoaderType(ElementLoaderType.COMPOSITE_PAGE);
		automator.setElementLoaderType(ElementLoaderType.COMPOSITE_PAGE);
	}
	
	public BasePage(
			String uiLabel, 
			Page parent,
			UiDriver automator, 
			String mapPath) throws Exception {
		this(uiLabel, parent, automator);
		this.populate(PageMapperFactory.getFileMapper(mapPath));
	}
	
	protected void loadMap(){
		this.uiMap = UiAutomatorSingleton.INSTANCE.getCentralMap();		
	}
	
//	public String getImagesDirectory(){
//		return this.imagesDirectory;
//	}
//	
//	protected void setImagesDirectory(String imageDirectory){
//		this.imagesDirectory = imageDirectory;
//	}
	
	public String getName() {
		return name;
	}
	
	public void setName(String name) {
		this.name = name;
	}


	public ElementLoaderType getElementLoaderType() {
		return this.loaderType;
	}

	public void setElementLoaderType(ElementLoaderType type) {
		this.loaderType = type;
	}

	@Override
	public String getLabel() {
		return this.label;
	}

	@Override
	public void setLabel(String label) {
		this.label = label;
	}

	@Override
	public UiAutomationContext getContext() throws Exception {
		return context;
	}

	@Override
	public void setContext(UiAutomationContext context) throws Exception {
		this.context = context;
	}

	@Override
	public Page getParent() {
		return parent;
	}

	@Override
	public void setParent(Page entity) {
		this.parent = entity;
	}

	@Override
	public UiDriver getUiDriver() throws Exception {
		return this.automator;
	}

	@Override
	public void setUiDriver(UiDriver automator) throws Exception {
		if (automator != null){
			this.automator = automator;
		} else {
			throwNullAutomatorException("setAutomator");
		}
	}

	@Override
	public void processUiProperties(String elementName, HashMap<String, String> properties) throws Exception {
		if (this.getParent() != null){
			this.processElementProperties(elementName, properties);
			if (properties != null){
				this.processElementPropertiesForLabel(this.getLabel(), elementName, properties);
			}
		}
	}
	
	@Override
	public void processElementProperties(String elementName, HashMap<String, String> properties) throws Exception  {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void processElementPropertiesForLabel(String uiName, String elementName, HashMap<String, String> properties) throws Exception {
		// TODO Auto-generated method stub
		
	}

	public UiElement element(String name) throws Exception {
		return getElement(name);
	}

	public void populate(PageMapper uiMapper) throws Exception {
		getUiMap().populateRawPageMap(this.getName(), uiMapper);
		HashMap<String, HashMap<String,String>> rawMap = getUiMap().getRawMap(this.getName());
		for (String uiElementName: rawMap.keySet()){
			HashMap<String,String> elemMap = rawMap.get(uiElementName);
			try{
				processUiProperties(uiElementName, elemMap);
			} catch (IgnoreElementException e){
				continue;
			}
			if (elemMap != null){
				addElement(uiElementName, elemMap);
			}
		}
	}
	
	public void populate(String mapPath) throws Exception{
		this.populate(PageMapperFactory.getFileMapper(mapPath));
	}

	public UiElement getElement(String elementName) throws Exception {
		if (elementName == null){
			return (UiElement) throwNullElementException("element", elementName);
		} else if (!uiElementMap.containsKey(elementName)) {
			return (UiElement) throwUndefinedElementException("element", elementName);		
		} else {
			return uiElementMap.get(elementName);
		}
	}

	private UiElement registerElement(String elementName, ElementMetaData elementMap) throws Exception {
		logger.debug("Declaring element");
		UiElement uiElement = getUiDriver().declareElement(elementMap);
		logger.debug("Set element name as " + elementName);		
		uiElement.setName(elementName);
		if (this.getParent() != null){
			logger.debug("Set element entity as " + this.getParent().getName());	
			uiElement.setCompositePageName(this.getParent().getName());
		}
		logger.debug("Verifying entity: " + uiElement.getCompositePageName());
		uiElementMap.put(elementName, uiElement);
		return uiElement;
	}

	public void addElement(String elementName, HashMap<String, String> elementMap) throws Exception {
		ElementMetaData elementMetaData = new DefaultElementMetaData(elementMap);
		elementMetaData.process(this.getContext());
		if (elementMetaData.isRelevantForPage()){
			if (this.isAutomatorPresent()){
				UiElement element = this.registerElement(elementName, elementMetaData);
				element.setPageLabel(this.getLabel());
				element.setMetaData(elementMetaData);
			}			
		}
	}

	@Override
	public boolean isAutomatorPresent() throws Exception {
		return this.automator != null;
	}

	protected Object throwDefaultUiException(String action, String code, String message) throws Exception {
		throw new Problem(
				UiAutomator.getComponentName(),
				this.getName(),
				action,
				code,
				message
				);		
	}

	public Object throwNullAutomatorException(String methodName) throws Exception {
		return throwDefaultUiException(
				methodName,
				UiAutomator.problem.PAGE_NULL_AUTOMATOR,
				RunConfig.getProblemText(
						UiAutomator.problem.PAGE_NULL_AUTOMATOR,
						UiAutomator.getAutomationContextName(this.getContext())
						)
				);
	}

	public Object throwUndefinedElementException(String methodName, String elementName) throws Exception {
		return throwDefaultUiException(
				methodName,
				UiAutomator.problem.PAGE_UNDEFINED_ELEMENT,
				RunConfig.getProblemText(
						UiAutomator.problem.PAGE_UNDEFINED_ELEMENT,
						elementName,
						DataBatteries.toTitleCase(this.getContext().toString())
						//						Batteries.toTitleCase(getDeviceType().toString()),
						//						Batteries.toTitleCase(getAutomationType().toString())
						)
				);
	}

	public Object throwNullElementException(String methodName, String elementName) throws Exception {
		return throwDefaultUiException(
				methodName,
				UiAutomator.problem.UI_NULL_ELEMENT,
				RunConfig.getProblemText(
						UiAutomator.problem.UI_NULL_ELEMENT,
						DataBatteries.toTitleCase(this.getContext().toString())
						//						Batteries.toTitleCase(getDeviceType().toString()),
						//						Batteries.toTitleCase(getAutomationType().toString())
						)
				);
	}
	
	@Override
	public Object getUnderlyingEngine() throws Exception {
		return this.getUiDriver().getUnderlyingEngine();
	}

	@Override
	public UiElement elementWithId(String id) throws Exception {
		return this.getUiDriver().elementWithId(id);
	}

	@Override
	public UiElement elementWithName(String name) throws Exception {
		return this.getUiDriver().elementWithName(name);
	}

	@Override
	public UiElement elementWithClass(String klass) throws Exception {
		return this.getUiDriver().elementWithClass(klass);
	}

	@Override
	public UiElement elementWithCss(String cssSelector) throws Exception {
		return this.getUiDriver().elementWithCss(cssSelector);
	}

	@Override
	public UiElement elementWithLinkText(String text) throws Exception {
		return this.getUiDriver().elementWithLinkText(text);
	}

	@Override
	public UiElement elementWithPartialLinkText(String textContent) throws Exception {
		return this.getUiDriver().elementWithPartialLinkText(textContent);
	}

	@Override
	public UiElement elementWithXPath(String xpath) throws Exception {
		return this.getUiDriver().elementWithXPath(xpath);
	}

	@Override
	public UiElement elementWithXText(String text) throws Exception {
		return this.getUiDriver().elementWithXText(text);
	}

	@Override
	public UiElement elementWithXPartialText(String textContent) throws Exception {
		return this.getUiDriver().elementWithXPartialText(textContent);
	}

	@Override
	public UiElement elementWithXValue(String value) throws Exception {
		return this.getUiDriver().elementWithXValue(value);
	}

	@Override
	public UiElement elementWithXImageSource(String path) throws Exception {
		return this.getUiDriver().elementWithXImageSource(path);
	}

	@Override
	public UiElement elementOfXType(UiElementType type) throws Exception {
		return this.getUiDriver().elementOfXType(type);
	}

	@Override
	public UiElement elementBasedOnImage(String imagePath) throws Exception {
		return this.getUiDriver().elementBasedOnImage(imagePath);
	}

	@Override
	public UiDriverEngine getUiDriverEngineName() throws Exception {
		return this.getUiDriver().getUiDriverEngineName();
	}
	//
	@Override
	public Object getUiDriverEngine() throws Exception {
		return this.getUiDriver().getUiDriverEngine();
	}
	//
	@Override
	public File takeScreenshot() throws Exception {
		return this.getUiDriver().takeScreenshot();
	}
	//
	@Override
	public void setAppTitle(String appTitle) throws Exception {
		this.getUiDriver().setAppTitle(appTitle);
	}
	//
	@Override
	public String getAppTitle() throws Exception {
		return this.getUiDriver().getAppTitle();
	}
	//
	@Override
	public void focusOnApp() throws Exception {
		this.getUiDriver().focusOnApp();
	}
	//
	
	//
	@Override
	public void confirmAlertIfPresent() throws Exception {
		this.getUiDriver().confirmAlertIfPresent();
	}
	//
	@Override
	public void close() throws Exception {
		this.getUiDriver().close();
	}
	//
	@Override
	public String getCurrentWindow() throws Exception {
		return this.getUiDriver().getCurrentWindow();
	}
	//
	@Override
	public void switchToNewWindow() throws Exception {
		this.getUiDriver().switchToNewWindow();
	}
	//
	@Override
	public void switchToWindow(String windowHandle) throws Exception {
		this.getUiDriver().switchToWindow(windowHandle);
	}
	//
	@Override
	public void closeCurrentWindow() throws Exception {
		this.getUiDriver().closeCurrentWindow();
	}
	//
	@Override
	public void goTo(String url) throws Exception {
		this.getUiDriver().goTo(url);
	}
	//
	@Override
	public void refresh() throws Exception {
		this.getUiDriver().refresh();
	}
	//
	@Override
	public void back() throws Exception {
		this.getUiDriver().back();
	}
	//
	@Override
	public void forward() throws Exception {
		this.getUiDriver().forward();
	}
	//
	@Override
	public void waitForBody() throws Exception {
		this.getUiDriver().waitForBody();
	}
	//
	@Override
	public void switchToFrame(int index) throws Exception {
		this.getUiDriver().switchToFrame(index);
	}
	//
	@Override
	public void switchToFrame(String name) throws Exception {
		this.getUiDriver().switchToFrame(name);
	}
	//
	@Override
	public void switchToDefaultFrame() throws Exception {
		this.getUiDriver().switchToDefaultFrame();
	}
	//
	@Override
	public boolean areImagesSimilar(File leftImagePath, File rightImage, Double minScore) throws Exception {
		return this.getUiDriver().areImagesSimilar(leftImagePath, rightImage, minScore);
	}
	//
	@Override
	public boolean areImagesSimilar(String leftImagePath, File rightImage) throws Exception {
		return this.getUiDriver().areImagesSimilar(leftImagePath, rightImage);
	}
	//
	@Override
	public boolean areImagesSimilar(String leftImagePath, File rightImage, Double minScore) throws Exception {
		return this.getUiDriver().areImagesSimilar(leftImagePath, rightImage, minScore);
	}
	//
	@Override
	public boolean areImagesSimilar(String leftImagePath, String rightImagePath) throws Exception {
		return this.getUiDriver().areImagesSimilar(leftImagePath, rightImagePath);
	}
	//
	@Override
	public boolean areImagesSimilar(File leftImage, File rightImage) throws Exception {
		return this.getUiDriver().areImagesSimilar(leftImage, rightImage);
	}
	
	@Override
	public void switchToWebContext() throws Exception {
		this.getUiDriver().switchToWebContext();
	}

	@Override
	public void switchToNativeContext() throws Exception {
		this.getUiDriver().switchToNativeContext();
	}

}
