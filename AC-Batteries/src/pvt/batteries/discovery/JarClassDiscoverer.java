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
package pvt.batteries.discovery;

import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

import org.apache.commons.io.FilenameUtils;
import org.apache.log4j.Logger;

import com.arjunapro.sysauto.batteries.DataBatteries;

import pvt.batteries.config.Batteries;
import pvt.batteries.discoverer.DiscoveredFile;
import pvt.batteries.discoverer.DiscoveredFileAttribute;
import pvt.batteries.discoverer.FileAggregator;

public class JarClassDiscoverer {
	public Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	FileAggregator aggregator = null;
	String jarFilePath = null;
	String parentDir = null;
	String parentAbsDir = null;

	public JarClassDiscoverer(FileAggregator aggregator, String jarFilePath, String parentDir, String parentAbsDir) {
		this.aggregator = aggregator;
		this.jarFilePath = jarFilePath;
		this.parentDir = parentDir;
		this.parentAbsDir = parentAbsDir;
	}

	public void discover() throws Exception {
		if (Batteries.logFileDiscoveryInfo) {
			logger.debug("Start- Find classes in JAR");
		}
		JarFile jarFile = new JarFile(jarFilePath);

		Enumeration<JarEntry> e = jarFile.entries();

		URL[] urls = { new URL("jar:file:" + jarFilePath + "!/") };
		URLClassLoader cl = URLClassLoader.newInstance(urls);
		while (e.hasMoreElements()) {
			JarEntry je = (JarEntry) e.nextElement();
			if (Batteries.logFileDiscoveryInfo) {
				logger.debug(je.getName());
			}
			if (je.isDirectory() || !je.getName().endsWith(".class")) {
				continue;
			}
			// -6 because of .class
			String className = je.getName().substring(0, je.getName().length() - 6);
			// logger.debug(className);
			className = className.replace('/', '.').replace("\\", ".");
			if (Batteries.logFileDiscoveryInfo) {
				logger.debug(className);
			}
			Class c = null;
			try {
				c = cl.loadClass(className);
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			if (c != null) {
				if (Batteries.logFileDiscoveryInfo) {
					logger.debug("Adding class to aggregator: " + className);
				}

				DiscoveredFile df = new DiscoveredFile();
				String[] classBaseNameParts = className.split("\\.");
				ArrayList<String> parts = DataBatteries.arrayToArrayList(classBaseNameParts);
				String classBaseName = classBaseNameParts[classBaseNameParts.length - 1];
				df.setAttribute(DiscoveredFileAttribute.NAME, classBaseName);
				df.setAttribute(DiscoveredFileAttribute.EXTENSION, "class");
				if (classBaseNameParts.length > 1) {
					df.setAttribute(DiscoveredFileAttribute.PACKAGE_DOT_NOTATION,
							DataBatteries.join(parts.subList(0, parts.size() - 1), "."));
					df.setAttribute(DiscoveredFileAttribute.FULL_NAME,
							df.getAttribute(DiscoveredFileAttribute.PACKAGE_DOT_NOTATION) + "." + classBaseName + "."
									+ "class");
				} else {
					df.setAttribute(DiscoveredFileAttribute.PACKAGE_DOT_NOTATION, "");
					df.setAttribute(DiscoveredFileAttribute.FULL_NAME, classBaseName + "." + "class");
				}
				df.setAttribute(DiscoveredFileAttribute.DIRECTORY_RELATIVE_PATH, this.parentDir);
				df.setAttribute(DiscoveredFileAttribute.DIRECTORY_ABSOLUTE_PATH, this.parentAbsDir);
				String replaced = df.getAttribute(DiscoveredFileAttribute.DIRECTORY_RELATIVE_PATH).replace("/", "|");
				replaced = replaced.replace("\\", "|");
				df.setAttribute(DiscoveredFileAttribute.COMMA_SEPATARED_RELATIVE_PATH,
						DataBatteries.join(replaced.split("|"), ","));
				df.setAttribute(DiscoveredFileAttribute.CONTAINER, FilenameUtils.getName(jarFilePath));
				df.setAttribute(DiscoveredFileAttribute.CONTAINER_TYPE, "JAR");
				aggregator.addFile(df);
			}

		}
		jarFile.close();
	}
}
