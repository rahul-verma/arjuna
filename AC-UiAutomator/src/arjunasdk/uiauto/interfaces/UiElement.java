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
package arjunasdk.uiauto.interfaces;

import pvt.arjunasdk.uiauto.api.ACElement;
import pvt.arjunasdk.uiauto.api.actions.AttributesInquirer;
import pvt.arjunasdk.uiauto.api.actions.BasicActionHandler;
import pvt.arjunasdk.uiauto.api.actions.ChainActionHandler;
import pvt.arjunasdk.uiauto.api.actions.CheckBoxActionHandler;
import pvt.arjunasdk.uiauto.api.actions.ElementIdentifier;
import pvt.arjunasdk.uiauto.api.actions.ElementNestedActionHandler;
import pvt.arjunasdk.uiauto.api.actions.ImageBasedActionHandler;
import pvt.arjunasdk.uiauto.api.actions.InstanceGetter;
import pvt.arjunasdk.uiauto.api.actions.SelectAndRadioActionHandler;
import pvt.arjunasdk.uiauto.api.actions.WebActionHandler;

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
