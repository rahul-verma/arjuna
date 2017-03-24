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
package pvt.uiautomator.lib.config;

import java.util.ArrayList;
import java.util.HashMap;

import com.arjunapro.sysauto.batteries.DataBatteries;

import pvt.uiauto.enums.AppiumAndroidBrowserType;
import pvt.uiauto.enums.AppiumIosBrowserType;
import pvt.uiauto.enums.AppiumMobilePlatformType;
import pvt.uiauto.enums.IdentifyBy;
import pvt.uiauto.enums.MobileNativeIdentifyBy;
import pvt.uiauto.enums.MobileWebIdentifyBy;
import pvt.uiauto.enums.NativeIdentifyBy;
import pvt.uiauto.enums.ScreenIdentifyBy;
import pvt.uiauto.enums.UiAutomationContext;
import pvt.uiauto.enums.UiElementType;
import pvt.uiauto.enums.WebIdentifyBy;
import pvt.uiautomator.api.CentralPageMap;
import pvt.uiautomator.lib.DefaultCentralUiMap;

public enum UiAutomatorSingleton {
	INSTANCE;

	CentralPageMap uicentralMap = new DefaultCentralUiMap();
	// UI Automator
	private static ArrayList<String> allowedGenericIdentifiers = null;
	private static ArrayList<String> allowedWebIdentifiers = null;
	private static ArrayList<String> allowedNativeIdentifiers = null;
	private static ArrayList<String> allowedMobileWebIdentifiers = null;
	private static ArrayList<String> allowedMobileNativeIdentifiers = null;
	private static ArrayList<String> allowedScreenIdentifiers = null;
	private static ArrayList<String> allAllowedUiElementTypes = null;
	private static HashMap<UiAutomationContext, String> automationContextNames = null;
	// Appium
	private static ArrayList<String> allowedAppiumPlatforms = new ArrayList<String>();;
	private static ArrayList<String> allowedAppiumAndroidBrowsers = new ArrayList<String>();;
	private static ArrayList<String> allowedAppiumIosBrowsers = new ArrayList<String>();

	public void init() throws Exception{
		/* Appium */
		for (AppiumMobilePlatformType prop: AppiumMobilePlatformType.class.getEnumConstants()){
			allowedAppiumPlatforms.add(prop.toString());
		}

		for (AppiumAndroidBrowserType prop: AppiumAndroidBrowserType.class.getEnumConstants()){
			allowedAppiumAndroidBrowsers.add(prop.toString());
		}

		for (AppiumIosBrowserType prop: AppiumIosBrowserType.class.getEnumConstants()){
			allowedAppiumIosBrowsers.add(prop.toString());
		}

		/* UI Automator */
		automationContextNames = new HashMap<UiAutomationContext, String>();
		automationContextNames.put(UiAutomationContext.PC_WEB, "PC Web");
		automationContextNames.put(UiAutomationContext.PC_NATIVE, "PC Native");
		automationContextNames.put(UiAutomationContext.MOBILE_WEB, "Mobile Web");
		automationContextNames.put(UiAutomationContext.MOBILE_NATIVE, "Mobile Native");
		automationContextNames.put(UiAutomationContext.SCREEN, "Screen");
		automationContextNames.put(UiAutomationContext.GENERIC, "Generic");

		allowedGenericIdentifiers = new ArrayList<String>();
		for (IdentifyBy prop: IdentifyBy.class.getEnumConstants()){
			allowedGenericIdentifiers.add(prop.toString());
		}

		allAllowedUiElementTypes = new ArrayList<String>();
		for (UiElementType prop: UiElementType.class.getEnumConstants()){
			allAllowedUiElementTypes.add(prop.toString());
		}

		allowedScreenIdentifiers = new ArrayList<String>();
		for (ScreenIdentifyBy prop: ScreenIdentifyBy.class.getEnumConstants()){
			allowedScreenIdentifiers.add(prop.toString());
		}

		allowedNativeIdentifiers = new ArrayList<String>();
		for (NativeIdentifyBy prop: NativeIdentifyBy.class.getEnumConstants()){
			allowedNativeIdentifiers.add(prop.toString());
		}

		allowedMobileNativeIdentifiers = new ArrayList<String>();
		for (MobileNativeIdentifyBy prop: MobileNativeIdentifyBy.class.getEnumConstants()){
			allowedMobileNativeIdentifiers.add(prop.toString());
		}

		allowedWebIdentifiers = new ArrayList<String>();
		for (WebIdentifyBy prop: WebIdentifyBy.class.getEnumConstants()){
			allowedWebIdentifiers.add(prop.toString());
		}

		allowedMobileWebIdentifiers = new ArrayList<String>();
		for (MobileWebIdentifyBy prop: MobileWebIdentifyBy.class.getEnumConstants()){
			allowedMobileWebIdentifiers.add(prop.toString());		
		}
	}

