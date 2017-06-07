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
package pvt.arjunasdk.uiauto.api;

import java.io.File;

import arjunasdk.uiauto.interfaces.UiElement;
import pvt.arjunasdk.uiauto.api.actions.AttributesInquirer;
import pvt.arjunasdk.uiauto.api.actions.BasicActionHandler;
import pvt.arjunasdk.uiauto.api.actions.ChainActionHandler;
import pvt.arjunasdk.uiauto.api.actions.CheckBoxActionHandler;
import pvt.arjunasdk.uiauto.api.actions.ElementNestedActionHandler;
import pvt.arjunasdk.uiauto.api.actions.ImageBasedActionHandler;
import pvt.arjunasdk.uiauto.api.actions.InstanceGetter;
import pvt.arjunasdk.uiauto.api.actions.SelectAndRadioActionHandler;
import pvt.arjunasdk.uiauto.api.actions.WebActionHandler;
import pvt.arjunasdk.uiauto.enums.UiElementType;

public interface UiMediator extends 	AttributesInquirer,
									BasicActionHandler,
									ChainActionHandler,
									CheckBoxActionHandler,
									ImageBasedActionHandler,
									SelectAndRadioActionHandler,
									WebActionHandler,
									InstanceGetter,
									ElementNestedActionHandler{
	String getAutomatorName();
	void setAutomatorName(String name);
	
	Object getToolFindersQueueObject();
	void identify() throws Exception;
	void identifyAll() throws Exception;
	
	int getWaitTime() throws Exception;
	File takeScreenshot() throws Exception;
	
	void setRawToolElement(Object toolElementObject) throws Exception;
	void setRawToolElements(Object toolElementsObject);
	int getRandomElementIndex() throws Exception;
	int getLastIndex() throws Exception;
	
	boolean isCompositeElementIdentified() throws Exception;
	boolean isSingularElementIdentified() throws Exception;
	int getElementCountForCompositeElement() throws Exception;
	void assignElementAtIndexFromMatches(int index) throws Exception;
	UiElement getInstanceAtIndex(int index) throws Exception;
	UiElementType getElementType();
}
