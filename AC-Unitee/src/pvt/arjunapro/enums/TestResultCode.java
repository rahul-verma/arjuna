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

public enum TestResultCode {
	ALL_STEPS_PASS,
	STEP_FAILURE,
	STEP_ERROR,
	UNPICKED_CLASS,
	UNPICKED_METHOD,
	SKIPPED_CLASS_ANNOTATION,
	SKIPPED_METHOD_ANNOTATION,
	SKIPPED_RECORD,
	TEST_CONTAINER_DEPENDENCY_NOTMET,
	TEST_CREATOR_DEPENDENCY_NOTMET,
	TEST_CONTAINER_CONSTRUCTOR_ERROR,
	ERROR_IN_SETUP_CLASS,
	ERROR_IN_SETUP_CLASS_INSTANCE,
	ERROR_IN_SETUP_CLASS_FRAGMENT,
	ERROR_IN_SETUP_METHOD,
	ERROR_IN_SETUP_METHOD_INSTANCE,
	ERROR_IN_SETUP_TEST,
	ERROR_IN_TEARDOWN_CLASS,
	ERROR_IN_TEARDOWN_CLASS_INSTANCE,
	ERROR_IN_TEARDOWN_CLASS_FRAGMENT,
	ERROR_IN_TEARDOWN_METHOD,
	ERROR_IN_TEARDOWN_METHOD_INSTANCE,
	ERROR_IN_TEARDOWN_TEST,
	UNSELECTED,
}
