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
package com.autocognite.pvt.unitee.reporter.lib.writer.console;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.log4j.Logger;

import com.autocognite.internal.arjuna.enums.TestAttribute;
import com.autocognite.internal.arjuna.enums.TestObjectAttribute;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.arjuna.enums.TestReportSection;
import com.autocognite.pvt.arjuna.enums.TestResultAttribute;
import com.autocognite.pvt.arjuna.enums.TestResultType;
import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.batteries.console.Console;
import com.autocognite.pvt.unitee.reporter.lib.DefaultObserver;
import com.autocognite.pvt.unitee.reporter.lib.test.TestResult;

public class ConsoleTestResultWriter extends DefaultObserver<TestResult> {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	String marker = new String(new char[100]).replace("\0", "-");
	private List<TestObjectAttribute> execTestObjectProps = null;
	private List<TestAttribute> execTestProps = null;
	private List<String> execCustomProps = null;
	private List<TestResultAttribute> execResultProps = null;
	Map<TestObjectAttribute,String> testObjectNames = null;
	Map<TestAttribute,String> testPropNames = null;
	Map<TestResultAttribute,String> testResultPropNames = null;
	Set<String> ignoreValues = new HashSet<String>(Arrays.asList("NA","NOT_SET", "null"));
	private Set<TestResultType> allowedRTypes = null;
	
	List<String> execTestHeaders = new ArrayList<String>();
	private boolean shouldIncludeAnnotatedTestProps;
	
	public ConsoleTestResultWriter() throws Exception{
		this.allowedRTypes = ArjunaInternal.getReportableTestTypes();
	}
	
	public void setUp() throws Exception{
		// Populate meta-data
		testObjectNames = ArjunaInternal.getTestObjectAttrNameMap();
		testPropNames = ArjunaInternal.getTestAttrNameMap();
		testResultPropNames = ArjunaInternal.getTestResultAttrNameMap();
		shouldIncludeAnnotatedTestProps = ArjunaInternal.shouldIncludeCustomPropsInReport();
		
		// Test Result Section		
		execTestObjectProps = ArjunaInternal.getTestObjectAttrListForTestReport();
		execTestProps = ArjunaInternal.getTestAttrList();
		execResultProps = ArjunaInternal.getTestResultAttrList();

		for (int i =0; i<this.execTestObjectProps.size(); i++){
			execTestHeaders.add(this.testObjectNames.get(execTestObjectProps.get(i)));
		}
		
		if (shouldIncludeAnnotatedTestProps){
			for (int i =0; i<this.execTestProps.size(); i++){
				execTestHeaders.add(this.testPropNames.get(execTestProps.get(i)));
			}
		}
		
		for (int i =0; i<this.execResultProps.size(); i++){
			execTestHeaders.add(this.testResultPropNames.get(execResultProps.get(i)));
		}	
		
		if (ArjunaInternal.displayObserverSetUpInfo){
			logger.debug(this.execTestHeaders);
		}
	}
	
	public void update(TestResult reportable) throws Exception {
		if (!ArjunaInternal.shouldIncludedReportSection(TestReportSection.TESTS)){
			return;
		}
		if (!allowedRTypes.contains(reportable.resultProps().result())){
			return;
		}
		List<String> values = new ArrayList<String>();

		values.addAll(reportable.objectPropStrings(this.execTestObjectProps));
		if (shouldIncludeAnnotatedTestProps){
			values.addAll(reportable.testPropStrings(this.execTestProps));
		}
		values.addAll(reportable.resultPropStrings(this.execResultProps));
	
		if (ArjunaInternal.displayObserverUpdateInfo){
			logger.debug(values);
		}
		Console.display(marker);
		for (int i=0; i < this.execTestHeaders.size(); i++){
			String header = execTestHeaders.get(i);
			String val = values.get(i);
			if (this.ignoreValues.contains(val)) continue;
			if (header.equals("Exception Trace")){
				Console.displayPaddedKeyValueExceptionTrace(execTestHeaders.get(i), values.get(i), 30);
			} else if (header.equals("Exception Message")){
				Console.displayPaddedKeyValueError(execTestHeaders.get(i), values.get(i), 30);
			} else {
				Console.displayPaddedKeyValue(execTestHeaders.get(i), values.get(i), 30);
			}
		}
		Console.display(marker);
	}	
	
}
