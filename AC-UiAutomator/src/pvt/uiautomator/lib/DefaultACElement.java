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
package pvt.uiautomator.lib;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import com.arjunapro.testauto.config.RunConfig;
import com.arjunapro.uiauto.enums.ElementLoaderType;
import com.arjunapro.uiauto.enums.UiElementType;

import pvt.batteries.config.Batteries;
import pvt.batteries.exceptions.Problem;
import pvt.uiautomator.UiAutomator;
import pvt.uiautomator.api.ACElement;
import pvt.uiautomator.api.ElementMetaData;
import pvt.uiautomator.api.UiMediator;

public abstract class DefaultACElement implements  ACElement{
	private UiElementType elementType = UiElementType.GENERIC;
	private UiMediator mediator = null;
	private ElementMetaData metaData = null;
	private String name = null;
	private String entityName = null;
	private Object element = null;
	private Object elements = null;
	private boolean compositeFlag = false;
	private String imagePath = null;
	private ElementLoaderType loaderType = null;
	private String uiLabel = null;

	public DefaultACElement(ElementMetaData metaData) {
		this.metaData = metaData;
	}

	@Override
	public void setLoaderType(ElementLoaderType type) {
		this.loaderType = type;
	}

	@Override
	public ElementLoaderType getLoaderType() {
		return this.loaderType;
	}

	@Override
	public String getPageLabel() {
		return this.uiLabel;
	}

	@Override
	public void setPageLabel(String label) {
		this.uiLabel = label;
	}

	@Override
	public UiMediator getMediator() {
		return this.mediator;
	}

	public void setMediator(UiMediator mediator){
		this.mediator = mediator;
	}
//	public UiMediator getUiMediator(){
//		return mediator;
//	}

	public String getName(){
		return this.name;
	}

	public void setName(String name){
		this.name = name;
	}

	public String getCompositePageName(){
		return this.entityName;
	}

	public void setCompositePageName(String name){
		this.entityName = name;
	}

	public void setElement (Object element){
		this.element = element;
	}

	public Object getElement(){
		return this.element;
	}

	public void setElements (Object elements){
		this.elements = elements;
	}

	public Object getElements (){
		return this.elements;
	}

	public void setType(UiElementType type) {
		elementType = type;
	}

	public UiElementType getType() {
		return elementType;
	}

	@Override
	public void switchOnCompositeFlag() {
		this.compositeFlag = true;
	}

	@Override
	public void switchOffCompositeFlag() {
		this.compositeFlag = false;
	}

	public boolean isComposite() {
		return this.compositeFlag;
	}

	public void reset() throws Exception {
		this.element = null;
		this.elements = null;
	}

	public String property(String propName) {
		return metaData.get(propName);
	}

	public String getProperty(String propName) {
		return metaData.get(propName);
	}

	public ElementMetaData getMetaData() {
		return this.metaData;
	}

	public void setProperty(String propName, String value) {
		metaData.set(propName, value);
	}

	public void setMetaData(ElementMetaData map) {
		this.metaData = map;
	}

	private String takeScreenshotIfPossible() throws IOException{
		try{
			File path = this.getMediator().takeScreenshot();
			if (path != null){
				return path.getCanonicalPath();
			} else {
				return "NA";
			}
		} catch (Exception e){
			return "Not able to take snapshot";
		}
	}

	protected String getClassForLoaderType() throws Exception{
		String rValue = "";
		if(this.getLoaderType() == null){
			return "Element API";
		}
		switch(this.getLoaderType()){
		case AUTOMATOR: rValue = "Element API"; break;
		case PAGE: rValue = this.getPageLabel(); break;
		case COMPOSITE_PAGE: rValue = this.getCompositePageName() + "." + this.getPageLabel(); break;
		}
		return rValue;
	}

	protected String getElementNameFillerForException() throws Exception{
		String rValue = "";
		if(this.getLoaderType() == null){
			return "";
		}
		switch(this.getLoaderType()){
		case AUTOMATOR: rValue = ""; break;
		case PAGE:  rValue = String.format("name %s and ", this.getName()); break;
		case COMPOSITE_PAGE: rValue = String.format("name %s and ", this.getName()); break;
		}
		return rValue;
	}

