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
package com.autocognite.pvt.uiautomator;

import java.util.ArrayList;

import com.autocognite.arjuna.uiauto.enums.UiAutomationContext;
import com.autocognite.arjuna.uiauto.plugins.appium.AppiumMobilePlatformType;
import com.autocognite.pvt.batteries.integration.ComponentConfigurator;
import com.autocognite.pvt.uiautomator.lib.config.UiAutomatorConfigurator;
import com.autocognite.pvt.uiautomator.lib.config.UiAutomatorSingleton;

public class UiAutomator {
	
	public static void init() throws Exception{
		UiAutomatorSingleton.INSTANCE.init();
	}
	
	public static String getAutomationContextName(UiAutomationContext context) {
		return UiAutomatorSingleton.INSTANCE.getAutomationContextName(context);
	}

	public static ArrayList<String> getAllowedIdentifiers(UiAutomationContext identificationContext) throws Exception {
		return UiAutomatorSingleton.INSTANCE.getAllowedIdentifiers(identificationContext) ;
	}

	public static ArrayList<String> getAllAllowedUiElementTypes() {
		return UiAutomatorSingleton.INSTANCE.getAllAllowedUiElementTypes();
	}
	
	public static String getComponentName(){
		return "UI Automator";
	}
	
	public static boolean isAllowedAppiumPlatform(String platformName){
		return UiAutomatorSingleton.INSTANCE.isAllowedAppiumPlatform(platformName);
	}
	
	public static String getAppiumPlatformString(AppiumMobilePlatformType platform) throws Exception{
		return UiAutomatorSingleton.INSTANCE.getAppiumPlatformString(platform);
	}
	
	public static String getAppiumBrowserString(String rawName) throws Exception{
		return UiAutomatorSingleton.INSTANCE.getAppiumBrowserString(rawName);
	}

	public static boolean isAllowedAppiumBrowser(AppiumMobilePlatformType platform, String browser) throws Exception {
		return UiAutomatorSingleton.INSTANCE.isAllowedAppiumBrowser(platform, browser);
	}
	public static class problem{
		/* Appium */
		public static final String APPIUM_UNSUPPORTED_PLATFORM = "problem.appium.unsupported.platform";
		public static final String APPIUM_UNSUPPORTED_BROWSER = "problem.appium.unsupported.browser";	
		public static final String APPIUM_UNREACHABLE_BROWSER = "problem.appium.unreachablebrowser";
		
		/* UI Automator */
		public static final String ELEMENT_IDENTIFICATION_FAILURE = "problem.uiauto.identification.failure";
		public static final String ELEMENT_GET_INSTANCE_FAILURE = "problem.uiauto.getinstance.failure";

		public static final String ELEMENT_WAIT_FAILURE = "problem.uiauto.wait.failure";
		
		public static final String ELEMENT_ACTION_FAILURE = "problem.uiauto.action.failure";
		public static final String ELEMENT_GET_ATTR_FAILURE = "problem.uiauto.getattr.failure";
		
		public static final String ACTION_MULTIELEMENT_FAILURE = "problem.uiauto.action.multielement.failure";
		public static final String ELEMENT_UNSUPPORTED_ACTION = "problem.uiauto.action.unsupported";
		public static final String ELEMENT_INQUIRY_FAILURE = "problem.uiauto.inquiry.failure";
		public static final String PAGE_NULL_AUTOMATOR = "problem.ui.nullautomator";
		public static final String PAGE_UNDEFINED_ELEMENT = "problem.uientity.undefinedelement";
		public static final String COMPOSITE_PAGE_CONSTRUCTOR_NULL_AUTOMATOR = "problem.genericuientity.constructor.nullautomator";
		public static final String COMPOSITE_PAGE_GET_AUTOMATOR_NULL = "problem.genericuientity.getautomator.null";
		public static final String MAPFILE_RELATIVE_PATH = "problem.uimap.file.relativepath";
		public static final String MAPFILE_NOT_FOUND = "problem.uimap.file.notfound";
		public static final String MAPFILE_NOTAFILE = "problem.uimap.file.notafile";
		public static final String APP_MAP_DIR_NOT_A_DIR = "problem.uimap.dir.notadirectory";
		public static final String UNSUPPORTED_IDENTIFIER = "problem.uiauto.identifier.unsupported";
		public static final String UNSUPPORTED_MULTIPLE_IDENTIFIERS = "problem.uiauto.identifiers.combination.unsupported";
		public static final String HYBRID_NULL_AUTOMATOR = "problem.uientity.hybrid.nullautomator";
		
		// NEW CODES
		public static final String UI_ELEMENT_INVALID_METADATA = "problem.uielement.invalid.metadata";
		public static final String LOCALIZER_NOT_INITIALIZED = "problem.localizer.not.initialized";
		public static final String PROPERTY_DOES_NOT_EXIST = "problem.propmanager.notaproperty";
		public static final String UNSUPPORTED_MAP_FILE_FORMAT = "problem.uimapper.unsupported.fileformat";
		public static final String WRAPPER_AUTOMATOR_NULL_DEFAULT_AUTOMATOR = "problem.wrapperautomator.nulldefault";
		public static final String AUTOMATOR_UNSUPPORTED_ACTION = "problem.automator.unsupportedaction";
		public static final String COMPOSITE_PAGE_NULL_AUTOMATOR = "problem.entity.nullautomator";
		public static final String UIENTITY_DISALLOWED_LABEL = "problem.entity.uilabel.disallowed";
		public static final String COMPOSITE_PAGE_NONEXISTING_LABEL = "problem.entity.uilabel.nonexisting";
		public static final String COMPOSITE_PAGE_NULL_LABEL = "problem.entity.uilabel.null";
		public static final String UI_NULL_ELEMENT = "problem.ui.element.null";
		public static final String FACTORY_AUTOMATOR_MOBILE_NULL_APP_PATH = "problem.factory.automator.mobile.nullapppath";
		public static final String FACTORY_AUTOMATOR_UNSUPPORTED_CONTEXT = "problem.factory.automator.unsupportedcontext";
		public static final String FACTORY_METHOD_APPPATH_NOT_APPLICABLE = "problem.factory.apppath.methodnotapplicable";
		public static final String UIAUTO_CONTEXT_HANDLER_NO_AUTO_FOR_LABEL = "problem.uicontexthandler.absentautolabel";
		public static final String UIAUTO_CONTEXT_HANDLER_NULL_AUTOMATOR = "problem.uicontexthandler.nullautomator";
		public static final String UIAUTO_CONTEXT_HANDLER_ABSENT_PROPERTIES = "problem.uicontexthandler.propabsent";
		public static final String ELEMENT_NEGATIVE_INEDX = "problem.uielement.negativeindex";
		public static final String ELEMENT_ZERO_ORDINAL = "problem.uielement.zerorodinal";
		public static final String ELEMENT_EMPTY_QUEUE = "problem.uielement.emptyqueue";
		public static final String ELEMENT_UNSUPPORTED_SELECT_ACTION = "problem.uielement.selectaction.unsupported";
		
		/* Sikuli */
		public static final String COMPARISON_IMAGE_NOT_FOUND = "problem.sikuli.comparison.imagenotfound";
		public static final String COMPARISON_NOT_POSSIBLE = "problem.sikuli.comparison.imagesnotcomparable";
		
	}
	public static ComponentConfigurator getComponentConfigurator() {
		return new UiAutomatorConfigurator();
	}

}
