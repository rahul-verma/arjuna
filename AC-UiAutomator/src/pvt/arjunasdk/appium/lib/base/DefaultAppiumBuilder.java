package pvt.arjunasdk.appium.lib.base;

import java.util.HashMap;

import org.openqa.selenium.remote.DesiredCapabilities;

import arjunasdk.uiauto.interfaces.AppiumBuilder;
import arjunasdk.uiauto.interfaces.UiDriver;
import io.appium.java_client.remote.MobileCapabilityType;
import pvt.arjunasdk.uiauto.appium.AppiumNativeUiDriver;
import pvt.arjunasdk.uiauto.appium.AppiumWebUiDriver;
import pvt.arjunasdk.uiauto.enums.AppiumMobilePlatformType;
import pvt.arjunasdk.uiauto.enums.UiAutomationContext;
import pvt.arjunasdk.uiauto.enums.UiAutomatorPropertyType;
import pvt.arjunasdk.uiautomator.UiAutomator;
import pvt.batteries.config.Batteries;
import pvt.batteries.exceptions.Problem;

public class DefaultAppiumBuilder implements AppiumBuilder {
	private DesiredCapabilities caps = new DesiredCapabilities();
	private UiAutomationContext context = UiAutomationContext.MOBILE_WEB;
	
	public DefaultAppiumBuilder(){
		caps = new DesiredCapabilities();		
	}
	
	/* (non-Javadoc)
	 * @see arjunasdk.uiauto.interfaces.AppiumBuilder#automationContext(pvt.arjunasdk.uiauto.enums.UiAutomationContext)
	 */
	@Override
	public void automationContext(UiAutomationContext context){
		this.context = context;
	}
	
	/* (non-Javadoc)
	 * @see arjunasdk.uiauto.interfaces.AppiumBuilder#appPath(java.lang.String)
	 */
	@Override
	public void appPath(String path){
		caps.setCapability(MobileCapabilityType.APP, path);
	}
	
	/* (non-Javadoc)
	 * @see arjunasdk.uiauto.interfaces.AppiumBuilder#platformName(java.lang.String)
	 */
	@Override
	public void platformName(String name){
		caps.setCapability(MobileCapabilityType.PLATFORM_NAME, name);
	}
	
	/* (non-Javadoc)
	 * @see arjunasdk.uiauto.interfaces.AppiumBuilder#platformVersion(java.lang.String)
	 */
	@Override
	public void platformVersion(String version){
		caps.setCapability(MobileCapabilityType.PLATFORM_VERSION, version);
	}
	
	/* (non-Javadoc)
	 * @see arjunasdk.uiauto.interfaces.AppiumBuilder#deviceName(java.lang.String)
	 */
	@Override
	public void deviceName(String name){
		caps.setCapability(MobileCapabilityType.DEVICE_NAME, name);
	}
	
	/* (non-Javadoc)
	 * @see arjunasdk.uiauto.interfaces.AppiumBuilder#udid(java.lang.String)
	 */
	@Override
	public void udid(String id){
		caps.setCapability(MobileCapabilityType.UDID, id);
	}
	
	/* (non-Javadoc)
	 * @see arjunasdk.uiauto.interfaces.AppiumBuilder#capabilities(org.openqa.selenium.remote.DesiredCapabilities)
	 */
	@Override
	public void capabilities(DesiredCapabilities caps){
		caps.merge(caps);
	}
	
	/* (non-Javadoc)
	 * @see arjunasdk.uiauto.interfaces.AppiumBuilder#build()
	 */
	@Override
	public UiDriver build() throws Exception{
		UiDriver appium = null;
		switch (this.context){
		case MOBILE_NATIVE:
			appium = new AppiumNativeUiDriver();
			break;
		case MOBILE_WEB:
			appium = new AppiumWebUiDriver();
			break;
		default:
			throwUnsupportedAutomationContextException(context);
		}
		appium.setCapabilities(caps.asMap());
		return appium;
	}
	
	public UiDriver throwUnsupportedAutomationContextException(UiAutomationContext context) throws Exception{
		throw new Problem(
				Batteries.getComponentName("UI_AUTOMATOR"),
				"Appium Builder",
				"build",
				UiAutomator.problem.FACTORY_AUTOMATOR_UNSUPPORTED_CONTEXT,
				Batteries.getProblemText(
						UiAutomator.problem.FACTORY_AUTOMATOR_UNSUPPORTED_CONTEXT,
						UiAutomator.getAutomationContextName(context))
			);		
	}

}
