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
package com.autocognite.pvt.uiautomator.lib.base;

import java.io.File;
import java.util.ArrayList;
import java.util.Random;

import com.autocognite.arjuna.uiauto.enums.UiElementType;
import com.autocognite.arjuna.uiauto.interfaces.UiElement;
import com.autocognite.pvt.uiautomator.api.ElementMetaData;
import com.autocognite.pvt.uiautomator.api.UiMediator;

public abstract class BaseUiMediator extends BaseUiScreenMediator implements UiMediator{
	
	private String automatorName = null;
	private UiElement uiElement = null;
	private ElementMetaData elementMetaData = null;
	private UiElementType elementType = null;
	private boolean bComposite = false;

	public BaseUiMediator() {
		super();
	}

	public BaseUiMediator(UiElement uiElement) {
		this.uiElement = uiElement;
		this.elementMetaData = uiElement.getMetaData();
	}
	
	public ElementMetaData getElementMetaData() {
		return elementMetaData;
	}

	public UiElement getUiElement() {
		return this.uiElement;
	}

	public void setUiElement(UiElement element) {
		this.uiElement = element;
	}

	@Override
	public String getAutomatorName() {
		return this.automatorName;
	}

	@Override
	public void setAutomatorName(String name) {
		this.automatorName = name;
	}

	@Override
	public UiElementType getElementType() {
		return this.elementType;
	}

	public void setElementType(UiElementType elementType) {
		this.elementType = elementType;
	}

	public boolean isComposite() {
		return bComposite;
	}

	public void setComposite(boolean isComposite) {
		this.bComposite = isComposite;
	}

	public void verifyIndex(int index) throws Exception {
		if (index < 0){
			this.getUiElement().throwNegativeIndexException("verifyIndex");
		}
	}

	public void verifyOrdinal(int ordinal) throws Exception {
		if (ordinal < 1){
			this.getUiElement().throwZeroOrdinalException("verifyOrdinal");
		}
	}

	public void prepareIndexIndetification(int index) throws Exception {
		verifyIndex(index);
		identifyAll();		
	}

	public void identifyIfNull() throws Exception {
		if (!isSingularElementIdentified()){
			identify();
		}		
	}

	public void identifyAllIfNull() throws Exception {
		if (!isCompositeElementIdentified()){
			identifyAll();
		}		
	}

	@Override
	public int getRandomElementIndex() throws Exception {
		identifyAllIfNull();
		Random rn = new Random();
		int retValue = -1;
		if (isCompositeElementIdentified() && (getElementCountForCompositeElement() > 1)){
			retValue = rn.nextInt(getElementCountForCompositeElement());
		} else {
			return (int) this.getUiElement().throwEmptyElementQueueException("getRandomElementIndex");
		}
		return retValue;
	}

	@Override
	public int getLastIndex() throws Exception {
		identifyAllIfNull();
		int retValue = -1;
		if (isCompositeElementIdentified() && (getElementCountForCompositeElement() > 1)){
			retValue = getElementCountForCompositeElement() - 1;
		} else {
			return (int) this.getUiElement().throwEmptyElementQueueException("getLastIndex");
		}
		return retValue;
	}

	public UiElement get(int index) throws Exception {
		this.verifyIndex(index);
		return getInstanceAtIndex(index);
	}

	public UiElement get() throws Exception {
		if (!this.getUiElement().isComposite()){
			identifyAllIfNull();
			return this.getUiElement();
		} else {
			return getInstanceAtIndex(0);
		}
	}

	public UiElement getInstanceAtOrdinal(int ordinal) throws Exception {
		this.verifyOrdinal(ordinal);
		return getInstanceAtIndex(ordinal - 1);
	}

	public UiElement getRandomInstance() throws Exception {
		return getInstanceAtIndex(getRandomElementIndex());
	}

	public UiElement getFirstInstance() throws Exception {
		return getInstanceAtIndex(0);
	}

	public UiElement getLastInstance() throws Exception {
		return getInstanceAtIndex(getLastIndex());
	}

	@Override
	public String getText() throws Exception {
		return (String) this.getUiElement().throwUnsupportedActionException("getText");
	}

