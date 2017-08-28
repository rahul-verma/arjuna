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
package pvt.unitee.testobject.lib.java.loader;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import arjunasdk.sysauto.batteries.DataBatteries;
import pvt.batteries.config.Batteries;
import pvt.batteries.ddt.datarecord.BaseDataRecordContainer;
import pvt.unitee.arjuna.ArjunaInternal;
import unitee.annotations.DataMethod;

public abstract class DefaultDataMethodsHandler implements DataMethodsHandler {
	private static Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private Map<String,Method> methods = new HashMap<String,Method>();
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
			String originalDgName = null;
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
							originalDgName = m.getName();
							
						} else {
							originalDgName = dataGenAnnotation.value();
						}
					} else {
						originalDgName = dataGenAnnotation.name();
					}		
//					logger.debug("DG Method Label (Case insensitive): " + dgName);
				} else{
						continue;
					}
			} else {
				continue;
			}
			
			dgName = originalDgName.toUpperCase();
			
			if (!Modifier.isStatic(m.getModifiers())){
				Console.displayError("!!!FATAL Error!!!");
				Console.displayError("Data methods need to be static methods.");
				Console.displayError(String.format("Change Data method [%s] to static in %s class.", m.getName(), this.getContainerName()));
				Console.displayError("Exiting...");
				System.exit(1);
				throw new Exception();
			}
			
			Class<?>[] paramTypes = m.getParameterTypes();
			if (paramTypes.length > 0){
				List<String> tStrings =  new ArrayList<String>();
				for (Class<?> t: paramTypes){
					tStrings.add(t.getSimpleName());
				}

				String argString = null;
				if (tStrings.size() == 0){
					argString = "";
				} else {
					argString = DataBatteries.join(tStrings, ",");
				}

				Console.displayError("!!!FATAL Error!!!");
				Console.displayError(String.format("There is a critical issue with your data method [%s] in %s class", m.getName(), this.getContainerName()));
				Console.displayError(String.format("Current (wrong) data method signature is: static %s(%s)", m.getName(), argString));
				Console.displayError("Data methods can not take any argument. Remove argument(s), change the method implementation and run again.");
				Console.displayError("Exiting...");
				System.exit(1);	

			}
			
			if (this.methods.containsKey(methodName)){
				Console.displayError("!!!FATAL Error!!!");
				Console.displayError(String.format("You need to change name of data method [%s] in %s class.", m.getName(), this.getContainerName()));
				Console.displayError(String.format("Another data method exists in %s class either with same name or @DataMethod label.", this.getContainerName()));
				Console.displayError("Exiting...");
				System.exit(1);
			}
			
			if (this.methods.containsKey(dgName)){
				Console.displayError("!!!FATAL Error!!!");
				Console.displayError(String.format("You need to change @DataMethod label [%s] of data method [%s] in %s class.", originalDgName, m.getName(), this.getContainerName()));
				Console.displayError(String.format("Another data method exists in %s class either with same name or @DataMethod label.", this.getContainerName()));
				Console.displayError("Exiting...");
				System.exit(1);
			}

				this.methods.put(dgName, m);
				this.methods.put(methodName, m);
			}

		}

		@Override
		public Method getMethod(String dgName) throws Exception{
			if (methods.containsKey(dgName.toUpperCase())){
				return (Method) methods.get(dgName.toUpperCase());
			} else {
				Console.displayError("!!!FATAL Error!!!");
				Console.displayError(String.format("No data method with name [%s] found in %s class.", dgName, this.getContainerName()));
				Console.displayError("Exiting...");
				System.exit(1);
				throw new Exception();
			}
		}
	}
