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
package com.autocognite.pvt.unitee.cli;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import com.autocognite.batteries.console.Console;
import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.arjuna.enums.TestPickerProperty;
import com.autocognite.pvt.batteries.cli.AbstractCliConfigurator;
import com.autocognite.pvt.batteries.enums.BatteriesPropertyType;
import com.autocognite.pvt.batteries.lib.ComponentIntegrator;
import com.autocognite.pvt.batteries.value.StringListValue;
import com.autocognite.pvt.batteries.value.ValueFactory;
import com.autocognite.pvt.batteries.value.ValueType;
import com.autocognite.pvt.unitee.config.ArjunaSingleton;

public class UniteeCliConfigurator extends AbstractCliConfigurator {	
	ComponentIntegrator integrator = null;
	private Set<String> nullEquivalentSet = new HashSet<String>(Arrays.asList("na","null","not_set"));
	private Map<TestPickerProperty,String> cliPickerOptions = new HashMap<TestPickerProperty,String>();
	private boolean pickerProvided = false;
	
	public UniteeCliConfigurator() throws Exception {
		super(new UniteeCLI());
	}

	public  void processUserOptions() throws Exception {
		super.processUserOptions();
		if (hasOption("HELP")) {
			help();	
			System.exit(0);
		}
		if (hasOption("VERSION")) {
//			UniteeSingleton.INSTANCE.printUniteeHeader();
			System.exit(0);
		}		

		addFilter(TestPickerProperty.PACKAGE_NAME,"PACKAGE-NAME");
		addFilter(TestPickerProperty.CLASS_NAME,"CLASS-NAME");
		addFilter(TestPickerProperty.PACKAGE_CONSIDER_PATTERNS,"CONSIDER-PACKAGES");
		addFilter(TestPickerProperty.PACKAGE_IGNORE_PATTERNS, "IGNORE-PACKAGES");
		addFilter(TestPickerProperty.CLASS_CONSIDER_PATTERNS, "CONSIDER-CLASSES");
		addFilter(TestPickerProperty.CLASS_IGNORE_PATTERNS,"IGNORE-CLASSES");
		addFilter(TestPickerProperty.METHOD_CONSIDER_PATTERNS, "CONSIDER-METHODS");
		addFilter(TestPickerProperty.METHOD_IGNORE_PATTERNS, "IGNORE-METHODS");
		
		this.addUniteeStringProperty("SESSION-NAME", ArjunaProperty.SESSION_NAME);
		this.addUniteeStringProperty("TEST-DIR", ArjunaProperty.DIRECTORY_TESTS);
		this.addUniteeStringProperty("DISPLAY-LEVEL", BatteriesPropertyType.LOGGING_CONSOLE_LEVEL);
		this.addUniteeStringProperty("LOG-LEVEL", BatteriesPropertyType.LOGGING_FILE_LEVEL);
		this.addUniteeStringProperty("REPORT-GENERATORS-BUILTIN", ArjunaProperty.REPORT_GENERATORS_BUILTIN);
		this.addUniteeStringProperty("REPORT-LISTENERS-BUILTIN", ArjunaProperty.REPORT_LISTENERS_BUILTIN);
		this.addUniteeStringProperty("REPORT-MODE", ArjunaProperty.REPORT_MODE);
		this.addUniteeStringProperty("RUN-ID", ArjunaProperty.RUNID);
		
		if ((this.getUserOption(this.integrator.getPropPathForEnum(ArjunaProperty.SESSION_NAME)) != null) && (pickerProvided)){
			Console.displayError("You can not pass picker switches along with -s (or --session-name) switch for user defined session.");
			Console.displayError("");
			help();	
			System.exit(1);	
		}
		
		ArjunaSingleton.INSTANCE.setPickerOptions(this.cliPickerOptions);
	}
	
	private void addFilter(TestPickerProperty type, String optName) throws Exception{
		String rawValue = this.getRawUserValue(optName);
		if (rawValue != null){
			cliPickerOptions.put(type, this.getRawUserValue(optName));
			pickerProvided = true;
		}
	}
	
	private <T extends Enum<T>> void addUniteeStringProperty(String cliOptName, T enumObj) throws Exception{
		String propPath = this.integrator.getPropPathForEnum(enumObj);
		ValueType type = this.integrator.expectedValueType(enumObj);
		if (this.getRawUserValue(cliOptName) == null) return;
		switch (type){
		case BOOLEAN:
			this.addValue(propPath, ValueFactory.createBooleanValue(this.getRawUserValue(cliOptName)));
			break;
		case ENUM:
			this.addValue(propPath, ValueFactory.createStringValue(this.getRawUserValue(cliOptName).toUpperCase()));
			break;
		case ENUM_LIST:
			Value val = null;
			if (nullEquivalentSet.contains(this.getRawUserValue(cliOptName).toLowerCase())){
				val = new StringListValue(new ArrayList<String>());
			} else {
				val = ValueFactory.createStringUCListValue(this.getRawUserValue(cliOptName));
			}
			this.addValue(propPath, val);
			break;
		case INTEGER:
			this.addValue(propPath, ValueFactory.createNumberValue(this.getRawUserValue(cliOptName)));
			break;
		case LONG:
			this.addValue(propPath, ValueFactory.createNumberValue(this.getRawUserValue(cliOptName)));
			break;
		case FLOAT:
			this.addValue(propPath, ValueFactory.createNumberValue(this.getRawUserValue(cliOptName)));
			break;
		case DOUBLE:
			this.addValue(propPath, ValueFactory.createNumberValue(this.getRawUserValue(cliOptName)));
			break;
		case NUMBER:
			this.addValue(propPath, ValueFactory.createNumberValue(this.getRawUserValue(cliOptName)));
			break;
		case LIST:
			this.addValue(propPath, ValueFactory.createStringListValue(this.getRawUserValue(cliOptName)));
			break;
		case NULL:
			throw new Exception("Some problem in configuring Unitee component defaults.");
		case NUMBER_LIST:
			break;
		case ANYREF:
			break;
		case STRING:
			this.addValue(propPath, ValueFactory.createStringValue(this.getRawUserValue(cliOptName)));
			break;
		case STRING_LIST:
			this.addValue(propPath, ValueFactory.createStringListValue(this.getRawUserValue(cliOptName)));
			break;
		default:
			break;
		
		}
	}

	public Map<TestPickerProperty,String> getCliPickerOptions() {
		return this.cliPickerOptions;
	}

	@Override
	public void setIntegrator(ComponentIntegrator integrator) {
		this.integrator = integrator;
	}
}
