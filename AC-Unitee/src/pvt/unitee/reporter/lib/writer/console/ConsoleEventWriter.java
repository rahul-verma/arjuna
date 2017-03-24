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
package pvt.unitee.reporter.lib.writer.console;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.log4j.Logger;

import com.arjunapro.testauto.console.Console;

import pvt.arjunapro.ArjunaInternal;
import pvt.arjunapro.enums.EventAttribute;
import pvt.arjunapro.enums.TestReportSection;
import pvt.batteries.config.Batteries;
import pvt.unitee.reporter.lib.DefaultObserver;
import pvt.unitee.reporter.lib.event.Event;

public class ConsoleEventWriter extends DefaultObserver<Event> {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	String marker = new String(new char[100]).replace("\0", "-");
	Set<String> ignoreValues = new HashSet<String>(Arrays.asList("NA","NOT_SET", "null"));
	private List<EventAttribute> activityInfoProps = null;
	private List<String> activityHeaders = new ArrayList<String>();
	
	public ConsoleEventWriter() throws Exception{
	}
	
	public void setUp() throws Exception{
		Map<EventAttribute,String> activityPropNames = ArjunaInternal.getEventAttrNameMap();
		activityInfoProps = ArjunaInternal.getEventAttrList();		
		for (EventAttribute prop: activityInfoProps){
			this.activityHeaders.add(activityPropNames.get(prop));
		}	
	}
	
	public void update(Event reportable) throws Exception {
		if (!ArjunaInternal.shouldIncludedReportSection(TestReportSection.EVENTS)){
			return;
		}
		Console.display(marker);
		List<String> values = reportable.infoPropStrings(this.activityInfoProps);
		for (int i=0; i < this.activityHeaders.size(); i++){
			Console.displayPaddedKeyValue(activityHeaders.get(i), values.get(i), 30);
		}
		Console.display(marker);
	}
	
}
