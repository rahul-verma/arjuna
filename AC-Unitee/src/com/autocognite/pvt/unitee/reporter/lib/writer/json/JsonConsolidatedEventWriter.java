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

import com.autocognite.pvt.batteries.config.Batteries;
import com.autocognite.pvt.unitee.reporter.lib.event.Event;

public class JsonConsolidatedEventWriter extends JsonConsolidatedResultWriter<Event> {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private int counter = 0;
	
	public JsonConsolidatedEventWriter() throws Exception{
		super("events.json");
	}
	
	public void update(Event reportable) throws Exception {
		super.update(reportable.asJsonObject().toString());
	}
}
