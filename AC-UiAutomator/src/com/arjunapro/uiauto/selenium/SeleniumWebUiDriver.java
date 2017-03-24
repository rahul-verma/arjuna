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
package com.arjunapro.uiauto.selenium;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.Proxy;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.remote.Augmenter;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.safari.SafariDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import com.arjunapro.sysauto.batteries.FileSystemBatteries;
import com.arjunapro.sysauto.batteries.SystemBatteries;
import com.arjunapro.testauto.enums.Browser;
import com.arjunapro.uiauto.enums.ElementLoaderType;
import com.arjunapro.uiauto.enums.UiAutomationContext;
import com.arjunapro.uiauto.enums.UiDriverEngine;
import com.arjunapro.uiauto.enums.UiElementType;
import com.arjunapro.uiauto.interfaces.UiElement;

import pvt.arjunapro.enums.BatteriesPropertyType;
import pvt.batteries.config.Batteries;
import pvt.selenium.api.WDMediator;
import pvt.selenium.lib.base.DefaultSeleniumMediator;
import pvt.uiautomator.api.ElementMetaData;
import pvt.uiautomator.api.Identifier;
import pvt.uiautomator.api.identify.enums.WebIdentifyBy;
import pvt.uiautomator.lib.DefaultUiDriver;
import pvt.uiautomator.lib.DefaultUiElement;
import pvt.uiautomator.lib.config.UiAutomatorPropertyType;

public class SeleniumWebUiDriver extends DefaultUiDriver implements SeleniumUiDriver {
	
	private WebDriver driver = null;
	private WebDriverWait waiter = null;
	private Browser browser = null;
	private int waitTime = -1;
	DesiredCapabilities capabilities = null;
	
	public SeleniumWebUiDriver(ElementLoaderType loaderType) throws Exception{
		super(UiAutomationContext.PC_WEB, loaderType);
		initDriver();
		switch (this.getBrowser()){
		case FIREFOX:
			setDriver(getFirefoxDriver());
			break;
		case CHROME:
			setDriver(getChromeDriver());
			break;
		case SAFARI:
			setDriver(getSafariDriver());
			break;
		default:; 
		}
		initWait();
		maximizeWindow();
	}
	
	public SeleniumWebUiDriver() throws Exception{
		this(ElementLoaderType.AUTOMATOR);
	}

	public void maximizeWindow(){
		// Check for some property here. To override this default.
		getDriver().manage().window().maximize();	
	}

	public DesiredCapabilities getFireFoxCapabilitiesSkeleton() { 
		return DesiredCapabilities.firefox();
	}

	public DesiredCapabilities getChromeCapabilitiesSkeleton() {
		return DesiredCapabilities.chrome();
	}

	public DesiredCapabilities getSafariCapabilitiesSkeleton() {
		return DesiredCapabilities.safari();
	}

	public WebDriver getFirefoxDriver() throws Exception {
		this.setAppTitle(Batteries.value(UiAutomatorPropertyType.FIREFOX_WINDOWNAME).asString());
		capabilities = getFireFoxCapabilitiesSkeleton();
		//driver = new FirefoxDriver(capabilities);
		FirefoxProfile profile = new FirefoxProfile();
		profile.setEnableNativeEvents(true);
		capabilities.setCapability(FirefoxDriver.PROFILE, profile);
		setCapabilities(capabilities);
		return new FirefoxDriver(capabilities);
	}

	public WebDriver getChromeDriver() throws Exception {
		this.setAppTitle(Batteries.value(UiAutomatorPropertyType.CHROME_WINDOWNAME).asString());
		String os = SystemBatteries.getOSName();
		String chromeDriverBinaryName = null;
		if (os.startsWith("Window")){
			chromeDriverBinaryName = "chromedriver.exe";
		} else if (os.startsWith("Mac")) {
			chromeDriverBinaryName = "chromedriver";
		}
		System.setProperty("webdriver.chrome.driver", Batteries.value(UiAutomatorPropertyType.DIRECTORY_TOOLS_UIDRIVERS).asString() + "/" + chromeDriverBinaryName);
		capabilities = getChromeCapabilitiesSkeleton();
		setCapabilities(capabilities);
		return new ChromeDriver(capabilities);
	}