	protected String getElementNameFillerForException(ACElement element) throws Exception{
		String rValue = "";
		if(element.getLoaderType() == null){
			return "";
		}
		switch(element.getLoaderType()){
		case AUTOMATOR: rValue =  ""; break;
		case PAGE: rValue = String.format("name %s and ", element.getName()); break;
		case COMPOSITE_PAGE: rValue = String.format("name %s and ", element.getName()); break;
		}
		return rValue;
	}

	protected Object throwElementException(
			Throwable e,
			String code,
			String action,
			String message
			) throws Exception{
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
				getClassForLoaderType(),
				action,
				code,
				message,
				takeScreenshotIfPossible(),
				e
				);
	}

	private Object throwBasicElementMessageException(Throwable e, String code, String action, String filler) throws Exception{
		return throwElementException(
				e, 
				code,
				action,
				Batteries.getProblemText(
						code,
						this.getMediator().getAutomatorName(),
						filler,
						getElementNameFillerForException(),
						this.getMetaData().getAllProperties().toString()
						)
				);		
	}

	protected Object throwUnsupportedException(String action) throws Exception{
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
				getClassForLoaderType(),
				action,
				UiAutomator.problem.ELEMENT_UNSUPPORTED_ACTION,
				Batteries.getProblemText(
						UiAutomator.problem.ELEMENT_UNSUPPORTED_ACTION,
						action,
						getElementNameFillerForException(),
						this.getMetaData().getAllProperties().toString()
						),
				takeScreenshotIfPossible()
				);	
	}
	
	protected Object throwExceptionFromMediator(String code, String action) throws Exception{
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
				getClassForLoaderType(),
				action,
				code,
				Batteries.getProblemText(
						code,
						getElementNameFillerForException(),
						this.getMetaData().getAllProperties().toString()
						),
				takeScreenshotIfPossible()
				);	
	}
	
	protected Object throwUnsupportedActionExceptionFromMediator(String code, String action) throws Exception{
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
				getClassForLoaderType(),
				action,
				code,
				Batteries.getProblemText(
						code,
						action,
						getElementNameFillerForException(),
						this.getMetaData().getAllProperties().toString()
						),
				takeScreenshotIfPossible()
				);	
	}
	
	private Object throwElementActionException(Throwable e, String action, String filler) throws Exception{
		return throwBasicElementMessageException(e, UiAutomator.problem.ELEMENT_ACTION_FAILURE, action, filler);		
	}

	private Object throwElementInquiryException(Exception e, String action, String filler) throws Exception{
		return throwBasicElementMessageException(e, UiAutomator.problem.ELEMENT_INQUIRY_FAILURE, action, filler);		
	}

	private Object throwElementGetAttributeException(Exception e, String action, String filler) throws Exception{
		return throwBasicElementMessageException(e, UiAutomator.problem.ELEMENT_GET_ATTR_FAILURE, action, filler);		
	}

	protected Object throwElementGetInstanceException(Exception e, String action, String filler) throws Exception{
		return throwBasicElementMessageException(e, UiAutomator.problem.ELEMENT_GET_INSTANCE_FAILURE, action, filler);		
	}

	protected Object throwElementIdentificationException(Exception e, String action, String filler) throws Exception{
		return throwBasicElementMessageException(e, UiAutomator.problem.ELEMENT_IDENTIFICATION_FAILURE, action, filler);		
	}

	/* (non-Javadoc)
	 * @see in.unitee.lib.ui.element.IWebUiElement#enterText(java.lang.String)
	 */

	@Override
	public void enterText(String text) throws Exception{
		try {
			getMediator().enterText(text);} catch (Exception e){
			throwElementActionException(e, "enterText", "enter text in");
		}
	}

	/* (non-Javadoc)
	 * @see in.unitee.lib.ui.element.IWebUiElement#isElementPresent(in.unitee.lib.ui.element.IWebUiElement)
	 */
	@Override
	public boolean isPresent() throws Exception{
		try {
			return getMediator().isPresent();} catch (Exception e){
			return (boolean) throwElementInquiryException(e, "isPresent", "presence of");
		}
	}
	
	@Override
	public boolean isAbsent() throws Exception {
		try {
			return getMediator().isAbsent();} catch (Exception e){
			return (boolean) throwElementInquiryException(e, "isAbsent", "absence of");
		}
	}
	
	@Override
	public boolean isVisible() throws Exception {
		try {
			return getMediator().isVisible();} catch (Exception e){
			return (boolean) throwElementInquiryException(e, "isVisible", "visibility of");
		}
	}

	@Override
	public boolean isInvisible() throws Exception {
		try {
			return getMediator().isInvisible();} catch (Exception e){
			return (boolean) throwElementInquiryException(e, "isInvisible", "invisibility of");
		}
	}

	/* (non-Javadoc)
	 * @see in.unitee.lib.ui.element.IWebUiElement#click()
	 */
	@Override
	public void click() throws Exception {
		try {
			getMediator().click();} catch (Exception e){
			throwElementActionException(e, "click", "click");
		}
	}

	@Override
	public void focus() throws Exception {
		try {
			getMediator().focus();} catch (Exception e){
			throwElementActionException(e, "focus", "focus on");
		}
	}

	@Override
	public void waitForPresence() throws Exception {
		try {
			getMediator().waitForPresence();} catch (Exception e){
			throwElementException(
					e,
					UiAutomator.problem.ELEMENT_WAIT_FAILURE,
					"waitForPresence",
					Batteries.getProblemText(
							UiAutomator.problem.ELEMENT_WAIT_FAILURE,
							this.getMediator().getAutomatorName(),
							this.getMediator().getWaitTime(),
							"presence of",
							getElementNameFillerForException(),
							this.getMetaData().getAllProperties().toString()
							)
					);
		}
	}
	

	@Override
	public void waitForAbsence() throws Exception {
		try {
			getMediator().waitForAbsence();} catch (Exception e){
			throwElementException(
					e,
					UiAutomator.problem.ELEMENT_WAIT_FAILURE,
					"waitForAbsence",
					Batteries.getProblemText(
							UiAutomator.problem.ELEMENT_WAIT_FAILURE,
							this.getMediator().getAutomatorName(),
							this.getMediator().getWaitTime(),
							"absence of",
							getElementNameFillerForException(),
							this.getMetaData().getAllProperties().toString()
							)
					);
		}
	}

	@Override
	public void waitForVisibility() throws Exception {
		try {
			getMediator().waitForVisibility();} catch (Exception e){
			throwElementException(
					e,
					UiAutomator.problem.ELEMENT_WAIT_FAILURE,
					"waitForVisibility",
					Batteries.getProblemText(
							UiAutomator.problem.ELEMENT_WAIT_FAILURE,
							this.getMediator().getAutomatorName(),
							this.getMediator().getWaitTime(),
							"visibility of",
							getElementNameFillerForException(),
							this.getMetaData().getAllProperties().toString()
							)
					);
		}
	}

	@Override
	public void waitForInvisibility() throws Exception {
		try {
			getMediator().waitForInvisibility();} catch (Exception e){
			throwElementException(
					e,
					UiAutomator.problem.ELEMENT_WAIT_FAILURE,
					"waitForInvisibility",
					Batteries.getProblemText(
							UiAutomator.problem.ELEMENT_WAIT_FAILURE,
							this.getMediator().getAutomatorName(),
							this.getMediator().getWaitTime(),
							"invisibility of",
							getElementNameFillerForException(),
							this.getMetaData().getAllProperties().toString()
							)
					);
		}
	}

	@Override
	public void setText(String text) throws Exception {
		try {
			getMediator().setText(text);} catch (Exception e){
			throwElementActionException(e, "setText", "set text of");
		}
	}

	public void clearText() throws Exception {
		try {
			getMediator().clearText();} catch (Exception e){
			throwElementActionException(e, "clearText", "clear text of");
		}
	}

	public void check() throws Exception {
		try {
			getMediator().check();} catch (Exception e){
			throwElementActionException(e, "check", "check checkbox");
		}
	}

	public void uncheck() throws Exception {
		try {
			getMediator().uncheck();} catch (Exception e){
			throwElementActionException(e, "uncheck", "uncheck checkbox");
		}
	}

	public void toggle() throws Exception {
		try {
			getMediator().toggle();} catch (Exception e){
			throwElementActionException(e, "toggle", "toggle checkbox");
		}
	}

	/*
	 * Selection API
	 */

	public void selectLabel(String text) throws Exception {
		try {
			getMediator().selectLabel(text);} catch (Exception e){
			throwElementActionException(
					e, "selectLabel",
					String.format("select label %s from %s", text, this.getType().toString().toLowerCase())
					);
		}
	}	

	public void select(String text) throws Exception {
		try {
			getMediator().select(text);} catch (Exception e){
			throwElementActionException(
					e, "select",
					String.format("select label %s from %s", text, this.getType().toString().toLowerCase())
					);
		}
	}

	public void selectValue(String value) throws Exception {
		try {
			getMediator().selectValue(value);} catch (Exception e){
			throwElementActionException(
					e, "selectValue",
					String.format("select value %s from %s", value, this.getType().toString().toLowerCase())
					);
		}
	}

	public void selectIndex(int index) throws Exception {
		try {
			getMediator().selectIndex(index);} catch (Exception e){
			throwElementActionException(
					e, "selectIndex",
					String.format("select option at index %d from %s", index, this.getType().toString().toLowerCase())
					);
		}
	}

	public boolean hasSelectedLabel(String text) throws Exception {
		try {
			return getMediator().hasSelectedLabel(text);} catch (Exception e){
			return (boolean) throwElementInquiryException(
					e, "hasSelectedLabel",
					String.format("whether label %s is selected for %s", text, this.getType().toString().toLowerCase())
					);
		}
	}

	public boolean hasSelectedValue(String value) throws Exception {
		try {
			return getMediator().hasSelectedValue(value);} catch (Exception e){
			return (boolean) throwElementInquiryException(
					e, "hasSelectedValue",
					String.format("whether value %s is selected for %s", value, this.getType().toString().toLowerCase())
					);
		}
	}

	public boolean hasSelectedIndex(int index) throws Exception {
		try {
			return getMediator().hasSelectedIndex(index);} catch (Exception e){
			return (boolean) throwElementInquiryException(
					e, "hasSelectedIndex",
					String.format("whether option at index %d is selected for %s", index, this.getType().toString().toLowerCase())
					);
		}
	}

	@SuppressWarnings("unchecked")
	public ArrayList<String> getAllLabels() throws Exception {
		try {
			return getMediator().getAllLabels();} catch (Exception e){
			return (ArrayList<String>) throwElementGetAttributeException(
					e, "getAllLabels",
					String.format("all labels for %s", this.getType().toString().toLowerCase())
					);
		}
	}

	@SuppressWarnings("unchecked")
	public ArrayList<String> getAllValues() throws Exception {
		try {
			return getMediator().getAllValues();} catch (Exception e){
			return (ArrayList<String>) throwElementGetAttributeException(
					e, "getAllValues",
					String.format("all values for %s", this.getType().toString().toLowerCase())
					);
		}
	}


	public int getOptionCount() throws Exception {
		try {
			return getMediator().getOptionCount();} catch (Exception e){
			return (int) throwElementGetAttributeException(
					e, "getOptionCount",
					String.format("option count for %s", this.getType().toString().toLowerCase())
					);
		}
	}

	// Properties


	public String getText() throws Exception {
		try {
			return getMediator().getText();} catch (Exception e){
			return (String) throwElementGetAttributeException(e, "getText","text of");
		}
	}


	public String getValue() throws Exception {
		try {
			return getMediator().getValue();} catch (Exception e){
			return (String) throwElementGetAttributeException(e, "getValue","value of");
		}
	}


	public String getAttribute(String attr) throws Exception {
		try {
			return getMediator().getAttribute(attr);} catch (Exception e){
			return (String) throwElementGetAttributeException(e, "getAttribute",String.format("value of %s attribute of", attr));
		}
	}

	// Frame related action

	public void switchToFrame() throws Exception {
		this.getMediator().switchToFrame();
	}

	public void hover() throws Exception {
		try{
			this.getMediator().hover();} catch (Exception e){
			throwElementActionException(e, "hover", "hover on");
		}
	}


	public void hoverAndClick() throws Exception {
		try{
			this.getMediator().hoverAndClick();} catch (Exception e){
			throwElementActionException(e, "hoverAndClick", "hover and click on");
		}
	}


	public void rightClick() throws Exception {
		try{
			this.getMediator().rightClick();} catch (Throwable e){
			throwElementActionException(e, "rightClick", "right click on");
		}
	}


	public String getImagePath() throws Exception {
		return this.imagePath;
	}


	public void setImagePath(String imagePath) throws Exception {
		this.imagePath = imagePath;
	}
	
}
