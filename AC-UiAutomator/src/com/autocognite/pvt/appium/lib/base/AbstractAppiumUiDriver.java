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
package com.autocognite.pvt.appium.lib.base;

import java.io.File;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.Proxy;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.Augmenter;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.UnreachableBrowserException;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.enums.Browser;
import com.autocognite.arjuna.uiauto.enums.ElementLoaderType;
import com.autocognite.arjuna.uiauto.enums.UiAutomationContext;
import com.autocognite.arjuna.uiauto.enums.UiDriverEngine;
import com.autocognite.arjuna.uiauto.enums.UiElementType;
import com.autocognite.arjuna.uiauto.interfaces.UiElement;
import com.autocognite.arjuna.uiauto.plugins.appium.AppiumMobilePlatformType;
import com.autocognite.arjuna.uiauto.plugins.appium.AppiumUiDriver;
import com.autocognite.arjuna.utils.FileSystemBatteries;
import com.autocognite.pvt.appium.api.AppiumMediator;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.batteries.enums.BatteriesPropertyType;
import com.autocognite.pvt.batteries.exceptions.Problem;
import com.autocognite.pvt.uiautomator.UiAutomator;
import com.autocognite.pvt.uiautomator.api.ElementMetaData;
import com.autocognite.pvt.uiautomator.api.Identifier;
import com.autocognite.pvt.uiautomator.api.identify.enums.MobileWebIdentifyBy;
import com.autocognite.pvt.uiautomator.lib.DefaultUiDriver;
import com.autocognite.pvt.uiautomator.lib.DefaultUiElement;
import com.autocognite.pvt.uiautomator.lib.config.UiAutomatorPropertyType;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.ios.IOSDriver;
import io.appium.java_client.remote.MobileCapabilityType;

public abstract class AbstractAppiumUiDriver extends DefaultUiDriver implements AppiumUiDriver {

	private AppiumDriver<MobileElement> driver = null;
	private WebDriverWait waiter = null;
	private Browser browser = null;
	private int waitTime = -1;
	private String appPath = null;
	UiAutomationContext context = null;
	
	public AbstractAppiumUiDriver() throws Exception{
		super(UiAutomationContext.MOBILE_WEB, ElementLoaderType.AUTOMATOR);
		init(UiAutomationContext.MOBILE_WEB, null);
	}

	public AbstractAppiumUiDriver(String appPath, UiAutomationContext context, ElementLoaderType loaderType) throws Exception{
		super(context, loaderType);
		if (appPath == null){
			throw new Exception("Null value supplied for appPath");
		}
		init(context, appPath);
	}
	
	public AbstractAppiumUiDriver(String appPath) throws Exception{
		this(appPath, UiAutomationContext.MOBILE_NATIVE, ElementLoaderType.AUTOMATOR);
	}
	
	public AbstractAppiumUiDriver(UiAutomationContext context, ElementLoaderType loaderType) throws Exception{
		super(context, loaderType);
		init(context, null);
	}
	
	public AppiumMediator createMediatorSkeleton(UiElement element) throws Exception {
		return new DefaultAppiumMediator(this, element);
	}
	
	public UiElement createDefaultElementSkeleton(ElementMetaData elementMetaData) throws Exception {
		return new DefaultUiElement(elementMetaData);
	}
	
	private void NOTEXPOSED_startService() {
		//		AppiumDriverLocalService service;
		//		String nodeLoc ="/Applications/Appium.app/Contents/Resources/node/bin/node";
		//		String appiumLoc ="/Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js";
		//		service = AppiumDriverLocalService
		//			.buildService
		//			(
		//			new AppiumServiceBuilder()
		//				.usingDriverExecutable(new File(nodeLoc))
		//				.withAppiumJS(new File(appiumLoc))
		//			);
		//		service.start();
	}

