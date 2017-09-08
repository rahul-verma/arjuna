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
package pvt.arjunasdk.appium.lib.base;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

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

import arjunasdk.enums.Browser;
import arjunasdk.sysauto.batteries.FileSystemBatteries;
import arjunasdk.uiauto.interfaces.AppiumUiDriver;
import arjunasdk.uiauto.interfaces.UiElement;
import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.ios.IOSDriver;
import io.appium.java_client.remote.MobileCapabilityType;
import pvt.arjunasdk.appium.api.AppiumMediator;
import pvt.arjunasdk.enums.BatteriesPropertyType;
import pvt.arjunasdk.uiauto.api.ElementMetaData;
import pvt.arjunasdk.uiauto.api.Identifier;
import pvt.arjunasdk.uiauto.enums.AppiumMobilePlatformType;
import pvt.arjunasdk.uiauto.enums.ElementLoaderType;
import pvt.arjunasdk.uiauto.enums.MobileWebIdentifyBy;
import pvt.arjunasdk.uiauto.enums.UiAutomationContext;
import pvt.arjunasdk.uiauto.enums.UiAutomatorPropertyType;
import pvt.arjunasdk.uiauto.enums.UiDriverEngine;
import pvt.arjunasdk.uiauto.enums.UiElementType;
import pvt.arjunasdk.uiautomator.UiAutomator;
import pvt.arjunasdk.uiautomator.lib.DefaultUiDriver;
import pvt.arjunasdk.uiautomator.lib.DefaultUiElement;
import pvt.batteries.config.Batteries;
import pvt.batteries.exceptions.Problem;

public abstract class AbstractAppiumUiDriver extends DefaultUiDriver implements AppiumUiDriver {

	private AppiumDriver<MobileElement> driver = null;
	private WebDriverWait waiter = null;
	private Browser browser = null;
	private int waitTime = -1;
	private String appPath = null;
	UiAutomationContext context = null;
	private DesiredCapabilities capabilities = null;
	private AppiumMobilePlatformType platformType = null;
	
	public AbstractAppiumUiDriver() throws Exception{
		super(UiAutomationContext.MOBILE_WEB, ElementLoaderType.AUTOMATOR);
	}
//
//	public AbstractAppiumUiDriver(String appPath, UiAutomationContext context, ElementLoaderType loaderType) throws Exception{
//		super(context, loaderType);
//		if (appPath == null){
//			throw new Exception("Null value supplied for appPath");
//		}
//	}
//	
//	public AbstractAppiumUiDriver(String appPath) throws Exception{
//		this(appPath, UiAutomationContext.MOBILE_NATIVE, ElementLoaderType.AUTOMATOR);
//	}
//	
//	public AbstractAppiumUiDriver(UiAutomationContext context, ElementLoaderType loaderType) throws Exception{
//		super(context, loaderType);
//	}
	
	private AppiumMediator createMediatorSkeleton(UiElement element) throws Exception {
		return new DefaultAppiumMediator(this, element);
	}
	
	private UiElement createDefaultElementSkeleton(ElementMetaData elementMetaData) throws Exception {
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

	@Override
	public void init() throws Exception{
		this.setUiTestEngineName(UiDriverEngine.APPIUM);
	}
	
	@Override
	public void setCapabilities(Map<String,?> caps){
		this.capabilities = new DesiredCapabilities(caps);
	}
	
	@Override
	public void load() throws Exception{
		URL hubUrl = new URL(
				String.format(
						Batteries.value(UiAutomatorPropertyType.APPIUM_HUB_URL).asString(),
						Batteries.value(UiAutomatorPropertyType.APPIUM_HUB_HOST).asString(),
						Batteries.value(UiAutomatorPropertyType.APPIUM_HUB_PORT).asString()
						)
				);
		try{
			switch(getPlatformType()){
			case ANDROID: driver = new AndroidDriver<MobileElement>(hubUrl, capabilities); break;
			case IOS: driver = new IOSDriver<MobileElement>(hubUrl, capabilities); break;
			}
	
		}catch (UnreachableBrowserException e){
			throwUnreachableBrowserException(getPlatformType(), e);
		}
		this.setWaiter(new WebDriverWait(this.getDriver(), this.getWaitTime()));		
	}
	
	protected void setAutomationContext(UiAutomationContext context) {
		this.context = context;
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
		List<By> finderQueue = new ArrayList<By>();
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
	 **********************************************************************************/

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
        return FileSystemBatteries.moveFiletoDir(srcFile, Batteries.value(BatteriesPropertyType.DIRECTORY_PROJECT_SCREENSHOTS).asString());
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

	public List<String> getDropDownOptionLabels(Select selectControl) {
		List<String> texts = new ArrayList<String>();
		for (WebElement option: selectControl.getOptions()){
			texts.add(option.getText());
		}
		return texts;
	}
	
	public List<String> getDropDownOptionValues(Select selectControl) {
		List<String> texts = new ArrayList<String>();
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

	public List<String> getRadioButtonLabels(List<MobileElement> wdElements) {
		List<String> texts = new ArrayList<String>();
		for (MobileElement option: wdElements){
			texts.add(getText(option));
		}
		return texts;
	}

	public List<String> getRadioButtonValues(List<MobileElement> wdElements) throws Exception {
		List<String> texts = new ArrayList<String>();
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

	private AppiumMobilePlatformType getPlatformType() {
		return platformType;
	}

	@Override
	public void setPlatformType(AppiumMobilePlatformType platformType) {
		this.platformType = platformType;
	}

}
