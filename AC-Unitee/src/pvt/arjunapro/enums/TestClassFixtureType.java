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
package pvt.arjunapro.enums;

public enum TestClassFixtureType {
	SETUP_CLASS,
	SETUP_CLASS_INSTANCE,
	SETUP_CLASS_FRAGMENT,
	SETUP_METHOD,
	SETUP_METHOD_INSTANCE,
	SETUP_TEST,
	TEARDOWN_TEST,
	TEARDOWN_METHOD_INSTANCE,
	TEARDOWN_METHOD,
	TEARDOWN_CLASS_FRAGMENT,
	TEARDOWN_CLASS_INSTANCE,
	TEARDOWN_CLASS
}