	protected void init(UiAutomationContext context, String appPath) throws Exception {
		this.context = context;
		this.setAppPath(appPath);
		switch(context){
		case MOBILE_WEB: this.setWaitTime(Batteries.value(UiAutomatorPropertyType.BROWSER_MOBILE_MAXWAIT).asInt());
		case MOBILE_NATIVE: this.setWaitTime(Batteries.value(UiAutomatorPropertyType.APP_MOBILE_MAXWAIT).asInt());
		default: this.setWaitTime(Batteries.value(UiAutomatorPropertyType.APP_MOBILE_MAXWAIT).asInt());
		}
		this.setUiTestEngineName(UiDriverEngine.APPIUM);	
		DesiredCapabilities capabilities = new DesiredCapabilities();
		URL hubUrl = new URL(
				String.format(
						Batteries.value(UiAutomatorPropertyType.APPIUM_HUB_URL).asString(),
						Batteries.value(UiAutomatorPropertyType.APPIUM_HUB_HOST).asString(),
						Batteries.value(UiAutomatorPropertyType.APPIUM_HUB_PORT).asString()
						)
				);
		String platform = Batteries.value(UiAutomatorPropertyType.MOBILE_PLATFORM_NAME).asString();
		if (!UiAutomator.isAllowedAppiumPlatform(platform)){
			throwUnsupportedPlatformException("constructor", platform);
		}
		AppiumMobilePlatformType platformType = AppiumMobilePlatformType.valueOf(platform.toUpperCase());
		setCapabilities(platformType, capabilities);
		try{
			switch(platformType){
			case ANDROID: driver = new AndroidDriver<MobileElement>(hubUrl, capabilities); break;
			case IOS: driver = new IOSDriver<MobileElement>(hubUrl, capabilities); break;
			}
	
		}catch (UnreachableBrowserException e){
			throwUnreachableBrowserException(platformType, e);
		}
		this.setWaiter(new WebDriverWait(this.getDriver(), this.getWaitTime()));
	}

	public void setMobileNativeCapabilities(AppiumMobilePlatformType platform, DesiredCapabilities capabilities) throws Exception {		
		capabilities.setCapability(MobileCapabilityType.PLATFORM_NAME, UiAutomator.getAppiumPlatformString(platform));
		capabilities.setCapability(MobileCapabilityType.PLATFORM_VERSION, Batteries.value(UiAutomatorPropertyType.MOBILE_PLATFORM_VERSION).asString());
		capabilities.setCapability(MobileCapabilityType.APP, this.getAppPath());
		capabilities.setCapability(MobileCapabilityType.DEVICE_NAME, Batteries.value(UiAutomatorPropertyType.MOBILE_DEVICE_NAME).asString());
		if (!Batteries.value(UiAutomatorPropertyType.MOBILE_PLATFORM_NAME).isNull()){
			capabilities.setCapability(MobileCapabilityType.UDID, Batteries.value(UiAutomatorPropertyType.MOBILE_DEVICE_UDID).asString());
		}
	}

	public void setMobileWebCapabilities(AppiumMobilePlatformType platform, DesiredCapabilities capabilities) throws Exception {
		String browser = Batteries.value(UiAutomatorPropertyType.BROWSER_MOBILE_DEFAULT).asString();
		if (!UiAutomator.isAllowedAppiumBrowser(platform, browser)){
			throwUnsupportedBrowserException("setMobileCapabilities", platform, browser);
		}
		capabilities.setCapability(MobileCapabilityType.PLATFORM_NAME, UiAutomator.getAppiumPlatformString(platform));
		capabilities.setCapability(MobileCapabilityType.PLATFORM_VERSION,  Batteries.value(UiAutomatorPropertyType.MOBILE_PLATFORM_VERSION).asString());
		capabilities.setCapability(MobileCapabilityType.BROWSER_NAME, UiAutomator.getAppiumBrowserString(browser));
		capabilities.setCapability(MobileCapabilityType.DEVICE_NAME, Batteries.value(UiAutomatorPropertyType.MOBILE_DEVICE_NAME).asString());
		if (!Batteries.value(UiAutomatorPropertyType.MOBILE_DEVICE_UDID).isNull()){
			capabilities.setCapability(MobileCapabilityType.UDID, Batteries.value(UiAutomatorPropertyType.MOBILE_DEVICE_UDID).asString());
		}
	}

