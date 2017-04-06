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
package pvt.batteries.discoverer;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import org.apache.commons.io.DirectoryWalker;
import org.apache.commons.io.FilenameUtils;
import org.apache.log4j.Logger;

import com.arjunapro.sysauto.batteries.DataBatteries;
import com.arjunapro.sysauto.batteries.FileSystemBatteries;
import com.arjunapro.sysauto.batteries.SystemBatteries;

import pvt.batteries.config.Batteries;
import pvt.batteries.discovery.JarClassDiscoverer;

public class FileDiscoverer extends DirectoryWalker {
	public Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	FileAggregator aggregator = null;
	String rootDir = null;
	String currentDir = null;
	String currentAbsDir = null;

	public FileDiscoverer(FileAggregator aggregator, String rootDir) {
		super();
		this.aggregator = aggregator;
		if (rootDir.endsWith("\\") || rootDir.endsWith("//")) {
			this.rootDir = rootDir.substring(0, rootDir.length() - 1);
		} else {
			this.rootDir = rootDir;
		}
	}

	public void discover() throws IOException {
		List results = new ArrayList();
		walk(new File(this.rootDir), results);
		this.aggregator.freeze();
	}

	protected boolean handleDirectory(File directory, int depth, Collection results) {
		// currentAbsDir = directory.getPath();
		// int factor = 1;
		// if (currentAbsDir.equals(this.rootDir)) {
		// factor = 0;
		// }
		// this.currentDir =
		// currentAbsDir.substring(currentAbsDir.indexOf(this.rootDir) +
		// this.rootDir.length() + factor);
		return true;
	}

	protected void handleFile(File file, int depth, Collection results) throws IOException {
		String fullPath = FileSystemBatteries.getCanonicalPath(file.getAbsolutePath());
		// RunConfig.getCentralLogger().debug(fullPath);
		String parentDir = fullPath.substring(0, fullPath.indexOf(file.getName()) - 1);
		// RunConfig.getCentralLogger().debug(parentDir);
		String pkgParentDir = null;
		if (parentDir.equals(this.rootDir)) {
			pkgParentDir = "";
		} else {
			pkgParentDir = parentDir.substring(parentDir.indexOf(this.rootDir) + this.rootDir.length() + 1);
		}
		String fileExt = FilenameUtils.getExtension(file.getName());
		if (fileExt.toLowerCase().equals("jar")) {
			JarClassDiscoverer jcd = new JarClassDiscoverer(aggregator, file.getPath(), pkgParentDir, parentDir);
			try {
				jcd.discover();
			} catch (Exception e) {
				e.printStackTrace();
			}
			return;
		}

		DiscoveredFile df = new DiscoveredFile();
		df.setAttribute(DiscoveredFileAttribute.NAME, FilenameUtils.getBaseName(file.getName()));
		df.setAttribute(DiscoveredFileAttribute.EXTENSION, fileExt);
		df.setAttribute(DiscoveredFileAttribute.FULL_NAME, file.getName());
		df.setAttribute(DiscoveredFileAttribute.PACKAGE_DOT_NOTATION,
				pkgParentDir.replace(SystemBatteries.getPathSeparator(), "."));
		df.setAttribute(DiscoveredFileAttribute.DIRECTORY_RELATIVE_PATH, pkgParentDir);
		df.setAttribute(DiscoveredFileAttribute.DIRECTORY_ABSOLUTE_PATH, parentDir);
		String replaced = df.getAttribute(DiscoveredFileAttribute.DIRECTORY_RELATIVE_PATH).replace("/", "|");
		replaced = replaced.replace("\\", "|");
		df.setAttribute(DiscoveredFileAttribute.COMMA_SEPATARED_RELATIVE_PATH,
				DataBatteries.join(replaced.split("|"), ","));
		df.setAttribute(DiscoveredFileAttribute.CONTAINER, "NA");
		df.setAttribute(DiscoveredFileAttribute.CONTAINER_TYPE, "NA");
		aggregator.addFile(df);

	}
}
