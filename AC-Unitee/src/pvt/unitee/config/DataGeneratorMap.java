/*******************************************************************************
 * Copyright 2015-16 AutoCognite Testing Research Pvt Ltd
 * 
 * Website: www.AutoCognite.com
 * Email: support [at] autocognite.com
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/
package pvt.unitee.config;

import java.lang.annotation.Annotation;
import java.lang.reflect.Constructor;
import java.util.HashMap;
import java.util.Map;

import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import arjunasdk.ddauto.interfaces.DataSource;
import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import unitee.annotations.DataGenerator;

public class DataGeneratorMap {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
		Map<String,Class<? extends DataSource>> dataSources = new HashMap<String, Class<? extends DataSource>>();
	//HashMap<String,String> dataGenClassNames = new HashMap<String,String>();
	//HashMap<Class<? extends DataSource>,String> dataGenClassToNameMapper = new HashMap<Class<? extends DataSource>,String>();
	
	@SuppressWarnings("unchecked")
	public void process(Class<?> klassRaw) throws Exception{
		Class<? extends DataSource> klass = null;
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug("Evaluating: " + klassRaw.getName());
			logger.debug("Does it implement DataSource interface?");
		}
		if (DataSource.class.isAssignableFrom(klassRaw)){
			if (ArjunaInternal.displayDataMethodProcessingInfo){
				logger.debug("Yes");
			}
			klass = (Class<? extends DataSource>) klassRaw ;
		} else {
			if (ArjunaInternal.displayDataMethodProcessingInfo){
				logger.debug("No!");
				logger.debug("Would not be considered as a data generator.");
			}
			return;
		}
		String dataGenClassName = klass.getName().toUpperCase();
		String dataGenName = null;
		String origDGName = null;
		if (klass.isAnnotationPresent(DataGenerator.class)){
			Annotation annotation = klass.getAnnotation(DataGenerator.class);
			DataGenerator dataGenAnn = (DataGenerator) annotation;
			if (dataGenAnn.name().equals("NOT_SET")){
				if (dataGenAnn.value().equals("NOT_SET")){
					origDGName = dataGenClassName;
				} else {
					origDGName = dataGenAnn.value();
				}
			} else {
				origDGName = dataGenAnn.name();
			}
		} else {
			origDGName = dataGenClassName;
		}
		
		dataGenName = origDGName.toUpperCase();
		
		Constructor<?>[] constructors = klass.getConstructors();
		for (Constructor<?> constructor: constructors){
			if (constructor.getParameterTypes().length > 0){
				Console.displayError("!!!FATAL Error!!!");
				Console.displayError(String.format("Critical Error. Non-default constructor found for data generator class: %s",klass.getName()));
				Console.displayError(String.format("Data Generator constructor can not take any argument."));
				Console.displayError(String.format("Change constructor to:"));
				Console.displayError(String.format("public %s()", klass.getSimpleName()));
				Console.displayError("Exiting...");
				System.exit(1);				
			}
		}
		
		if (this.dataSources.containsKey(dataGenClassName)){
			Console.displayError("!!!FATAL Error!!!");
			Console.displayError(String.format("You need to change name of Data Generator class [%s].", klass.getName()));
			Console.displayError(String.format("Another data generator exists in your project, either with same name or @DataGenerator label."));
			Console.displayError("Exiting...");
			System.exit(1);
		}
		
		if (this.dataSources.containsKey(dataGenName)){
			Console.displayError("!!!FATAL Error!!!");
			Console.displayError(String.format("You need to change @DataGenerator label [%s] of data generator class [%s].", origDGName, klass.getName()));
			Console.displayError(String.format("Another data generator exists in your project, either with same name or @DataGenerator label."));
			Console.displayError("Exiting...");
			System.exit(1);
		}
		
		dataSources.put(dataGenName, klass);
		dataSources.put(dataGenClassName, klass);
	}
	
	public DataSource getDataSource(String dataGenName) throws Exception{
		if (dataSources.containsKey(dataGenName.toUpperCase())){
			return dataSources.get(dataGenName.toUpperCase()).newInstance();
		} else {
			throw new Exception(String.format("No data generator class with name %s found.", dataGenName));
		}
	}
}