	public void setCapabilities(AppiumMobilePlatformType platform, DesiredCapabilities capabilities) throws Exception {
		if (Batteries.value(UiAutomatorPropertyType.BROWSER_MOBILE_PROXY_ON).asBoolean()){
			Proxy proxy = new Proxy();
			String p = Batteries.value(UiAutomatorPropertyType.BROWSER_MOBILE_PROXY_HOST).asString() + ":" + Batteries.value(UiAutomatorPropertyType.BROWSER_MOBILE_PROXY_PORT).asString();
			setHttpProxy(proxy, p);
			setSslProxy(proxy, p);
			capabilities.setCapability("proxy", proxy);
		}
		switch(this.getContext()){
		case MOBILE_WEB: setMobileWebCapabilities(platform, capabilities) ; break;
		case MOBILE_NATIVE: setMobileNativeCapabilities(platform, capabilities); break;
		default: throw new Exception("Unsupported automation context for Appium. Allowed: MOBILE_WEB/MOBILE_NATIVE");
		}
	}

	public void setHttpProxy(Proxy proxy, String proxyString) {
		proxy.setHttpProxy(proxyString);
	}

	public void setSslProxy(Proxy proxy, String proxyString) {
		proxy.setSslProxy(proxyString);
	}

	public AppiumDriver<MobileElement> getDriver() {
		return driver;
	}

	public void setDriver(AppiumDriver<MobileElement> driver) {
		this.driver = driver;
	}

	public String getAppPath() {
		return appPath;
	}

	public void setAppPath(String appPath) {
		this.appPath = appPath;
	}

	public WebDriverWait getWaiter() {
		return this.waiter;
	}

	public void setWaiter(WebDriverWait waiter) {
		this.waiter = waiter;
	}

	public int getWaitTime() {
		return this.waitTime;
	}

	public void setWaitTime(int waitTime) {
		this.waitTime = waitTime;
	}

	public void setBrowser(Browser browser) {
		this.browser = browser;
	}

	public Browser getBrowser() {
		return this.browser;
	}

	@Override
	public Object getUiDriverEngine() {
		return this.getDriver();
	}

	public Object getUnderlyingEngine() {
		return getDriver();
	}

	/**********************************************************************************/

	@Override
	public UiElement declareElement(ElementMetaData elementMetaData) throws Exception {
		UiElement uiElement = createDefaultElementSkeleton(elementMetaData);
		ArrayList<By> finderQueue = new ArrayList<By>();
		for (Identifier id: elementMetaData.getIdentifiers()){
			finderQueue.add(getFinderType(id.NAME, id.VALUE));
		}

		AppiumMediator mediator = createMediatorSkeleton(uiElement);
		uiElement.setMediator(mediator);
		uiElement.setLoaderType(this.getElementLoaderType());
		mediator.setFindersQueue(finderQueue);
		mediator.setAutomatorName(this.getName());
		return uiElement;
	}

	public By getFinderType(String identifier, String idValue) throws Exception {
		By findBy = null;
		MobileWebIdentifyBy idType = null;
		try{
			idType = MobileWebIdentifyBy.valueOf(identifier.toUpperCase());
		} catch (Throwable e){
			throwUnsupportedIndentifierException(
					this.getName(),
					"getFinderType",
					identifier);
		}
		switch(identifier.toUpperCase()){
		case "ID": findBy = By.id(idValue); break;
		case "NAME": findBy = By.name(idValue); break;
		case "CLASS": findBy = By.className(idValue); break;
		case "LINK_TEXT": findBy = By.linkText(idValue); break;
		case "PARTIAL_LINK_TEXT": findBy = By.partialLinkText(idValue); break;
		case "XPATH": findBy = By.xpath(idValue); break;
		case "CSS": findBy = By.cssSelector(idValue); break;
		case "TAG": findBy = By.tagName(idValue); break;
		}
		return findBy;
	}

	public UiElementType getElementType(MobileElement wdElement) {
		String tagName = wdElement.getTagName().toLowerCase();
		if (tagName.equals("select")){
			return UiElementType.DROPDOWN;
		} else if (tagName.equals("input") && wdElement.getAttribute("type").toLowerCase().equals("radio") ){
			return UiElementType.RADIO;
		} else {
			return UiElementType.GENERIC;
		}
	}

	/**********************************************************************************
	/**					EXCEPTIONS											
	 *********************************************************************************/
	protected void throwAppiumAutomatorException(String action, String code, String message) throws Exception {
		throw new Problem(
				Batteries.getConfiguredName("COMPONENT_NAMES", "APPIUM_AUTOMATOR"),
				this.getClass().getSimpleName(),
				action,
				code,
				message
				);		
	}

