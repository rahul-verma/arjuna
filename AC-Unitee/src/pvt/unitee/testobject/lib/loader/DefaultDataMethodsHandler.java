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
package pvt.unitee.testobject.lib.loader;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.HashMap;

import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import pvt.batteries.config.Batteries;
import pvt.batteries.ddt.datarecord.BaseDataRecordContainer;
import pvt.unitee.arjuna.ArjunaInternal;
import unitee.annotations.DataMethod;

public abstract class DefaultDataMethodsHandler implements DataMethodsHandler {
	private static Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private HashMap<String,Method> methods = new HashMap<String,Method>();
	public static Object[][] sampleArr = {};

	protected abstract boolean shouldInclude(Method m);

	protected abstract Method[] getMethods();

	protected abstract String getContainerName();
	
	public static boolean hasAllowedReturnType(Method m){
		return (m.getReturnType().isAssignableFrom(sampleArr.getClass())) 
				|| (m.getReturnType().isAssignableFrom(BaseDataRecordContainer.class));
	}

	public void process() throws Exception{
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug("Would now load any data generator methods present in " + this.getContainerName());
		}
		Annotation annotation = null;
		for (Method m: getMethods()){
			if (ArjunaInternal.displayDataMethodProcessingInfo){
				logger.debug("Check for being a Data method: " + m.getName());
			}
			String methodName = m.getName().toUpperCase();
			String dgName = null;
			if (shouldInclude(m)){
				if (ArjunaInternal.displayDataMethodProcessingInfo){
					logger.debug("Passed method type check.");
				}
				if (m.isAnnotationPresent(DataMethod.class)){
					if (ArjunaInternal.displayDataMethodProcessingInfo){
						logger.debug("Is annotated as Data Method.");
					}
					if (!hasAllowedReturnType(m)){
						continue;
					}
					if (ArjunaInternal.displayDataMethodProcessingInfo){
						logger.debug("Method has the required annotation and meets the return type criterion. Now loading...");
						logger.debug(String.format("Found Data generator method %s in %s", m.getName(), this.getContainerName()));
					}
					annotation = m.getAnnotation(DataMethod.class);
					DataMethod dataGenAnnotation = (DataMethod) annotation;
					if (dataGenAnnotation.name().equals("NOT_SET")){
						if (dataGenAnnotation.value().equals("NOT_SET")){
							dgName = m.getName().toUpperCase();
						} else {
							dgName = dataGenAnnotation.value().toUpperCase();
						}
					} else {
						dgName = dataGenAnnotation.name().toUpperCase();
					}		
//					logger.debug("DG Method Label (Case insensitive): " + dgName);
				} else{
						continue;
					}
			} else {
				continue;
			}
				if (this.methods.containsKey(dgName)){
					Console.displayError("!!!FATAL Error!!!");
					Console.displayError(String.format("Duplicate data method name/label [%s] found in %s class. Check @DataMethod annotation as well names of the data methods in code.", dgName, this.getContainerName()));
					Console.displayError("Exiting...");
					System.exit(1);
				}

				this.methods.put(dgName, m);
			}

		}

		@Override
		public Method getMethod(String dgName) throws Exception{
			if (methods.containsKey(dgName.toUpperCase())){
				return (Method) methods.get(dgName.toUpperCase());
			} else {
				throw new Exception(String.format("No data method with name %s found in %s class.", dgName, this.getContainerName()));
			}
		}
	}
