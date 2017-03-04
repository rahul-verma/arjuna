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
package com.autocognite.pvt.batteries.config;

import java.util.HashMap;
import java.util.Map;

import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.batteries.integration.ComponentConfigurator;
import com.autocognite.pvt.batteries.lib.BatteriesConfigurator;
import com.autocognite.pvt.batteries.lib.ComponentIntegrator;

public class Batteries {
	public static boolean logFileDiscoveryInfo = false;
	private static ComponentIntegrator integrator = new ComponentIntegrator();

	public static void addConfigurator(ComponentConfigurator configurator) {
		configurator.setIntegrator(integrator);
		configurator.setBaseDir(integrator.getBaseDir());
		integrator.addConfigurator(configurator);
	}

	public static void init() throws Exception {
		integrator.init();
		Batteries.addConfigurator(new BatteriesConfigurator());
	}

	public static void init(String baseDir) throws Exception {
		integrator.init(baseDir);
		Batteries.addConfigurator(new BatteriesConfigurator());
	}

	public static String getBaseDir() {
		return integrator.getBaseDir();
	}
	
	public static String getProjectDir() {
		return integrator.getProjectDir();
	}

	public static void processConfigDefaults() throws Exception {
		integrator.processDefaults();
	}

	public static void processConfigProperties(HashMap<String, Value> properties) throws Exception {
		integrator.processConfigProperties(properties);
	}

	public static void processCentralUDVProperties(Map<String, Value> properties) {
		integrator.processCentralUDVProperties(properties);
	}

	public static void freezeCentralConfig() throws Exception {
		Configuration configuration = integrator.freezeCentralConfig();
	}

	public static class info {
		public static final String EXIT_ON_ERROR = "message.exit.on.error";
	}
}
