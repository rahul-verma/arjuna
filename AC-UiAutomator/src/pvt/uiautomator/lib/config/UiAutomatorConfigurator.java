package pvt.uiautomator.lib.config;

import java.util.ArrayList;
import java.util.HashMap;

import com.arjunapro.testauto.interfaces.Value;

import pvt.batteries.ds.Message;
import pvt.batteries.ds.MessagesContainer;
import pvt.batteries.ds.Name;
import pvt.batteries.ds.NamesContainer;
import pvt.batteries.hocon.HoconReader;
import pvt.batteries.hocon.HoconResourceReader;
import pvt.batteries.integration.AbstractComponentConfigurator;
import pvt.batteries.property.ConfigProperty;
import pvt.batteries.property.ConfigPropertyBatteries;
import pvt.batteries.property.ConfigPropertyBuilder;
import pvt.uiauto.enums.UiAutomationContext;
import pvt.uiautomator.UiAutomator;

public class UiAutomatorConfigurator extends AbstractComponentConfigurator{
	private ConfigPropertyBuilder<UiAutomatorPropertyType> builder = new ConfigPropertyBuilder<UiAutomatorPropertyType>();
	private HashMap<String, UiAutomatorPropertyType> pathToEnumMap = new HashMap<String, UiAutomatorPropertyType>();
	private HashMap<UiAutomatorPropertyType, String> enumToPathMap = new HashMap<UiAutomatorPropertyType, String>();
	
	public UiAutomatorConfigurator() {
		super("UiAutomator");
		for (UiAutomatorPropertyType e: UiAutomatorPropertyType.class.getEnumConstants()){
			String path = ConfigPropertyBatteries.enumToPropPath(e);
			pathToEnumMap.put(path.toUpperCase(), e);
			enumToPathMap.put(e, path.toUpperCase());
		}
	}
	
	private UiAutomatorPropertyType codeForPath(String propPath){
		return pathToEnumMap.get(propPath.toUpperCase());
	}
	
