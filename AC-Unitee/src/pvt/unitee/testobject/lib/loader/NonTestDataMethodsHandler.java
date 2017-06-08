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
import java.lang.reflect.Modifier;

import org.apache.log4j.Logger;

import pvt.batteries.config.Batteries;
import pvt.unitee.arjuna.ArjunaInternal;
import unitee.annotations.DataMethod;

public class NonTestDataMethodsHandler extends DefaultDataMethodsHandler {
	private static Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	Class<?> klass = null;

	public NonTestDataMethodsHandler(Class<?> klass) throws Exception {
		this.klass = klass;
	}

	public static Method getStaticMethodForClass(Class<?> klass, String targetDgName) throws Exception{
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug("Get static data method for any non-data method container class " + klass.getName());
		}
		Annotation annotation = null;
		Method method = null;
		boolean found = false;
		String dgName = null;
		String mName = null;
		for (Method m: klass.getDeclaredMethods()){
			if (ArjunaInternal.displayDataMethodProcessingInfo){
				logger.debug("Check for being a Data generator method: " + m.getName());
			}
			if ((Modifier.isStatic(m.getModifiers()) && Modifier.isPublic(m.getModifiers()))){
				if (ArjunaInternal.displayDataMethodProcessingInfo){
					logger.debug("Passed Filter");
				}
				if (m.isAnnotationPresent(DataMethod.class)){
					if (ArjunaInternal.displayDataMethodProcessingInfo){
						logger.debug("Is annotated as Data Method.");
					}
					if (!DefaultDataMethodsHandler.hasAllowedReturnType(m)){
						continue;
					}
					if (ArjunaInternal.displayDataMethodProcessingInfo){
						logger.debug("Method has the required annotation and meets the return type criterion. Now loading...");
						logger.debug("Found Data generator method: " + m.getName());
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
					if (ArjunaInternal.displayDataMethodProcessingInfo){
						logger.debug("DG Method Label (Case insensitive): " + dgName);
					}
					if (dgName.toUpperCase().equals(targetDgName.toUpperCase())){
						found = true;
						mName = m.getName();
						break;
					}
				} else {
					continue;
				}
			}
		}

		if (found){
			return klass.getMethod(mName);
		} else {
			throw new Exception(String.format("No data method with name %s found in class: %s", targetDgName, klass.getName()));
		}				
		}

		protected boolean shouldInclude(Method m){
			return (Modifier.isStatic(m.getModifiers()) && Modifier.isPublic(m.getModifiers()));
		}

		@Override
		protected Method[] getMethods() {
			return klass.getDeclaredMethods();
		}

		@Override
		protected String getContainerName() {
			return this.klass.getName();
		}
	}
