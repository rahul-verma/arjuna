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
package pvt.arjunasdk.uiautomator.lib.base;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

import arjunasdk.uiauto.enums.UiAutomationContext;
import arjunasdk.uiauto.enums.UiElementType;
import arjunasdk.uiauto.interfaces.UiDriver;
import arjunasdk.uiauto.interfaces.UiElement;
import pvt.arjunasdk.uiauto.api.ElementMetaData;
import pvt.arjunasdk.uiauto.enums.ElementLoaderType;
import pvt.arjunasdk.uiauto.enums.UiDriverEngine;
import pvt.arjunasdk.uiautomator.UiAutomator;
import pvt.arjunasdk.uiautomator.lib.DefaultElementMetaData;
import pvt.batteries.config.Batteries;
import pvt.batteries.exceptions.Problem;

public abstract class BaseUiDriver implements UiDriver{
	UiDriverEngine uiAutomatorEngineName = null;
	private UiAutomationContext context = null;
	String appTitle = null;
	private ElementLoaderType loaderType = ElementLoaderType.AUTOMATOR;
	
	public BaseUiDriver(UiAutomationContext context){
		this.setUiTestEngineName(UiDriverEngine.DEFAULT);
		this.setContext(context);
	}
	
	public BaseUiDriver(UiAutomationContext context, ElementLoaderType loaderType){
		this.setUiTestEngineName(UiDriverEngine.DEFAULT);
		this.setContext(context);
		this.setElementLoaderType(loaderType);
	}

	public BaseUiDriver() {
		this.setUiTestEngineName(UiDriverEngine.DEFAULT);
	}
	
	/*
	 * Exceptions
	 */
	
	protected void throwGenericUiAutomatorException(
			String automatorName,
			String action,
			String code,
			String message
			) throws Exception{
				throw new Problem(
						Batteries.getComponentName("UI_AUTOMATOR"),
				automatorName,
				action,
				code,
				message
				);		
	}

	public void throwUnsupportedIndentifierException(String componentName, String methodName, String idString) throws Exception{
		throwGenericUiAutomatorException(
				componentName,
				methodName,
				UiAutomator.problem.UNSUPPORTED_IDENTIFIER,
				Batteries.getProblemText(
						UiAutomator.problem.UNSUPPORTED_IDENTIFIER,
						idString
				)
		);
	}
	
//	public void throwUnsupportedMultipleIndentifiersException(String componentName, String methodName, String mapString) throws Exception{
//		throwGenericUiAutomatorException(
//				componentName,
//				methodName, 
//				UiAutomator.problem.UNSUPPORTED_MULTIPLE_IDENTIFIERS,
//				Unitee.getProblemText(
//						UiAutomator.problem.UNSUPPORTED_MULTIPLE_IDENTIFIERS,
//						mapString
//				)
//		);
//	}
	
	public UiDriverEngine getUiDriverEngineName(){
		return this.uiAutomatorEngineName;
	}
	
	public void setUiTestEngineName(UiDriverEngine name){
		this.uiAutomatorEngineName = name;
	}
	
	public void setAppTitle(String appTitle) {
		this.appTitle = appTitle;
	}

	public String getAppTitle() {
		return this.appTitle;
	}

	public UiAutomationContext getContext() {
		return context;
	}

	public void setContext(UiAutomationContext context) {
		this.context = context;
	}

