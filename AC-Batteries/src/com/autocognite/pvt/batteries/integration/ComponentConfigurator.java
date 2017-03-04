package com.autocognite.pvt.batteries.integration;

import java.util.HashMap;

import com.autocognite.batteries.value.Value;
import com.autocognite.pvt.batteries.lib.ComponentIntegrator;

public interface ComponentConfigurator {
	void processDefaults() throws Exception;

	void processConfigProperties(HashMap<String, Value> properties) throws Exception;

	void loadComponent() throws Exception;

	String getBaseDir();

	void setBaseDir(String dir);

	ComponentIntegrator getIntegrator();

	void setIntegrator(ComponentIntegrator integrator);

	String getComponentName();
}