	@Override
	public String getValue() throws Exception {
		return (String) this.getUiElement().throwUnsupportedActionException("getValue");
	}

	@Override
	public String getAttribute(String attr) throws Exception {
		return (String) this.getUiElement().throwUnsupportedActionException("getAttribute");
	}

	@Override
	public boolean isPresent() throws Exception {
		return (boolean) this.getUiElement().throwUnsupportedActionException("isPresent");
	}

	@Override
	public void waitForPresence() throws Exception {
		this.getUiElement().throwUnsupportedActionException("waitForPresence");
	}

	@Override
	public void enterText(String text) throws Exception {
		this.getUiElement().throwUnsupportedActionException("enterText");
	}

	@Override
	public void setText(String text) throws Exception {
		this.getUiElement().throwUnsupportedActionException("setText");
	}

	@Override
	public void clearText() throws Exception {
		this.getUiElement().throwUnsupportedActionException("clearText");
	}

	@Override
	public void focus() throws Exception {
		this.getUiElement().throwUnsupportedActionException("focus");
	}

	@Override
	public void click() throws Exception {
		this.getUiElement().throwUnsupportedActionException("click");
	}

	@Override
	public void hover() throws Exception {
		this.getUiElement().throwUnsupportedActionException("hover");
	}

	@Override
	public void hoverAndClick() throws Exception {
		this.getUiElement().throwUnsupportedActionException("hoverAndClick");
	}

	@Override
	public void rightClick() throws Exception {
		this.getUiElement().throwUnsupportedActionException("rightClick");
	}

	@Override
	public void check() throws Exception {
		this.getUiElement().throwUnsupportedActionException("check");
	}

	@Override
	public void uncheck() throws Exception {
		this.getUiElement().throwUnsupportedActionException("uncheck");
	}

	@Override
	public void toggle() throws Exception {
		this.getUiElement().throwUnsupportedActionException("toggle");
	}

	@Override
	public String getImagePath() throws Exception {
		return (String) this.getUiElement().throwUnsupportedActionException("getImagePath");
	}

	@Override
	public void setImagePath(String imagePath) throws Exception {
		this.getUiElement().throwUnsupportedActionException("setImagePath");
	}

	@Override
	public void switchToFrame() throws Exception {
		this.getUiElement().throwUnsupportedActionException("switchToFrame");
	}

	@Override
	public int getWaitTime() throws Exception {
		return (int) this.getUiElement().throwUnsupportedActionException("getWaitTime");
	}

	@Override
	public File takeScreenshot() throws Exception {
		return (File) this.getUiElement().throwUnsupportedActionException("takeScreenshot");
	}

	@Override
	public void identify() throws Exception {
		this.getUiElement().throwUnsupportedActionException("identify");
	}

	@Override
	public void identifyAll() throws Exception {
		this.getUiElement().throwUnsupportedActionException("identifyAll");
	}

	public void hoverAndClickElement(UiElement uiElement) throws Exception {
		this.getUiElement().throwUnsupportedActionException("hoverAndClickElement");
	}

	public void rightClickAndClickElement(UiElement uiElement) throws Exception {
		this.getUiElement().throwUnsupportedActionException("rightClickAndClickElement");
	}

	public UiElement getInstanceByText(String text) throws Exception {
		return (UiElement) this.getUiElement().throwUnsupportedActionException("getInstanceByText");
	}

	public UiElement getInstanceByTextContent(String text) throws Exception {
		return (UiElement) this.getUiElement().throwUnsupportedActionException("getInstanceByTextContent");
	}
	
