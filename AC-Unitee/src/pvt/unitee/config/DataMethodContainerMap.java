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
import java.lang.reflect.Method;
import java.util.HashMap;

import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import arjunasdk.sysauto.batteries.DataBatteries;
import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import pvt.unitee.testobject.lib.loader.DataMethodsHandler;
import pvt.unitee.testobject.lib.loader.NonTestDataMethodsHandler;
import unitee.annotations.DataMethodContainer;

public class DataMethodContainerMap {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	HashMap<String,DataMethodsHandler> wrappers = new HashMap<String, DataMethodsHandler>();
	HashMap<String,Class<?>> containerMapper = new HashMap<String,Class<?>>();
	HashMap<String,String> containerNameMapper = new HashMap<String,String>();
	
	public void process(Class<?> klass) throws Exception{
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug("Now processing for data methods: " + klass);
		}
		Annotation annotation = klass.getAnnotation(DataMethodContainer.class);
		DataMethodContainer dataContainer = (DataMethodContainer) annotation;
		String containerClassName = klass.getName().toUpperCase();
		String origContainerName = null;
		String containerName = null;
		if (dataContainer.name().equals("NOT_SET")){
			if (dataContainer.value().equals("NOT_SET")){
				origContainerName = containerClassName;
			} else {
				origContainerName = dataContainer.value();
			}
		} else {
			origContainerName = dataContainer.name();
		}
		
		containerName = origContainerName.toUpperCase();
		
		if (this.containerMapper.containsKey(containerClassName)){
			Console.displayError("!!!FATAL Error!!!");
			Console.displayError(String.format("You need to change name of Data Method Container class [%s].", klass.getName()));
			Console.displayError(String.format("Another data method container exists in your project, either with same name or @DataMethodContainer label."));
			Console.displayError("Exiting...");
			System.exit(1);
		}
		
		if (this.containerMapper.containsKey(containerName)){
			Console.displayError("!!!FATAL Error!!!");
			Console.displayError(String.format("You need to change @DataMethodContainer label [%s] of data method container class [%s].", origContainerName, klass.getName()));
			Console.displayError(String.format("Another data method container exists in your project, either with same name or @DataMethodContainer label."));
			Console.displayError("Exiting...");
			System.exit(1);
		}
		
		containerMapper.put(containerClassName, klass);
		containerMapper.put(containerName, klass);
		
		containerNameMapper.put(containerClassName, containerName);
		containerNameMapper.put(containerName, containerName);
		
		DataMethodsHandler handler = new NonTestDataMethodsHandler(klass);
		handler.process();
		this.wrappers.put(containerName, handler);
	}
	
	public Method getMethod(String containerName, String dgName) throws Exception{
		if (containerNameMapper.containsKey(containerName.toUpperCase())){
			String cName = containerNameMapper.get(containerName.toUpperCase());
			return (Method) wrappers.get(cName).getMethod(dgName);
		} else {
			throw new Exception(String.format("No data method container class with name %s found.", containerName));
		}
	}
	
	public Method getMethod(Class<?> containerClass, String methodName) throws Exception{
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug("Retrieving Data Method for class: "  + containerClass.getName());
		}
		if (!containerClass.isAnnotationPresent(DataMethodContainer.class)){
			logger.debug("@DataMethodContainer Annotated Container");
			return NonTestDataMethodsHandler.getStaticMethodForClass(containerClass, methodName);
		}
		
		String className = containerClass.getName();
		if (containerNameMapper.containsKey(className.toUpperCase())){
			String cName = containerNameMapper.get(className.toUpperCase());
			return (Method) wrappers.get(cName).getMethod(methodName);
		} else {
			throw new Exception(String.format("No data generator class found for: %s", className));
		}
	}
}
