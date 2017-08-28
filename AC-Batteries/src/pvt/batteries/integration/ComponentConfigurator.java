package pvt.batteries.integration;

import java.util.Map;

import arjunasdk.interfaces.Value;
import pvt.batteries.lib.ComponentIntegrator;

public interface ComponentConfigurator {
	void processDefaults() throws Exception;

	void processConfigProperties(Map<String, Value> map) throws Exception;

	void loadComponent() throws Exception;

	String getBaseDir();

	void setBaseDir(String dir);

	ComponentIntegrator getIntegrator();

	void setIntegrator(ComponentIntegrator integrator);

	String getComponentName();
}