	protected void handleStringConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createStringProperty(codeForPath(propPath), propPath, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleIntConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createNumberProperty(codeForPath(propPath), propPath, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleDoubleConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createNumberProperty(codeForPath(propPath), propPath, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleCoreDirPath(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createCoreDirPath(codeForPath(propPath), propPath, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	protected void handleBooleanConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception{
		ConfigProperty prop = ConfigPropertyBatteries.createBooleanProperty(codeForPath(propPath), propPath, configValue, purpose, visible);
		registerProperty(prop);		
	}
	
	private void handleUiContextConfig(String propPath, Value configValue, String purpose, boolean visible) throws Exception {
		ConfigProperty prop = ConfigPropertyBatteries.createEnumProperty(codeForPath(propPath), propPath, UiAutomationContext.class, configValue, purpose, visible);
		registerProperty(prop);	
	}
		
	public void processConfigProperties(HashMap<String, Value> properties) throws Exception{
		@SuppressWarnings("unchecked")
		HashMap<String, Value> tempMap = (HashMap<String, Value>) properties.clone();
		for (String propPath: tempMap.keySet()){
			String ucPropPath = propPath.toUpperCase();
			Value cValue = tempMap.get(propPath);
			if (pathToEnumMap.containsKey(ucPropPath)){
				switch(pathToEnumMap.get(ucPropPath)){
				case APPIUM_HUB_HOST:
					handleStringConfig(propPath, cValue, "Appium Hub Host Name", true);
					break;
				case APPIUM_HUB_PORT:
					handleIntConfig(propPath, cValue, "Appium Hub Port Number", true);
					break;
				case APPIUM_HUB_URL:
					handleStringConfig(propPath, cValue, "Appium Hub URL", false);
					break;
				case APP_MOBILE_MAXWAIT:
					handleIntConfig(propPath, cValue, "Mobile App Max Wait Time for Element Identification", true);
					break;
				case APP_MOBILE_PATH:
					handleStringConfig(propPath, cValue, "Mobile App Path on Test Machine", true);
					break;
				case APP_PC_MAXWAIT:
					handleIntConfig(propPath, cValue, "PC App Max Wait Time for Element Identification", true);
					break;
				case BROWSER_MOBILE_DEFAULT:
					handleStringConfig(propPath, cValue, "Default Mobile Web Browser", true);
					break;
				case BROWSER_MOBILE_MAXWAIT:
					handleIntConfig(propPath, cValue, "Mobile Web Browser Max Wait Time for Element Identification", true);
					break;
				case BROWSER_MOBILE_PROXY_HOST:
					handleStringConfig(propPath, cValue, "Mobile Web Browser Proxy Host Name", true);
					break;
				case BROWSER_MOBILE_PROXY_ON:
					handleBooleanConfig(propPath, cValue, "Should enable proxy for Web Browser on Mobile?", true);
					break;
				case BROWSER_MOBILE_PROXY_PORT:
					handleIntConfig(propPath, cValue, "Mobile Web Browser Proxy Port Number", true);
					break;
				case BROWSER_MOBILE_PROXY_URL:
					handleStringConfig(propPath, cValue, "Mobile Web Browser Proxy URL", false);
					break;
				case BROWSER_PC_DEFAULT:
					handleStringConfig(propPath, cValue, "Default Web Browser for PC", true);
					break;
				case BROWSER_PC_MAXWAIT:
					handleIntConfig(propPath, cValue, "PC Web Browser Max Wait Time for Element Identification", true);
					break;
				case BROWSER_PC_PROXY_HOST:
					handleStringConfig(propPath, cValue, "PC Web Browser Proxy Host Name", true);
					break;
				case BROWSER_PC_PROXY_ON:
					handleBooleanConfig(propPath, cValue, "Should enable proxy for Web Browser on PC?", true);
					break;
				case BROWSER_PC_PROXY_PORT:
					handleIntConfig(propPath, cValue, "PC Web Browser Proxy Port Number", true);
					break;
				case BROWSER_PC_PROXY_URL:
					handleStringConfig(propPath, cValue, "PC Web Browser Proxy URL", false);
					break;
				case CHROME_WINDOWNAME:
					handleStringConfig(propPath, cValue, "Chrome Web Browser's Window Name", false);
					break;
				case DIRECTORY_TOOLS_UIDRIVERS:
					handleCoreDirPath(propPath, cValue, "UI Drivers directory", false);
					break;
				case DIRECTORY_UI_IMAGES:
					handleCoreDirPath(propPath, cValue, "UI Images Directory (Identification Images)", false);
					break;
				case DIRECTORY_UI_MAPS:
					handleCoreDirPath(propPath, cValue, "UI Maps Directory (Page Definitions)", false);
					break;
				case FIREFOX_WINDOWNAME:
					handleStringConfig(propPath, cValue, "Firefox Web Browser's Window Name", false);
					break;
				case MOBILE_DEVICE_UDID:
					handleStringConfig(propPath, cValue, "Mobile Device UDID", true);
					break;
				case MOBILE_DEVICE_NAME:
					handleStringConfig(propPath, cValue, "Mobile Device Name", true);
					break;
				case MOBILE_PLATFORM_NAME:
					handleStringConfig(propPath, cValue, "Mobile Platform Name", true);
					break;
				case MOBILE_PLATFORM_VERSION:
					handleStringConfig(propPath, cValue, "Mobile Platform Version", true);
					break;
				case SAFARI_WINDOWNAME:
					handleStringConfig(propPath, cValue, "Safari Web Browser's Window Name", false);
					break;
				case SIKULI_COMPARISON_SCORE:
					handleDoubleConfig(propPath, cValue, "Sikuli Min Comparison Score for successful match", true);
					break;
				case SIKULI_MAXWAIT:
					handleIntConfig(propPath, cValue, "Sikuli Max Wait Time for Image Identification", true);
					break;
				case UIAUTO_RUNCONTEXT:
					handleUiContextConfig(propPath, cValue, "Current UI Automation Context", true);
					break;
				default:
					break;

				
				}
				
				properties.remove(propPath);
			}
		}
		
	}

	public void processDefaults() throws Exception {
		UiAutomator.init();
		HoconReader reader = new HoconResourceReader(this.getClass().getResourceAsStream("/com/autocognite/pvt/text/uiautomator.conf"));
		super.processDefaults(reader);
	}

	@Override
	public void loadComponent() throws Exception {
		// TODO Auto-generated method stub
		
	}

	@Override
	protected ArrayList<MessagesContainer> getAllMessages() {
		ArrayList<MessagesContainer> containers = new ArrayList<MessagesContainer>();

		MessagesContainer problemMessages = new MessagesContainer("PROBLEM_MESSAGES");
		problemMessages.add(new Message(	
					UiAutomator.problem.APPIUM_UNSUPPORTED_PLATFORM,
					"Unsupported platform: %s"
		));
				
		problemMessages.add(new Message(
				UiAutomator.problem.APPIUM_UNSUPPORTED_BROWSER,
					"Unsupported browser %s for platform: %s"
		));
		
		problemMessages.add(new Message(
				UiAutomator.problem.APPIUM_UNREACHABLE_BROWSER,
				"Not able to reach Appium Server for %s automation."
				));
		containers.add(problemMessages);	
		
		problemMessages.add(new Message(	
				UiAutomator.problem.COMPARISON_IMAGE_NOT_FOUND,
				"Image file not found at path: %s"
			));
			
	problemMessages.add(new Message(
			UiAutomator.problem.COMPARISON_NOT_POSSIBLE,
				"Image files are not comparable. Neither one seems to contain the other (size-wise). Left Image: %s. Right Image: %s."
	));
	
	/* UI Automator */
	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_IDENTIFICATION_FAILURE,
			"%s failed to %s with %sproperties %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_GET_INSTANCE_FAILURE,
			"%s failed to %s of element with %sproperties %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_WAIT_FAILURE,
			"%s waited for %s seconds, without success for %s element with %sproperties %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_ACTION_FAILURE,
			"%s failed to %s element with %sproperties %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_GET_ATTR_FAILURE,
			"%s failed to get %s element with %sproperties %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.ACTION_MULTIELEMENT_FAILURE,
			"%s failed to %s element with %sproperties %s and then %s element with %sproperties %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_UNSUPPORTED_ACTION,
			"Unsupported action: %s for element with %sproperties %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_INQUIRY_FAILURE,
			"%s was unable to check %s element with %sproperties %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.PAGE_NULL_AUTOMATOR,
			"%s page was provided a null automator."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.PAGE_UNDEFINED_ELEMENT,
			"Element with name %s is not defined for %s page."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.COMPOSITE_PAGE_CONSTRUCTOR_NULL_AUTOMATOR,
			"Composite Page was provided a null value for %s Automator."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.COMPOSITE_PAGE_GET_AUTOMATOR_NULL,
			"%s Automator is not a valid automator for composite page. Allowed Type: %s Automator."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.MAPFILE_RELATIVE_PATH,
			"Page Mapper was provided a file with relative path: %s. Expected absolute path."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.MAPFILE_NOT_FOUND,
			"Page Mapper was not able to find the source map file: %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.MAPFILE_NOTAFILE,
			"Page Mapper was provided a path which is not a file: %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.UNSUPPORTED_IDENTIFIER,
			"Unsupported identifier: %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.UNSUPPORTED_MULTIPLE_IDENTIFIERS,
			"Multiple identifiers not supported: %s"
			));

	problemMessages.add(new Message(
			UiAutomator.problem.PROPERTY_DOES_NOT_EXIST,
			"Property with the name %s does not exist in Property Manager."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.UNSUPPORTED_MAP_FILE_FORMAT,
			"Unsupported map file format: %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.AUTOMATOR_UNSUPPORTED_ACTION,
			"Unsupported action for: %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.COMPOSITE_PAGE_NULL_AUTOMATOR,
			"Null Automator provided to Composite Page for %s automation."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.COMPOSITE_PAGE_NONEXISTING_LABEL,
			"A page fragment with the label %s does not exist in %s composite page."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.COMPOSITE_PAGE_NULL_LABEL,
			"Null was provided as the page fragment name for %s composite page."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.UI_ELEMENT_INVALID_METADATA,
			"An invalid element definition was provided for %s context with meta-data: %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.UI_NULL_ELEMENT,
			"Null was provided as element name for %s UI."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.FACTORY_AUTOMATOR_MOBILE_NULL_APP_PATH,
			"Null value provided for mobile app path."
			));	

	problemMessages.add(new Message(
			UiAutomator.problem.FACTORY_AUTOMATOR_UNSUPPORTED_CONTEXT,
			"%s automation context is not supported by Automator Factory."
			));	

	problemMessages.add(new Message(
			UiAutomator.problem.FACTORY_METHOD_APPPATH_NOT_APPLICABLE,
			"Wrong factory method used for %s automation context. Use getAutomator(AutomationContext context)."
			));	

	problemMessages.add(new Message(
			UiAutomator.problem.UIAUTO_CONTEXT_HANDLER_NO_AUTO_FOR_LABEL,
			"No automator present with label: %s"
			));	

	problemMessages.add(new Message(
			UiAutomator.problem.UIAUTO_CONTEXT_HANDLER_NULL_AUTOMATOR,
			"Null automator provided."
			));
	//		
	//problemMessages.add(new Message(
	//			UiAutomator.problem.UIAUTO_CONTEXT_HANDLER_ABSENT_PROPERTIES,
	//			String.format("To use AutomationContext class, you must set the value of %s property.", Properties.UI_AUTO_CONTEXTS_INCLUDE)
	//));

	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_NEGATIVE_INEDX,
			"Negative index used for index based instance retieval for element with %sproperties %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_ZERO_ORDINAL,
			"Ordinal should be >= 1 in ordinal based instance retrieval for element with %sproperties %s."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_EMPTY_QUEUE,
			"Exception in instance retrieval for element with %sproperties %s. The element instance queue is empty. Try calling element.identifyAll() explicitly."
			));

	problemMessages.add(new Message(
			UiAutomator.problem.ELEMENT_UNSUPPORTED_SELECT_ACTION,
			"%s method works only for Drop downs and radio buttons. Not supported for element with %sproperties %s."
			));

		return containers;
	}

	@Override
	protected ArrayList<NamesContainer> getAllNames() {
		ArrayList<NamesContainer> containers = new ArrayList<NamesContainer>();
		NamesContainer objectNames = new NamesContainer("COMPONENT_NAMES");	
		objectNames.add(new Name("UI_AUTOMATOR", "UI Automator"));
		objectNames.add(new Name("APPIUM_AUTOMATOR", "Appium Automator"));
		objectNames.add(new Name("APPIUM_WEB_UIDRIVER", "Appium Web UI Driver"));
		objectNames.add(new Name("APPIUM_NATIVE_UIDRIVER", "Appium Native UI Driver"));
		objectNames.add(new Name("APPIUM_HYBRID_UIDRIVER", "Appium Hybrid UI Driver"));
		objectNames.add(new Name("WEBDRIVER_AUTOMATOR", "WebDriver Automator"));
		objectNames.add(new Name("SIKULI_AUTOMATOR", "Sikuli Automator"));
		containers.add(objectNames);
		return containers;
	}
	
}
