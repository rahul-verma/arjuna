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
package pvt.batteries.cli;

import java.util.HashMap;

import com.arjunapro.testauto.interfaces.Value;

import pvt.batteries.lib.ComponentIntegrator;

public interface CLIConfigurator extends CLIOptions {

	void processUserOptions() throws Exception;

	HashMap<String, Value> getUserOptions();

	void addValue(String propPath, Value value) throws Exception;

	void setIntegrator(ComponentIntegrator integrator);

	void setArgs(String[] cliArgs) throws Exception;
}
