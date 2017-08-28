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
import java.util.Map;

import arjunasdk.interfaces.Value;

public abstract class AbstractCliConfigurator implements CLIConfigurator {
	private CLI cli = null;
	private Map<String, String> rawMap = new HashMap<String, String>();
	private Map<String, Value> userOptionMap = new HashMap<String, Value>();

	public AbstractCliConfigurator(CLI cli) throws Exception {
		this.cli = cli;
	}

	private CLI getCli() {
		return cli;
	}

	@Override
	public Map<String, Value> getUserOptions() {
		return this.userOptionMap;
	}

	private void processProperties() throws Exception {
		// java.util.Properties map = getCli().getProperties();
		// for (Object prop: map.keySet()){
		// String propName = (String) prop;
		// rawMap.put(propName, map.getProperty(propName).trim());
		// }
	}

	@Override
	public String getOption(String option) {
		return this.getCli().getOption(option);
	}

	@Override
	public boolean hasOption(String option) {
		return this.getCli().hasOption(option);
	}

	@Override
	public void help() throws Exception {
		this.getCli().help();
	}

	@Override
	public void addValue(String propPath, Value value) throws Exception {
		this.userOptionMap.put(propPath, value);
	}

	protected String getRawUserValue(String optionName) {
		if (getCli().getOption(optionName) != null) {
			return getCli().getOption(optionName).trim();
		} else {
			return null;
		}
	}
	
	protected Value getUserOption(String optionName){
		if (this.userOptionMap.containsKey(optionName)){
			return this.userOptionMap.get(optionName);
		} else {
			return null;
		}
	}

	@Override
	public void processUserOptions() throws Exception {
		this.processProperties();
	}
	
	@Override
	public void setArgs(String[] cliArgs) throws Exception {
		this.cli.setArgs(cliArgs);
	}
}
