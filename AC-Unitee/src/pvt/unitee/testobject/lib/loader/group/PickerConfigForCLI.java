package pvt.unitee.testobject.lib.loader.group;

import java.util.Arrays;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

import arjunasdk.sysauto.batteries.DataBatteries;
import pvt.batteries.config.Batteries;
import pvt.unitee.enums.PickerTargetType;
import pvt.unitee.enums.TestPickerProperty;

public class PickerConfigForCLI extends AbstractPickerConfig{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private Map<TestPickerProperty, String> options = null;
	
	public PickerConfigForCLI(Map<TestPickerProperty, String> options) throws Exception {
		super();
		this.options = options;
	}
		
	public void process() throws Exception{
		logger.debug("Configuring picker: " + options);
		for (TestPickerProperty cProp: options.keySet()){
			this.configure(cProp, options.get(cProp));
		}
		validate();
		determineTarget();
	}
	
	private void determineTarget() throws PickerMisConfiguration{
		if (this.isPackageConsiderOrIgnoreOptionProvided()){
			this.setTargetType(PickerTargetType.PACKAGES);
		} else if (this.isClassConsiderOrIgnoreOptionProvided()){
			if (this.getPackageName() == null){
				throw new PickerMisConfiguration();
			}
			
			if (!this.getPackageName().matches("[\\.a-zA-Z0-9]+")){
				throw new PickerMisConfiguration();
			}
			this.setTargetType(PickerTargetType.CLASSES);
		} else if (this.isMethodConsiderOrIgnoreOptionProvided()){
			if (this.getPackageName() == null){
				throw new PickerMisConfiguration();
			}
			
			if (!this.getPackageName().matches("[\\.a-zA-Z0-9]+")){
				throw new PickerMisConfiguration();
			}
			
			if (this.getClassName() == null){
				throw new PickerMisConfiguration();
			}
			
			if (!this.getClassName().matches("[\\.a-zA-Z0-9]+")){
				throw new PickerMisConfiguration();
			}
			
			this.setTargetType(PickerTargetType.METHODS);
		} else if ((this.getPackageName() != null) && (this.getClassName() != null)){
			this.setTargetType(PickerTargetType.CLASSES);
			if ((!this.getPackageName().matches("[\\.a-zA-Z0-9]+")) || (!this.getClassName().matches("[\\a-zA-Z0-9]+"))){
				throw new PickerMisConfiguration();
			}
			this.configureClassConsiderPatterns(Arrays.asList("NONRX::" + this.getClassName()));
		} else if (this.getPackageName() != null) {
			this.setTargetType(PickerTargetType.PACKAGES);
			if (!this.getPackageName().matches("[\\.a-zA-Z0-9]+")){
				throw new PickerMisConfiguration();
			}
			this.configurePackageConsiderPatterns(Arrays.asList("NONRX::" + this.getPackageName()));			
		}
	}
	
	private void configure(TestPickerProperty type, String value) throws Exception{
		if (value == null) return;
		List<String> rawList = DataBatteries.split(value, ",");
		switch(type){
		case CLASS_CONSIDER_PATTERNS:
			configureClassConsiderPatterns(rawList);
			break;
		case CLASS_IGNORE_PATTERNS:
			 configureClassIgnorePatterns(rawList);
			break;
		case METHOD_CONSIDER_PATTERNS:
			configureMethodConsiderPatterns(rawList);
			break;
		case METHOD_IGNORE_PATTERNS:
			configureMethodIgnorePatterns(rawList);
			break;
		case PACKAGE_CONSIDER_PATTERNS:
			configurePackageConsiderPatterns(rawList);
			break;
		case PACKAGE_IGNORE_PATTERNS:
			configurePackageIgnorePatterns(rawList);
			break;
		case CLASS_NAME:
			configureClassName(value);
			break;
		case PACKAGE_NAME:
			configurePackageName(value);
			break;
		default:
			break;
		}
	}

}