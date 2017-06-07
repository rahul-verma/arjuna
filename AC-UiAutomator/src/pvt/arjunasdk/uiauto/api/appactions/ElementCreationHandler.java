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
package pvt.arjunasdk.uiauto.api.appactions;

import arjunasdk.uiauto.interfaces.UiElement;
import pvt.arjunasdk.uiauto.enums.UiElementType;

public interface ElementCreationHandler {
	UiElement elementWithId(String id) throws Exception;
	UiElement elementWithName(String name) throws Exception;
	UiElement elementWithClass(String klass) throws Exception;
	UiElement elementWithCss(String cssSelector) throws Exception;
	UiElement elementWithLinkText(String text) throws Exception;
	UiElement elementWithPartialLinkText(String textContent) throws Exception;
	UiElement elementWithXPath(String xpath) throws Exception;
	UiElement elementWithXText(String text) throws Exception;
	UiElement elementWithXPartialText(String textContent) throws Exception;
	UiElement elementWithXValue(String value) throws Exception;
	UiElement elementWithXImageSource(String path) throws Exception;
	UiElement elementOfXType(UiElementType type) throws Exception;
	UiElement elementBasedOnImage(String imagePath) throws Exception;
}
