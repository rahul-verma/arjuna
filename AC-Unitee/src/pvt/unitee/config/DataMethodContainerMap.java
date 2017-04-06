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
import java.lang.reflect.Method;
import java.util.HashMap;

import org.apache.log4j.Logger;

import com.arjunapro.ddt.annotations.DataMethodContainer;
import com.arjunapro.sysauto.batteries.DataBatteries;

import pvt.arjunapro.ArjunaInternal;
import pvt.batteries.config.Batteries;
import pvt.unitee.testobject.lib.loader.DataMethodsHandler;
import pvt.unitee.testobject.lib.loader.NonTestDataMethodsHandler;

public class DataMethodContainerMap {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	HashMap<String,DataMethodsHandler> wrappers = new HashMap<String, DataMethodsHandler>();
	HashMap<String,String> containerClassNames = new HashMap<String,String>();
	HashMap<Class<?>,String> containerClassToNameMapper = new HashMap<Class<?>,String>();
	// In obfuscated jar somehow class to class look up not working. So, this data structure.
	HashMap<String,Class<?>> containerClassNameToClassMapper = new HashMap<String,Class<?>>();
	
	public void process(Class<?> klass) throws Exception{
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug("Now processing for data methods: " + klass);
		}
		Annotation annotation = klass.getAnnotation(DataMethodContainer.class);
		DataMethodContainer dataContainer = (DataMethodContainer) annotation;
		String containerClassName = klass.getSimpleName().toUpperCase();
		String containerName = null;
		if (dataContainer.name().equals("NOT_SET")){
			if (dataContainer.value().equals("NOT_SET")){
				containerName = containerClassName;
			} else {
				containerName = dataContainer.value().toUpperCase();
			}
		} else {
			containerName = dataContainer.name().toUpperCase();
		}
		
		this.containerClassNames.put(containerClassName, containerName);
		this.containerClassToNameMapper.put(klass, containerName);
		this.containerClassNameToClassMapper.put(klass.getName(), klass);
		DataMethodsHandler handler = new NonTestDataMethodsHandler(klass);
		handler.process();
		this.wrappers.put(containerName, handler);
	}
	
	public Method getMethod(String containerName, String dgName) throws Exception{
		if (wrappers.containsKey(containerName.toUpperCase())){
			return (Method) wrappers.get(containerName.toUpperCase()).getMethod(dgName);
		} else if (containerClassNames.containsKey(containerName.toUpperCase())){
			return (Method) wrappers.get(containerClassNames.get(containerName.toUpperCase())).getMethod(dgName);
		} else {
			throw new Exception(String.format("No data generator class with name %s found.", containerName));
		}
	}
	
	public Method getMethod(Class<?> containerClass, String dgName) throws Exception{
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug("Retrieving Data Method for class: "  + containerClass.getName());
		}
		if (!containerClass.isAnnotationPresent(DataMethodContainer.class)){
			logger.debug("@DataMethodContainer Annotated Container");
			return NonTestDataMethodsHandler.getStaticMethodForClass(containerClass, dgName);
		}
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug(DataBatteries.flatten(this.containerClassNameToClassMapper.keySet()));
		}
		
		if (containerClassNameToClassMapper.containsKey(containerClass.getName())){
			Class<?> k = containerClassNameToClassMapper.get(containerClass.getName());
			return (Method) wrappers.get(containerClassToNameMapper.get(k)).getMethod(dgName);
		} else {
			throw new Exception(String.format("No data generator class found for: %s", containerClass.getName()));
		}
	}
}