	public WebDriver getSafariDriver() throws Exception {
		this.setAppTitle(Batteries.value(UiAutomatorPropertyType.SAFARI_WINDOWNAME).asString());
		capabilities = getSafariCapabilitiesSkeleton();
		setCapabilities(capabilities);
		return new SafariDriver(capabilities);
	}

	public void initDriver() throws Exception {
		this.setBrowser(Browser.valueOf(Batteries.value(UiAutomatorPropertyType.BROWSER_PC_DEFAULT).asString().toUpperCase()));
		this.setWaitTime(Batteries.value(UiAutomatorPropertyType.BROWSER_PC_MAXWAIT).asInt());
		this.setUiTestEngineName(UiDriverEngine.WEBDRIVER);		
	}

	public void initWait() {
		this.setWaiter(new WebDriverWait(this.getDriver(), getWaitTime()));
		if(this.getBrowser() != Browser.SAFARI){
			getDriver().manage().timeouts().pageLoadTimeout(getWaitTime(), TimeUnit.SECONDS);
		}	
	}

	public WebDriver getDriver() {
		return driver;
	}

	public void setDriver(WebDriver driver) {
		this.driver = driver;
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

	public void setCapabilities(DesiredCapabilities capabilities) throws Exception {
		if (Batteries.value(UiAutomatorPropertyType.BROWSER_PC_PROXY_ON).asBoolean()){
			Proxy proxy = new Proxy();
			String p = Batteries.value(UiAutomatorPropertyType.BROWSER_PC_PROXY_HOST).asString() + ":" + Batteries.value(UiAutomatorPropertyType.BROWSER_PC_PROXY_PORT).asString();
			setHttpProxy(proxy, p);
			setSslProxy(proxy, p);
			capabilities.setCapability("proxy", proxy);
		}
	}

	public void setHttpProxy(Proxy proxy, String proxyString) {
		proxy.setHttpProxy(proxyString);
	}

	public void setSslProxy(Proxy proxy, String proxyString) {
		proxy.setSslProxy(proxyString);
	}

	/**********************************************************************************/

	@Override
	public UiElement declareElement(ElementMetaData elementMetaData) throws Exception {
		UiElement uiElement = createDefaultElementSkeleton(elementMetaData);
		ArrayList<By> finderQueue = new ArrayList<By>();
		for (Identifier id: elementMetaData.getIdentifiers()){
				finderQueue.add(getFinderType(id.NAME, id.VALUE));
		}
		
		WDMediator mediator = createMediatorSkeleton(uiElement);
		uiElement.setMediator(mediator);
		uiElement.setLoaderType(this.getElementLoaderType());
		mediator.setFindersQueue(finderQueue);
		mediator.setAutomatorName(Batteries.getComponentName("WEBDRIVER_AUTOMATOR"));
		return uiElement;
	}

	@SuppressWarnings("incomplete-switch")
	public By getFinderType(String identifier, String idValue) throws Exception {
		By findBy = null;
		WebIdentifyBy idType = null;
		try{
			idType = WebIdentifyBy.valueOf(identifier.toUpperCase());
		} catch (Throwable e){
			throwUnsupportedIndentifierException(
					Batteries.getComponentName("WEBDRIVER_AUTOMATOR"),
					"getFinderType",
					identifier);
		}
		switch(idType){
		case ID: findBy = By.id(idValue); break;
		case NAME: findBy = By.name(idValue); break;
		case CLASS: findBy = By.className(idValue); break;
		case LINK_TEXT: findBy = By.linkText(idValue); break;
		case PARTIAL_LINK_TEXT: findBy = By.partialLinkText(idValue); break;
		case XPATH: findBy = By.xpath(idValue); break;
		case CSS: findBy = By.cssSelector(idValue); break;
		case TAG: findBy = By.tagName(idValue); break;
		}
		return findBy;
	}

	public UiElementType getElementType(WebElement wdElement) {
		String tagName = wdElement.getTagName().toLowerCase();
		if (tagName.equals("select")){
			return UiElementType.DROPDOWN;
		} else if (tagName.equals("input") && wdElement.getAttribute("type").toLowerCase().equals("radio") ){
			return UiElementType.RADIO;
		} else {
			return UiElementType.GENERIC;
		}
	}

	public TakesScreenshot getScreenshotAugmentedDriver() {
		return (TakesScreenshot) (new Augmenter().augment(getDriver()));
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
		WebDriver d = getDriver();
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
		WebDriver driver = getDriver();
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
	public void switchToFrame(WebElement wdElement) throws Exception{
		this.getDriver().switchTo().frame(wdElement);
	}
	
	public void switchToDefaultFrame() throws Exception {
		this.getDriver().switchTo().defaultContent();
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
	
	// FINDIND RELATED
	public WebElement findElement(By findBy) throws Exception{
		waitForElementPresence(findBy);
		WebElement element = getDriver().findElement(findBy);
		return element;
	}
	
	public List<WebElement> findElements(By findBy) throws Exception{
		waitForElementPresence(findBy);
		List<WebElement> elements = getDriver().findElements(findBy);
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
	
	public void focus(WebElement wdElement) throws Exception {
		wdElement.sendKeys("");
	}
	
	public boolean isSelected(WebElement wdElement){
		return wdElement.isSelected();
	}
	
	public void click(WebElement wdElement) throws Exception {
		waitForElementClickability(wdElement);
		try{
			wdElement.click();
		} catch (Exception f) {
			focus(wdElement);
			wdElement.sendKeys(Keys.ENTER);
		}	
	}

	public WebElement click(By findBy) throws Exception {
		WebElement wdElement = findElement(findBy);
		click(wdElement);
		return wdElement;
	}
	
	public WebElement clickIfPresent(By findBy) {
		try{
			return click(findBy);
		} catch (Exception e){
			//pass
		}
		return null;
	}
	
	public void clickIfNotSelected(WebElement wdElement) {
		if ((wdElement != null) && (!isSelected(wdElement))){
			wdElement.click();
		}
	}

	public void enterText(WebElement wdElement, String value) throws Exception {
		waitForElementClickability(wdElement);
		wdElement.click();
		wdElement.sendKeys(value);
	}

	public void setText(WebElement wdElement, String text) throws Exception {
		this.waitForElementClickability(wdElement);
		wdElement.click();
		wdElement.clear();
		wdElement.sendKeys(text);
	}

	public void clearText(WebElement wdElement) throws Exception {
		wdElement.clear();
	}
	
	public boolean isChecked(WebElement wdElement){
		return isSelected(wdElement);
	}

	public void check(WebElement wdElement) {
		if (!isChecked(wdElement)){
			wdElement.click();
		}
	}

	public void uncheck(WebElement wdElement) throws Exception {
		if (isChecked(wdElement)){
			wdElement.click();
		}
	}

	public void toggle(WebElement wdElement) throws Exception{
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
	
	public Select convertToSelectElement(WebElement element) throws Exception{
		return new Select(element);
	}
	
	/* 
	 * Radio Button API
	 */
	public WebElement chooseElementBasedOnText(List<WebElement> wdElements, String text) {
		for (WebElement wdElement: wdElements){
			if (getText(wdElement).equals(text)){
				return wdElement;
			}
		}
		return null;
	}
	
	public WebElement chooseElementBasedOnValue(List<WebElement> wdElements, String value) throws Exception {
		for (WebElement wdElement: wdElements){
			if (getValue(wdElement).equals(value)){
				return wdElement;
			}
		}
		return null;
	}
	
	public WebElement getParent(WebElement wdElement){
		return wdElement.findElement(By.xpath("parent::*")); 
	}
	
	public WebElement chooseElementBasedOnParentText(List<WebElement> wdElements, String text) {
		for (WebElement wdElement: wdElements){
			WebElement parent = getParent(wdElement);
			if (getText(parent).equals(text)){
				return wdElement;
			}
		}
		return null;
	}

	public boolean isSelectedText(List<WebElement> wdElements, String text) {
		for (WebElement wdElement: wdElements){
			if (getText(wdElement).equals(text)){
				return true;
			}
		}
		return false;
	}

	public boolean isSelectedValue(List<WebElement> wdElements, String value) throws Exception {
		for (WebElement wdElement: wdElements){
			if (getValue(wdElement).equals(value)){
				return true;
			}
		}
		return false;
	}

	public boolean isSelectedIndex(List<WebElement> elements, int index) {
		return elements.get(index).isSelected();
	}

	public boolean isSelectedElementParentText(List<WebElement> wdElements, String text) {
		for (WebElement wdElement: wdElements){
			WebElement parent = getParent(wdElement); 
			if (getText(parent).equals(text)){
				return true;
			}
		}
		return false;
	}

	public ArrayList<String> getRadioButtonLabels(List<WebElement> wdElements) {
		ArrayList<String> texts = new ArrayList<String>();
		for (WebElement option: wdElements){
			texts.add(getText(option));
		}
		return texts;
	}

	public ArrayList<String> getRadioButtonValues(List<WebElement> wdElements) throws Exception {
		ArrayList<String> texts = new ArrayList<String>();
		for (WebElement option: wdElements){
			texts.add(getValue(option));
		}
		return texts;
	}
	
	// Property API
	public String getText(WebElement wdElement) {
		return wdElement.getText();
	}
	
	public String getValue(WebElement wdElement) throws Exception {
		return wdElement.getAttribute("value");
	}

	public String getAttribute(WebElement wdElement, String attr) throws Exception{
		return wdElement.getAttribute(attr);
	}
	
	// Action chain actions	
	
	public Actions getActionChain(){
		return new Actions(getDriver());
	}
	
	public void moveToElementAndClick(WebElement element) throws Exception{
		Actions builder = getActionChain();
		builder.moveToElement(element).click(element).perform();
	}
	
	public void hover(By findBy) throws Exception {
		Actions builder = getActionChain();
		WebElement element = findElement(findBy);
		builder.moveToElement(element).perform();
	}
	
	@Override
	public void hover(WebElement element) throws Exception {
		Actions builder = getActionChain();
		builder.moveToElement(element).perform();
	}
	
	public void hoverAndClick(WebElement element) throws Exception {
		try {
			Actions builder = getActionChain();
			builder.moveToElement(element).perform();
			getWaiter().until(ExpectedConditions.elementToBeClickable(element));
			element.click();			
		} catch (Exception e){
			moveToElementAndClick(element);
		}
	}
	
	public void hoverAndClick(By finder1, By finder2) throws Exception {
		Actions builder =  null;
		try {
			builder = getActionChain();
			builder.moveToElement(findElement(finder1)).perform();
			getWaiter().until(ExpectedConditions.elementToBeClickable(finder2));
			findElement(finder2).click();
		} catch (Exception e){
			builder = getActionChain();
			builder.moveToElement(findElement(finder1)).click(findElement(finder2)).perform();
		}
	}
	
	@Override
	public void rightClick(WebElement element) throws Exception{
		Actions builder = getActionChain();
		builder.contextClick(element).perform();
	}
	
	public void rightClickAndClick(By finder1, By finder2) throws Exception {
		rightClick(findElement(finder1));
		click(findElement(finder2));
	}

	public WDMediator createMediatorSkeleton(UiElement element) throws Exception {
		return new DefaultSeleniumMediator(this, element);
	}
	
	public UiElement createDefaultElementSkeleton(ElementMetaData elementMetaData) throws Exception {
		return new DefaultUiElement(elementMetaData);
	}
	
}
