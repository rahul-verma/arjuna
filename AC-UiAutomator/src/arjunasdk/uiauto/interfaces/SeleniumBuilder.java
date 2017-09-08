package arjunasdk.uiauto.interfaces;

import org.openqa.selenium.remote.DesiredCapabilities;

import arjunasdk.enums.Browser;

public interface SeleniumBuilder {

	void capabilities(DesiredCapabilities caps);

	UiDriver build() throws Exception;

	void browser(Browser browser);

}