	protected void throwUnsupportedPlatformException(String methodName, String platform) throws Exception {
		throwAppiumAutomatorException(
				methodName,
				UiAutomator.problem.APPIUM_UNSUPPORTED_PLATFORM,
				Batteries.getProblemText(
						UiAutomator.problem.APPIUM_UNSUPPORTED_PLATFORM,
						platform
						)
				);
	}

	protected void throwUnsupportedBrowserException(String methodName, AppiumMobilePlatformType platform, String browser) throws Exception {
		throwAppiumAutomatorException(
				methodName,
				UiAutomator.problem.APPIUM_UNSUPPORTED_BROWSER,
				Batteries.getProblemText(
						UiAutomator.problem.APPIUM_UNSUPPORTED_BROWSER,
						browser,
						UiAutomator.getAppiumPlatformString(platform)
						)
				);
	}

	private void throwUnreachableBrowserException(AppiumMobilePlatformType platformType, Throwable e) throws Exception {
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
				this.getName(),
				"Constructor",
				UiAutomator.problem.APPIUM_UNREACHABLE_BROWSER,
				Batteries.getProblemText(UiAutomator.problem.APPIUM_UNREACHABLE_BROWSER, UiAutomator.getAppiumPlatformString(platformType)),
				e
				);
	}
	
	/**********************************************************************************/
	/*					AUTOMATOR API												*/
	/**********************************************************************************/
	
	public void goTo(String url) throws Exception {
		getDriver().get(url);
		waitForBody();
	}
	
	public void refresh() throws Exception {
		getDriver().navigate().refresh();
	}
	
	public void back() throws Exception {
		getDriver().navigate().back();
	}
	
	public void forward() throws Exception {
		getDriver().navigate().forward();
	}

	public void close(){
		getDriver().quit();
	}

	public void waitForBody() throws Exception {
		waitForElementPresence(By.tagName("body"));
	}

	public void confirmAlertIfPresent() {
		AppiumDriver<MobileElement> d = getDriver();
		try{
			Alert alert = d.switchTo().alert();
			alert.accept();
			d.switchTo().defaultContent();
		} catch (Exception e){ // ignore
		}
	}
	
	// Windows related
	public String getCurrentWindow() {
		return getDriver().getWindowHandle();
	}
	
	public void switchToWindow(String windowHandle){
		getDriver().switchTo().window(windowHandle); 		
	}
	
	public void switchToNewWindow() {
		AppiumDriver driver = getDriver();
		String parentHandle = getCurrentWindow();
		for (String winHandle : driver.getWindowHandles()) {
			if (!winHandle.equals(parentHandle)) {
				switchToWindow(winHandle); // switch focus of WebDriver to the next found window handle (that's your newly opened window)
			}
		}
	}
	
	public void closeCurrentWindow(){
		getDriver().close();
	}
	
	public void switchToFrame(int index) throws Exception {
		this.getDriver().switchTo().frame(index);
	}

	public void switchToFrame(String name) throws Exception {
		this.getDriver().switchTo().frame(name);
	}

	@Override
	public void switchToFrame(MobileElement appiumElement) throws Exception{
		this.getDriver().switchTo().frame(appiumElement);
	}
	
	public void switchToDefaultFrame() throws Exception {
		this.getDriver().switchTo().defaultContent();
	}
	
	public TakesScreenshot getScreenshotAugmentedDriver(){
		return (TakesScreenshot) (new Augmenter().augment(getDriver()));
	}
	
	@Override
	public File takeScreenshot() throws Exception {
		TakesScreenshot augDriver = getScreenshotAugmentedDriver();
        File srcFile = augDriver.getScreenshotAs(OutputType.FILE);
        return FileSystemBatteries.moveFiletoDir(srcFile, Batteries.value(BatteriesPropertyType.DIRECTORY_SCREENSHOTS).asString());
	}
	
	public void focusOnApp() throws Exception{
		
	}
	

	/**********************************************************************************/
	/*					ELEMENT API													*/
	/**********************************************************************************/

	public MobileElement findElement(By findBy) throws Exception{
		waitForElementPresence(findBy);
		MobileElement element = getDriver().findElement(findBy);
		return element;
	}
	
	public List<MobileElement> findElements(By findBy) throws Exception{
		waitForElementPresence(findBy);
		List<MobileElement> elements = getDriver().findElements(findBy);
		return elements;
	}
	

	@Override
	public void waitForElementPresence(By findBy) throws Exception {
		getWaiter().until(ExpectedConditions.presenceOfElementLocated(findBy));
	}
	
	@Override
	public void waitForElementAbsence(By findBy) throws Exception {
		try{
			getWaiter().until(ExpectedConditions.presenceOfElementLocated(findBy));
			throw new Exception("Not able to establish absence of element after polling for same.");
		} catch (Exception e){
			// Do nothing.
		}
	}
	
	public void waitForElementClickability(By findBy) throws Exception {
		getWaiter().until(ExpectedConditions.elementToBeClickable(findBy));
	}
	
	public void waitForElementClickability(WebElement element) throws Exception {
		getWaiter().until(ExpectedConditions.elementToBeClickable(element));
	}

	@Override
	public void waitForElementVisibility(By findBy) throws Exception {
		getWaiter().until(ExpectedConditions.visibilityOfElementLocated(findBy));
	}

	@Override
	public void waitForElementInvisibility(By findBy) throws Exception {
		getWaiter().until(ExpectedConditions.invisibilityOfElementLocated(findBy));
	}
	
	@Override
	public boolean isElementPresent(By findBy) {
		try {
			waitForElementPresence(findBy);
			return true;
		} catch ( Exception e){
			return false;
		}
		
	}

	@Override
	public boolean isElementAbsent(By findBy) {
		try {
			waitForElementAbsence(findBy);
			return true;
		} catch ( Exception e){
			return false;
		}
		
	}
	
	@Override
	public boolean isElementVisible(By findBy) {
		try {
			waitForElementVisibility(findBy);
			return true;
		} catch ( Exception e){
			return false;
		}
		
	}
	
	@Override
	public boolean isElementInvisible(By findBy) {
		try {
			waitForElementInvisibility(findBy);
			return true;
		} catch ( Exception e){
			return false;
		}
		
	}
	/* Element Basic Actions */
	
	
	public void focus(MobileElement wdElement) throws Exception {
		wdElement.sendKeys("");
	}
	
	public boolean isSelected(MobileElement wdElement){
		return wdElement.isSelected();
	}
	
	public void click(MobileElement wdElement) throws Exception {
		waitForElementClickability(wdElement);
		try{
			wdElement.click();
		} catch (Exception f) {
			focus(wdElement);
			wdElement.sendKeys(Keys.ENTER);
		}	
	}

	public MobileElement click(By findBy) throws Exception {
		MobileElement wdElement = findElement(findBy);
		click(wdElement);
		return wdElement;
	}
	
	public MobileElement clickIfPresent(By findBy) {
		try{
			return click(findBy);
		} catch (Exception e){
			//pass
		}
		return null;
	}
	
	public void clickIfNotSelected(MobileElement wdElement) {
		if ((wdElement != null) && (!isSelected(wdElement))){
			wdElement.click();
		}
	}

	public void enterText(MobileElement wdElement, String value) throws Exception {
		waitForElementClickability(wdElement);
		wdElement.click();
		wdElement.sendKeys(value);
	}

	public void setText(MobileElement wdElement, String text) throws Exception {
		this.waitForElementClickability(wdElement);
		wdElement.click();
		wdElement.clear();
		wdElement.sendKeys(text);
	}

	public void clearText(MobileElement wdElement) throws Exception {
		wdElement.clear();
	}
	
	public boolean isChecked(MobileElement wdElement){
		return isSelected(wdElement);
	}

	public void check(MobileElement wdElement) {
		if (!isChecked(wdElement)){
			wdElement.click();
		}
	}

	public void uncheck(MobileElement wdElement) throws Exception {
		if (isChecked(wdElement)){
			wdElement.click();
		}
	}

	public void toggle(MobileElement wdElement) throws Exception{
		wdElement.click();
	}

	/*
	 * Drop Down API
	 */
	public void selectDropDownLabel(Select selectElement, String text) {
		selectElement.selectByVisibleText(text);
	}

	public void selectDropDownValue(Select selectElement, String value) {
		selectElement.selectByValue(value);
	}

	public void selectDropDownOptionAtIndex(Select selectElement, int index) {
		selectElement.selectByIndex(index);
	}

	public boolean isDropDownSelectedText(Select selectElement, String text) {
		List<WebElement> selectedOptions = selectElement.getAllSelectedOptions();
		for (WebElement option: selectedOptions){
			if (option.getText().equals(text)) return true;
		}
		return false;
	}

	public boolean isDropDownSelectedValue(Select selectElement, String value) {
		List<WebElement> selectedOptions = selectElement.getAllSelectedOptions();
		for (WebElement option: selectedOptions){
			if (option.getAttribute("value").equals(value)) return true;
		}
		return false;
	}

	public boolean isDropDownSelectedIndex(Select selectElement, int index) {
		List<WebElement> options = selectElement.getOptions();
		return options.get(index).isSelected();
	}

	public ArrayList<String> getDropDownOptionLabels(Select selectControl) {
		ArrayList<String> texts = new ArrayList<String>();
		for (WebElement option: selectControl.getOptions()){
			texts.add(option.getText());
		}
		return texts;
	}
	
	public ArrayList<String> getDropDownOptionValues(Select selectControl) {
		ArrayList<String> texts = new ArrayList<String>();
		for (WebElement option: selectControl.getOptions()){
			texts.add(option.getAttribute("value"));
		}
		return texts;
	}
	
	public int getDropDownOptionCount(Select selectControl) {
		return selectControl.getOptions().size();
	}
	
	public Select convertToSelectElement(MobileElement element) throws Exception{
		return new Select(element);
	}
	
	/* 
	 * Radio Button API
	 */
	public MobileElement chooseElementBasedOnText(List<MobileElement> wdElements, String text) {
		for (MobileElement wdElement: wdElements){
			if (getText(wdElement).equals(text)){
				return wdElement;
			}
		}
		return null;
	}
	
	public MobileElement chooseElementBasedOnValue(List<MobileElement> wdElements, String value) throws Exception {
		for (MobileElement wdElement: wdElements){
			if (getValue(wdElement).equals(value)){
				return wdElement;
			}
		}
		return null;
	}
	
	public MobileElement getParent(MobileElement wdElement){
		return wdElement.findElement(By.xpath("parent::*")); 
	}
	
	public MobileElement chooseElementBasedOnParentText(List<MobileElement> wdElements, String text) {
		for (MobileElement wdElement: wdElements){
			MobileElement parent = getParent(wdElement);
			if (getText(parent).equals(text)){
				return wdElement;
			}
		}
		return null;
	}

	public boolean isSelectedText(List<MobileElement> wdElements, String text) {
		for (MobileElement wdElement: wdElements){
			if (getText(wdElement).equals(text)){
				return true;
			}
		}
		return false;
	}

	public boolean isSelectedValue(List<MobileElement> wdElements, String value) throws Exception {
		for (MobileElement wdElement: wdElements){
			if (getValue(wdElement).equals(value)){
				return true;
			}
		}
		return false;
	}

	public boolean isSelectedIndex(List<MobileElement> elements, int index) {
		return elements.get(index).isSelected();
	}

	public boolean isSelectedElementParentText(List<MobileElement> wdElements, String text) {
		for (MobileElement wdElement: wdElements){
			MobileElement parent = getParent(wdElement); 
			if (getText(parent).equals(text)){
				return true;
			}
		}
		return false;
	}

	public ArrayList<String> getRadioButtonLabels(List<MobileElement> wdElements) {
		ArrayList<String> texts = new ArrayList<String>();
		for (MobileElement option: wdElements){
			texts.add(getText(option));
		}
		return texts;
	}

	public ArrayList<String> getRadioButtonValues(List<MobileElement> wdElements) throws Exception {
		ArrayList<String> texts = new ArrayList<String>();
		for (MobileElement option: wdElements){
			texts.add(getValue(option));
		}
		return texts;
	}

	// Property API
	public String getText(MobileElement wdElement) {
		return wdElement.getText();
	}
	
	public String getValue(MobileElement wdElement) throws Exception {
		return wdElement.getAttribute("value");
	}

	public String getAttribute(MobileElement wdElement, String attr) throws Exception{
		return wdElement.getAttribute(attr);
	}

}
