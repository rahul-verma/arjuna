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
package com.autocognite.arjuna.uiauto.interfaces;

import com.autocognite.pvt.uiautomator.api.ACElement;
import com.autocognite.pvt.uiautomator.api.actions.AttributesInquirer;
import com.autocognite.pvt.uiautomator.api.actions.BasicActionHandler;
import com.autocognite.pvt.uiautomator.api.actions.ChainActionHandler;
import com.autocognite.pvt.uiautomator.api.actions.CheckBoxActionHandler;
import com.autocognite.pvt.uiautomator.api.actions.ElementIdentifier;
import com.autocognite.pvt.uiautomator.api.actions.ElementNestedActionHandler;
import com.autocognite.pvt.uiautomator.api.actions.ImageBasedActionHandler;
import com.autocognite.pvt.uiautomator.api.actions.InstanceGetter;
import com.autocognite.pvt.uiautomator.api.actions.SelectAndRadioActionHandler;
import com.autocognite.pvt.uiautomator.api.actions.WebActionHandler;

public interface UiElement extends 		ACElement,
											ImageBasedActionHandler,
											BasicActionHandler,
											AttributesInquirer,
											ChainActionHandler,
											CheckBoxActionHandler,
											SelectAndRadioActionHandler,
											WebActionHandler,
											ElementIdentifier,
											InstanceGetter,
											ElementNestedActionHandler{

	Object throwUnsupportedActionException(String action) throws Exception;

	Object throwZeroOrdinalException(String action) throws Exception;

	Object throwNegativeIndexException(String action) throws Exception;

	Object throwEmptyElementQueueException(String action) throws Exception;

	Object throwUnsupportedSelectActionException(String action)
			throws Exception;

}
