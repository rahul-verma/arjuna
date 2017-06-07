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
package arjunasdk.ddauto.exceptions;

public class EmptyListDataRecordLookUpException extends Exception {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1328715061248005907L;
	
	// Constructor that accepts a message
	public EmptyListDataRecordLookUpException(String index) {
		super(String.format("Invalid index [%s] used for list data record lookup. It is empty.", index));
	}
}
