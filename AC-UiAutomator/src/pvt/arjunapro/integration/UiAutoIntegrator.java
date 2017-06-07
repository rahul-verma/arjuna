package pvt.arjunapro.integration;

import pvt.batteries.integration.ComponentConfigurator;
import pvt.uiautomator.lib.config.UiAutomatorConfigurator;

public class UiAutoIntegrator {

	public static ComponentConfigurator getComponentConfigurator() {
		return new UiAutomatorConfigurator();
	}
}