	public Object throwUnsupportedActionException(String action) throws Exception {
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
				"Default Automator",
				action,
				UiAutomator.problem.AUTOMATOR_UNSUPPORTED_ACTION,
				Batteries.getProblemText(UiAutomator.problem.AUTOMATOR_UNSUPPORTED_ACTION, this.getClass().getSimpleName())
			);		
	}

	@Override
	public UiElement declareElement(ElementMetaData elementMetaData) throws Exception {
	return (UiElement) throwUnsupportedActionException("declareElement");}

	private ElementMetaData createMetaDataObject(String idType, String idValue) throws Exception {
		Map<String, String> map = new HashMap<String, String>();
		map.put(idType, idValue);
		ElementMetaData metaData = new DefaultElementMetaData(map);
		metaData.processStrictly(this.getContext());
		return metaData;
	}

	@Override
	public UiElement elementWithId(String id) throws Exception {
		return this.declareElement(createMetaDataObject("ID", id));
	}

	@Override
	public UiElement elementWithName(String name) throws Exception {
		return this.declareElement(createMetaDataObject("NAME", name));
	}

	@Override
	public UiElement elementWithClass(String klass) throws Exception {
		return this.declareElement(createMetaDataObject("CLASS", klass));
	}

	@Override
	public UiElement elementWithCss(String cssSelector) throws Exception {
		return this.declareElement(createMetaDataObject("CSS", cssSelector));
	}

	@Override
	public UiElement elementWithLinkText(String text) throws Exception {
		return this.declareElement(createMetaDataObject("LINK_TEXT", text));
	}

	@Override
	public UiElement elementWithPartialLinkText(String textContent) throws Exception {
		return this.declareElement(createMetaDataObject("PARTIAL_LINK_TEXT", textContent));
	}

	@Override
	public UiElement elementWithXPath(String xpath) throws Exception {
		return this.declareElement(createMetaDataObject("XPATH", xpath));
	}

	@Override
	public UiElement elementWithXText(String text) throws Exception {
		return this.declareElement(createMetaDataObject("X_TEXT", text));
	}

	@Override
	public UiElement elementWithXPartialText(String textContent) throws Exception {
		return this.declareElement(createMetaDataObject("X_PARTIAL_TEXT", textContent));
	}

	@Override
	public UiElement elementWithXValue(String value) throws Exception {
		return this.declareElement(createMetaDataObject("X_VALUE", value));
	}

	@Override
	public UiElement elementWithXImageSource(String path) throws Exception {
		return this.declareElement(createMetaDataObject("X_IMAGE_SRC", path));
	}

	@Override
	public UiElement elementOfXType(UiElementType type) throws Exception {
		return this.declareElement(createMetaDataObject("X_TYPE", type.toString()));
	}

	@Override
	public UiElement elementBasedOnImage(String imagePath) throws Exception {
		return this.declareElement(createMetaDataObject("IMAGE", imagePath));
	}
	
	@Override
	public Object getUiDriverEngine() throws Exception {
		return throwUnsupportedActionException("getUiTestEngine");
	}

	@Override
	public File takeScreenshot() throws Exception {
		return (File) throwUnsupportedActionException("takeScreenShot");
	}

	@Override
	public void focusOnApp() throws Exception {
		throwUnsupportedActionException("focusOnApp");}

	@Override
	public Object getUnderlyingEngine() throws Exception {
		return throwUnsupportedActionException("getUnderlyingEngine");}

	@Override
	public void confirmAlertIfPresent() throws Exception {
		throwUnsupportedActionException("confirmAlertIfPresent");}

	@Override
	public void close() throws Exception {
		throwUnsupportedActionException("close");}

	@Override
	public String getCurrentWindow() throws Exception {
		return (String) throwUnsupportedActionException("getCurrentWindow");}

	@Override
	public void switchToNewWindow() throws Exception {
		throwUnsupportedActionException("switchToNewWindow");}

	@Override
	public void switchToWindow(String windowHandle) throws Exception {
		throwUnsupportedActionException("switchToWindow");}

	@Override
	public void closeCurrentWindow() throws Exception {
		throwUnsupportedActionException("closeWindow");}

	@Override
	public void goTo(String url) throws Exception {
		throwUnsupportedActionException("goTo");}

	@Override
	public void refresh() throws Exception {
		throwUnsupportedActionException("refresh");}

	@Override
	public void back() throws Exception {
		throwUnsupportedActionException("back");}

	@Override
	public void forward() throws Exception {
		throwUnsupportedActionException("forward");}

	@Override
	public void waitForBody() throws Exception {
		throwUnsupportedActionException("waitForBody");}

	@Override
	public void switchToFrame(int index) throws Exception {
		throwUnsupportedActionException("switchToFrame");}

	@Override
	public void switchToFrame(String name) throws Exception {
		throwUnsupportedActionException("switchToFrame");}

	@Override
	public void switchToDefaultFrame() throws Exception {
		throwUnsupportedActionException("switchToDefaultFrame");}

	@Override
	public boolean areImagesSimilar(File leftImage, File rightImage, Double minScore) throws Exception {
		return (boolean) throwUnsupportedActionException("areImagesSimilar");}

	@Override
	public boolean areImagesSimilar(String leftImagePath, File rightImage) throws Exception {
		return (boolean) throwUnsupportedActionException("areImagesSimilar");}

	@Override
	public boolean areImagesSimilar(String leftImagePath, File rightImage, Double minScore) throws Exception {
		return (boolean) throwUnsupportedActionException("areImagesSimilar");}

	@Override
	public boolean areImagesSimilar(String leftImagePath, String rightImagePath) throws Exception {
		return (boolean) throwUnsupportedActionException("areImagesSimilar");}

	@Override
	public boolean areImagesSimilar(File leftImage, File rightImage) throws Exception {
		return (boolean) throwUnsupportedActionException("areImagesSimilar");}

	@Override
	public void switchToWebContext() throws Exception{
		throwUnsupportedActionException("switchToWebContext");
	}
	
	@Override
	public void switchToNativeContext() throws Exception{
		throwUnsupportedActionException("switchToNativeContext");
	}

	public ElementLoaderType getElementLoaderType() {
		return loaderType;
	}

	public void setElementLoaderType(ElementLoaderType loaderType) {
		this.loaderType = loaderType;
	}
}