	protected abstract void selectDropDownLabel(String label) throws Exception;
	protected abstract void selectRadioLabel(String label) throws Exception;
	protected abstract void selectDropDownValue(String value) throws Exception;
	protected abstract void selectRadioValue(String value) throws Exception;
	protected abstract void selectDropDownOptionAtIndex(int index) throws Exception;
	protected abstract void selectRadioOptionAtIndex(int index) throws Exception;
	protected abstract boolean isDropDownLabelSelected(String label) throws Exception;
	protected abstract boolean isRadioLabelSelected(String label) throws Exception;
	protected abstract boolean isDropDownValueSelected(String label) throws Exception;
	protected abstract boolean isRadioValueSelected(String label) throws Exception;
	protected abstract boolean isDropDownOptionSelectedAtIndex(int index) throws Exception;
	protected abstract boolean isRadioOptionSelectedAtIndex(int index) throws Exception;
	protected abstract ArrayList<String> getDropDownLabels() throws Exception;
	protected abstract ArrayList<String> getRadioLabels() throws Exception;
	protected abstract ArrayList<String> getDropDownValues() throws Exception;
	protected abstract ArrayList<String> getRadioValues() throws Exception;
	protected abstract int getDropDownOptionCount() throws Exception;
	protected abstract int getRadioOptionCount() throws Exception;
		
	public void selectLabel(String label) throws Exception {
		identifyIfNull();
		switch (this.getElementType()){
		case DROPDOWN:
			selectDropDownLabel(label);
			break;
		case RADIO:
			selectRadioLabel(label);
			break;
		default: this.getUiElement().throwUnsupportedSelectActionException("selectLabel");
		}
	}
	
	public void select(String text) throws Exception{
		selectLabel(text);
	}
	
	public void selectValue(String value) throws Exception {
		identifyIfNull();
		switch (this.getElementType()){
		case DROPDOWN:
			selectDropDownValue(value);
			break;
		case RADIO:
			selectRadioValue(value);
			break;
		default: this.getUiElement().throwUnsupportedSelectActionException("selectValue");
		}
	}
	
	public void selectIndex(int index) throws Exception {
		identifyIfNull();
		switch (this.getElementType()){
		case DROPDOWN:
			selectDropDownOptionAtIndex(index);
			break;
		case RADIO:
			selectRadioOptionAtIndex(index);
			break;
		default: this.getUiElement().throwUnsupportedSelectActionException("selectIndex");
		}
	}
	
	public boolean hasSelectedLabel(String label) throws Exception {
		identifyIfNull();
		switch (this.getElementType()){
		case DROPDOWN:
			return isDropDownLabelSelected(label);
		case RADIO:
			return isRadioLabelSelected(label);
		default: return (boolean) this.getUiElement().throwUnsupportedSelectActionException("hasSelectedLabel");
		}
	}
	
	public boolean hasSelectedValue(String value) throws Exception {
		identifyIfNull();
		switch (this.getElementType()){
		case DROPDOWN:
			return isDropDownValueSelected(value);
		case RADIO:
			return isRadioValueSelected(value);
		default: return (boolean) this.getUiElement().throwUnsupportedSelectActionException("hasSelectedValue");
		}
	}
	
	@Override
	public boolean hasSelectedIndex(int index) throws Exception {
		identifyIfNull();
		switch (this.getElementType()){
		case DROPDOWN:
			return isDropDownOptionSelectedAtIndex(index);
		case RADIO:
			return isRadioOptionSelectedAtIndex(index);
		default: return (boolean) this.getUiElement().throwUnsupportedSelectActionException("hasSelectedIndex");
		}
	}
	
	@Override
	public ArrayList<String> getAllLabels() throws Exception {
		identifyIfNull();
		switch (this.getElementType()){
		case DROPDOWN:
			return getDropDownLabels();
		case RADIO:
			return getRadioLabels();
		default: return (ArrayList<String>) this.getUiElement().throwUnsupportedSelectActionException("getAllLabels");
		}
	}
	
	@Override
	public ArrayList<String> getAllValues() throws Exception {
		identifyIfNull();
		switch (this.getElementType()){
		case DROPDOWN:
			return getDropDownValues();
		case RADIO:
			return getRadioValues();
		default: return (ArrayList<String>) this.getUiElement().throwUnsupportedSelectActionException("getAllValues");
		}
	}
	
	@Override
	public int getOptionCount() throws Exception {
		identifyIfNull();
		switch (this.getElementType()){
		case DROPDOWN:
			return getDropDownOptionCount();
		case RADIO:
			return getRadioOptionCount();
		default: return (int) this.getUiElement().throwUnsupportedSelectActionException("getOptionCount");
		}
	}
}