	/*
	 * UI Automator
	 */

	public String getAutomationContextName(UiAutomationContext type) {
		return automationContextNames.get(type);
	}

	public ArrayList<String> getAllowedGenericIdentifiers(){
		return allowedGenericIdentifiers;
	}

	public ArrayList<String> getAllAllowedUiElementTypes(){
		return allAllowedUiElementTypes;
	}

	public ArrayList<String> getAllowedScreenIdentifiers(){
		return allowedScreenIdentifiers;
	}

	public ArrayList<String> getAllowedNativeIdentifiers() {
		return allowedNativeIdentifiers;
	}

	public ArrayList<String> getAllowedMobileNativeIdentifiers() {
		return allowedMobileNativeIdentifiers;
	}

	public ArrayList<String> getAllowedWebIdentifiers() {
		return allowedWebIdentifiers;
	}

	public ArrayList<String> getAllowedMobileWebIdentifiers() {
		return allowedMobileWebIdentifiers;
	}

	public ArrayList<String> getAllowedIdentifiers(UiAutomationContext context) throws Exception{
		switch(context){
		case PC_WEB: return getAllowedWebIdentifiers();
		case PC_NATIVE: return getAllowedNativeIdentifiers();
		case MOBILE_WEB: return getAllowedMobileWebIdentifiers();
		case MOBILE_NATIVE: return getAllowedMobileNativeIdentifiers();
		case SCREEN: return getAllowedScreenIdentifiers();
		case GENERIC: return getAllowedGenericIdentifiers();
		default: throw new Exception("Unknown id context.");
		}
	}
	
	/*
	 * Appium Inquiry Methods
	 */

	private ArrayList<String> getAllowedPlatformsForAppium(){
		return allowedAppiumPlatforms;
	}

	private ArrayList<String> getAllowedBrowsersForAppium(AppiumMobilePlatformType platform) throws Exception{
		switch (platform){
		case ANDROID: return allowedAppiumAndroidBrowsers;
		case IOS: return allowedAppiumIosBrowsers;
		default: throw new Exception("Unknown platform: " + platform);
		}
	}

	public boolean isAllowedAppiumPlatform(String platformName){
		return getAllowedPlatformsForAppium().contains(platformName.toUpperCase());
	}

	public boolean isAllowedAppiumBrowser(AppiumMobilePlatformType platform, String browserName) throws Exception{
		return getAllowedBrowsersForAppium(platform).contains(browserName.toUpperCase());
	}

	public String getAppiumPlatformString(AppiumMobilePlatformType platform) throws Exception{
		switch(platform){
		case ANDROID: return "Android";
		case IOS: return "iOS";
		default: return platform.toString();
		}
	}

	public String getAppiumBrowserString(String rawName) throws Exception{
		return DataBatteries.toTitleCase(rawName);
	}

	public CentralPageMap getCentralMap() {
		return this.uicentralMap;
	}

}
