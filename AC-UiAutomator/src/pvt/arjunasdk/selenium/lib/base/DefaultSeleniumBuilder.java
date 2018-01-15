package pvt.arjunasdk.selenium.lib.base;

import java.util.HashMap;

import org.apache.poi.util.SystemOutLogger;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.safari.SafariDriver;

import arjunasdk.enums.Browser;
import arjunasdk.sysauto.batteries.SystemBatteries;
import arjunasdk.uiauto.enums.UiAutomationContext;
import arjunasdk.uiauto.interfaces.SeleniumBuilder;
import arjunasdk.uiauto.interfaces.UiDriver;
import io.appium.java_client.remote.MobileCapabilityType;
import pvt.arjunasdk.uiauto.appium.AppiumNativeUiDriver;
import pvt.arjunasdk.uiauto.appium.AppiumWebUiDriver;
import pvt.arjunasdk.uiauto.enums.AppiumMobilePlatformType;
import pvt.arjunasdk.uiauto.enums.UiAutomatorPropertyType;
import pvt.arjunasdk.uiauto.selenium.SeleniumWebUiDriver;
import pvt.arjunasdk.uiautomator.UiAutomator;
import pvt.batteries.config.Batteries;
import pvt.batteries.exceptions.Problem;

public class DefaultSeleniumBuilder implements SeleniumBuilder {
	private DesiredCapabilities browserCaps = new DesiredCapabilities();
	private DesiredCapabilities otherCaps = new DesiredCapabilities();
	private UiAutomationContext context = UiAutomationContext.PC_WEB;
	private String appTitle = null;
	private Browser browser = null;
	
	public DefaultSeleniumBuilder() throws Exception{
		this.browser = Batteries.value(UiAutomatorPropertyType.BROWSER_PC_DEFAULT).asEnum(Browser.class);
	}
	
	@Override
	public void browser(Browser browser){
		this.browser = browser;
	}
	
	/* (non-Javadoc)
	 * @see arjunasdk.uiauto.interfaces.SeleniumBuilder#capabilities(org.openqa.selenium.remote.DesiredCapabilities)
	 */
	@Override
	public void capabilities(DesiredCapabilities caps){
		otherCaps.merge(caps);
	}
	
	/* (non-Javadoc)
	 * @see arjunasdk.uiauto.interfaces.SeleniumBuilder#build()
	 */
	@Override
	public UiDriver build() throws Exception{
		SeleniumWebUiDriver selenium = new SeleniumWebUiDriver();
		selenium.setBrowser(browser);
		selenium.init();
		switch (this.browser){
		case FIREFOX:
			setFirefoxCaps();
			break;
		case CHROME:
			setChromeCaps();
			break;
		case SAFARI:
			setSafariCaps();
			break;	
		}
		
		browserCaps.merge(otherCaps);
		selenium.setCapabilities(browserCaps.asMap());
		selenium.load();
		return selenium;
	}


	private DesiredCapabilities getFireFoxCapabilitiesSkeleton() { 
		return DesiredCapabilities.firefox();
	}

	private DesiredCapabilities getChromeCapabilitiesSkeleton() {
		return DesiredCapabilities.chrome();
	}

	private DesiredCapabilities getSafariCapabilitiesSkeleton() {
		return DesiredCapabilities.safari();
	}
	
	private void setFirefoxCaps() throws Exception {
		this.appTitle = Batteries.value(UiAutomatorPropertyType.FIREFOX_WINDOWNAME).asString();
		String os = SystemBatteries.getOSName();
		String binaryName = null;
		if (os.startsWith("Window")){
			binaryName = "geckodriver.exe";
		} else if (os.startsWith("Mac")) {
			binaryName = "geckodriver";
		}
		System.setProperty("webdriver.gecko.driver", Batteries.value(UiAutomatorPropertyType.TOOLS_UIDRIVERS_DIR).asString() + "/" + binaryName);

		browserCaps = getFireFoxCapabilitiesSkeleton();
		//driver = new FirefoxDriver(capabilities);
		FirefoxProfile profile = new FirefoxProfile();
		//profile..setEnableNativeEvents(true);
		browserCaps.setCapability(FirefoxDriver.PROFILE, profile);
	}

	private void setChromeCaps() throws Exception {
		this.appTitle = Batteries.value(UiAutomatorPropertyType.CHROME_WINDOWNAME).asString();
		String os = SystemBatteries.getOSName();
		String chromeDriverBinaryName = null;
		if (os.startsWith("Window")){
			chromeDriverBinaryName = "chromedriver.exe";
		} else if (os.startsWith("Mac")) {
			chromeDriverBinaryName = "chromedriver";
		}

		System.setProperty("webdriver.chrome.driver", Batteries.value(UiAutomatorPropertyType.TOOLS_UIDRIVERS_DIR).asString() + "/" + chromeDriverBinaryName);
		browserCaps = getChromeCapabilitiesSkeleton();
	}

	private void setSafariCaps() throws Exception {
		this.appTitle = Batteries.value(UiAutomatorPropertyType.SAFARI_WINDOWNAME).asString();
		browserCaps = getSafariCapabilitiesSkeleton();
	}

}
