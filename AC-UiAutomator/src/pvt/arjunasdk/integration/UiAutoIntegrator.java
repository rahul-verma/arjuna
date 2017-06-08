package pvt.arjunasdk.integration;

import pvt.arjunasdk.uiautomator.lib.config.UiAutomatorConfigurator;
import pvt.batteries.integration.ComponentConfigurator;

public class UiAutoIntegrator {

	public static ComponentConfigurator getComponentConfigurator() {
		return new UiAutomatorConfigurator();
	}
}
