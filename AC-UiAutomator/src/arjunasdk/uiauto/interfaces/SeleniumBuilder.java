package arjunasdk.uiauto.interfaces;

import org.openqa.selenium.remote.DesiredCapabilities;

public interface SeleniumBuilder {

	void capabilities(DesiredCapabilities caps);

	UiDriver build() throws Exception;

}