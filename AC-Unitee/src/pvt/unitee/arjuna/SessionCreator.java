package pvt.unitee.arjuna;

import java.io.File;
import java.util.Map;

import arjunasdk.console.Console;
import pvt.batteries.lib.ComponentIntegrator;
import pvt.unitee.config.ArjunaSingleton;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.enums.PickerTargetType;
import pvt.unitee.enums.TestPickerProperty;
import pvt.unitee.testobject.lib.loader.group.PickerConfig;
import pvt.unitee.testobject.lib.loader.group.PickerConfigForCLI;
import pvt.unitee.testobject.lib.loader.group.PickerMisConfiguration;
import pvt.unitee.testobject.lib.loader.session.MSession;
import pvt.unitee.testobject.lib.loader.session.Session;
import pvt.unitee.testobject.lib.loader.session.UserDefinedSession;

public class SessionCreator {
	private String sessionName = null;
	private Session session = null;
	private Map<TestPickerProperty,String> cliPickerOptions = null;

	public SessionCreator(ComponentIntegrator integrator, Map<TestPickerProperty, String> options, String sessionName) throws Exception{
		this.sessionName = sessionName;
		this.cliPickerOptions = options;
		PickerConfig cliPickerConfig = createPickerConfigForCLIConfig();
		if (sessionName.trim().toUpperCase().equals("MSESSION")){
			PickerTargetType pType = cliPickerConfig.getTargetType();
			try{
				session = new MSession(cliPickerConfig);
			} catch (PickerMisConfiguration e){
				displayCLIPickerConfigError();
			} catch (Exception e){
				throw e;
			}
		} else {
			// User Defined Session Flow
			String sessionsDir = integrator.value(ArjunaProperty.DIRECTORY_PROJECT_SESSIONS).asString();
			File sDir = new File(sessionsDir);
			boolean matchFound = false;
			String sFileName = null;
			if (!sDir.isDirectory()){
				Console.displayError("Sessions directory does not exist: " + sDir);
				Console.displayError("Exiting...");
				System.exit(1);
			}
			
			boolean fileExistsButConfExtUsedInSessionName = false;
			for (File f: sDir.listFiles()){
				if (f.isFile()){
					if (f.getName().toUpperCase().equals(sessionName.toUpperCase() + "." + "CONF")){
						matchFound = true;
						sFileName = f.getName();
						break;
					}
					
					if ((sessionName.toUpperCase().endsWith(".CONF")) && (f.getName().toUpperCase().equals(sessionName.toUpperCase()))){
						fileExistsButConfExtUsedInSessionName = true;
					}
				}
			}
			
			if (!matchFound){
				if (fileExistsButConfExtUsedInSessionName){
					Console.displayError("Provide session name without the conf extension.");
				} else {
					Console.displayError("No session template found for session name: "  + sessionName);
					Console.displayError(String.format("Ensure that >>%s.conf<< file is present in >>%s<< directory.", sessionName.toUpperCase().replace(".CONF", ""), sessionsDir));
					if (sessionName.toUpperCase().endsWith(".CONF")){
						Console.displayError("Also, provide session name without the conf extension.");
					}
				}
				Console.displayError("Exiting...");
				System.exit(1);
			}
			
			session = new UserDefinedSession(sessionName, sessionsDir + "/" + sFileName);
		}
		
	}
	
	private PickerConfig createPickerConfigForCLIConfig() throws Exception{
		try{
			PickerConfig config = new PickerConfigForCLI(this.cliPickerOptions);
			config.process();
			return config;
		} catch (Exception e){
			displayCLIPickerConfigError();
		}
		
		return null;
	}
	
	public Session getSession() throws Exception {
		return this.session;
	}
	
	public static void displayCLIPickerConfigError() throws Exception{
		Console.displayError("Your test picker switches are not valid.");
		Console.displayError("Evaluate your usage in the light of following rules.");
		Console.displayError("Note: -pn, and -cn switches take single and actual name as argument. You can not provide regex patterns. Dot (.) is an allowed character but it is treated as a literal dot and not regex dot.");
		Console.displayError("Note: -i* and -c* switches take multiple comma separated names or regex patterns.");
		Console.displayError("Package Picker Valid Switch Combinations");
		Console.displayError("----------------------------------------");
		Console.displayError("-cp");
		Console.displayError("-pn");
		Console.displayError("-ip");
		Console.displayError("-cp -ip");
		Console.displayError("");
		Console.displayError("Class Picker Valid Switch Combinations");
		Console.displayError("--------------------------------------");
		Console.displayError("-pn -cc");
		Console.displayError("-pn -cn");
		Console.displayError("-pn -ic");
		Console.displayError("");
		Console.displayError("Method Picker Valid Switch Combinations");
		Console.displayError("--------------------------------------");
		Console.displayError("-pn -cn -cm");
		Console.displayError("-pn -cn -im");
		Console.displayError("");
		ArjunaSingleton.INSTANCE.getCliConfigurator().help();
		System.exit(1);			
	}
}
