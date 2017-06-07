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
package pvt.arjunasdk.uiauto.api.actions;

public interface BasicActionHandler {
	boolean isPresent() throws Exception;
     boolean isAbsent()  throws Exception;
     boolean isVisible()  throws Exception;
     boolean isInvisible()  throws Exception;
     void waitForPresence() throws Exception;
     void waitForAbsence()  throws Exception;
     void waitForVisibility()  throws Exception;
     void waitForInvisibility()  throws Exception;

	void enterText(String text) throws Exception;
	void setText(String text) throws Exception;
	void clearText() throws Exception;

	void focus() throws Exception;
	void click() throws Exception;
}
