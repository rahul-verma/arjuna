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
package com.autocognite.pvt.unitee.reporter.lib.writer.json;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.pvt.arjuna.enums.ArjunaProperty;
import com.autocognite.pvt.unitee.reporter.lib.test.TestResult;

public class JsonTestResultWriter extends JsonResultWriter<TestResult> {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	JsonConsolidatedTestResultWriter childWriter = null;
	
	public JsonTestResultWriter() throws Exception{
		super(RunConfig.value(ArjunaProperty.DIRECTORY_RUNID_REPORT_JSON_RAW_TESTS).asString());
		childWriter = new JsonConsolidatedTestResultWriter();
	}
	
	public void update(TestResult reportable) throws Exception {
		String jsonString = reportable.asJsonObject().toString();
		super.update(this.createFileID(reportable.objectProps().objectId()), jsonString);
		childWriter.update(jsonString);
	}
	
	public void setUp() throws Exception{
		super.setUp();
		childWriter.setUp();
	}

	public void tearDown() throws Exception{
		super.tearDown();
		childWriter.tearDown();
	}
}
