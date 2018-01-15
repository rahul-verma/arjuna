package arjunasdk.uiauto.interfaces;

import org.openqa.selenium.remote.DesiredCapabilities;

import arjunasdk.uiauto.enums.UiAutomationContext;

public interface AppiumBuilder {

	void context(UiAutomationContext context);

	void appPath(String path);

	void platformName(String name);

	void platformVersion(String version);

	void deviceName(String name);

	void udid(String id);

	void capabilities(DesiredCapabilities caps);

	UiDriver build() throws Exception;

}