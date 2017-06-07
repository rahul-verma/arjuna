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
package pvt.unitee.testobject.lib.loader;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

import org.apache.log4j.Logger;

import pvt.arjunapro.ArjunaInternal;
import pvt.batteries.config.Batteries;
import pvt.batteries.discoverer.DiscoveredFile;
import pvt.batteries.discoverer.DiscoveredFileAttribute;
import pvt.batteries.discoverer.FileAggregator;
import pvt.batteries.discoverer.FileDiscoverer;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.enums.TestLanguage;
import pvt.unitee.testobject.lib.loader.group.TestLoader;

public class TestDefinitionsProcessor {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private ArrayList<String> classes = null;
//	ArrayList<AuthoredTest> tests = new ArrayList<AuthoredTest>();
	private HashMap<TestLanguage, TestDefinitionsLoader> testDefinitionLoaders = new HashMap<TestLanguage, TestDefinitionsLoader>();
	private HashMap<TestLanguage, TestLoader> testLoaders = new HashMap<TestLanguage, TestLoader>();

	public TestDefinitionsProcessor() throws Exception {
	}

	public void setTestDefinitionsLoader(TestLanguage lang, TestDefinitionsLoader loader){
		if (ArjunaInternal.displayLoadingInfo){
			logger.debug(String.format("Set test loader for %s: %s", lang, loader.getClass()));
		}
		this.testDefinitionLoaders.put(lang, loader);
	}
	
//	public ArrayList<AuthoredTest> getQueue() throws Exception{
//		return this.tests;
//	}
	
	private TestLanguage extToLanguage(String ext){
		String ucExt = ext.toUpperCase();
		if (ucExt.equals("CLASS")){
			return TestLanguage.JAVA;
		} else {
			return null;
		}
	}
	
	public void populate() throws Exception{
		if (ArjunaInternal.displayDiscoveryInfo){
			logger.debug("Now finding tests inside: " + Batteries.value(ArjunaProperty.DIRECTORY_PROJECT_TESTS).asString());
			logger.debug(Batteries.getInfoMessageText(ArjunaInternal.info.TEST_DISCOVERY_START));	
		}
		String startDir = Batteries.value(ArjunaProperty.DIRECTORY_PROJECT_TESTS).asString();
		FileAggregator aggregator = new FileAggregator();
		FileDiscoverer discoverer = new FileDiscoverer(aggregator, startDir);
		discoverer.discover();
		
		for (TestLanguage lang: this.testDefinitionLoaders.keySet()){
			testDefinitionLoaders.get(lang).setTestDir(startDir);
		}
		populateClassQueue(aggregator) ;	

		for (TestLanguage lang: this.testDefinitionLoaders.keySet()){
			testDefinitionLoaders.get(lang).validateDependencies();
		}
	}

	private void populateClassQueue(FileAggregator aggregator) throws Exception{
		Iterator<DiscoveredFile> iter = aggregator.getIterator();
		//		aggregator.enumerate();
		TestDefinitionsLoader testDefLoader = null;
		TestDefinitionsLoader testLoader = null;
		while(iter.hasNext()){
			DiscoveredFile f = iter.next();
			TestLanguage lang = this.extToLanguage(f.getAttribute(DiscoveredFileAttribute.EXTENSION));
			if (ArjunaInternal.displayDiscoveryInfo){
				logger.debug("Found: " + f.getAttribute(DiscoveredFileAttribute.FULL_NAME));
			}
//			logger.debug(lang);
			if ((lang == null) || (!this.testDefinitionLoaders.containsKey(lang))){
				// not supported
				if (ArjunaInternal.displayDiscoveryInfo){
					logger.debug("Not supported");
				}
				continue;
			}
			
			testDefLoader = this.testDefinitionLoaders.get(lang);
			
			testDefLoader.load(f);
//			if (tests != null){
//				for (AuthoredTest test: tests){
//					this.tests.add(test);
//				}
//			}
		}
	}
}
