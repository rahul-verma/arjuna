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
package arjunasdk.exceptions;

import arjunasdk.interfaces.Value;

public class UnsupportedRepresentationException extends Exception {

	/**
	 * 
	 */
	private static final long serialVersionUID = 669734988933529307L;

	// Parameterless Constructor
	public <T extends Value> UnsupportedRepresentationException(String klassUserFriendlyName, String method, String strSourceValue, String targetValueType) {
		super(String.format("Value.%s(): Can not represent %s value containing >>%s<< as %s.", method, strSourceValue, klassUserFriendlyName, targetValueType));
	}

}
