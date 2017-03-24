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
package com.arjunapro.sysauto.batteries;

import java.io.File;
import java.net.URL;
import java.nio.file.Paths;
import java.util.ArrayList;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;

public class FileSystemBatteries {

	public static String getJarFilePathForObject(Object obj) {
		URL location = obj.getClass().getProtectionDomain().getCodeSource().getLocation();
		return location.getFile();
	}

	// The toURL() call is deprecated. However, not using this construct
	// converts spaces in paths to %20 in windows OS, which itself
	// is logged as a bug in Java.
	@SuppressWarnings("deprecation")
	public static String getCanonicalPath(String filePath) {
		File file = new File(filePath);
		try {
			file = Paths.get(file.toURL().toURI()).toFile();
		} catch (Exception e) {
			//
		}
		try {
			return file.getCanonicalPath();
		} catch (Exception e) {
			try {
				return new File(filePath).getCanonicalPath();
			} catch (Exception f) {
				return filePath;
			}
		}
	}

	public static String createFilePath(String parentPath, ArrayList<String> childParts, String fileName,
			String extension) {
		ArrayList<String> fullPath = new ArrayList<String>();
		fullPath.add(parentPath);
		fullPath.add(DataBatteries.join(childParts, "\\"));
		String finalPath = DataBatteries.join(fullPath, "\\");
		File resultFile = new File(finalPath);
		resultFile.mkdirs();
		return finalPath + "\\" + fileName + extension;
	}

	public static String getAbsolutePathFromJar(String mainPath, String relativePath) throws Exception {
		File a = new File(mainPath);
		File b = new File(a, relativePath);
		String absolute = b.getCanonicalPath(); // may throw IOException
		return absolute;
	}

	public static boolean isFile(File file) throws Exception {
		if (file.exists()) {
			if (file.isFile()) {
				return true;
			}
		}
		return false;
	}

	public static boolean isDir(File dir) throws Exception {
		if (dir.exists()) {
			if (dir.isDirectory()) {
				return true;
			}
		}
		return false;
	}

	public static boolean isFile(String filePath) throws Exception {
		return isFile(new File(filePath));
	}

	public static boolean isDir(String dirPath) throws Exception {
		return isDir(new File(dirPath));
	}

	public static boolean isAbsolutePath(String path) throws Exception {
		return (new File(path)).isAbsolute();
	}

	private static void validateFile(File file) throws Exception {
		if (!file.exists()) {
			throw new Exception("File does not exist.");
		} else if (!file.isFile()) {
			throw new Exception("Not a file.");
		}
	}

	private static void validateDir(File dir) throws Exception {
		if (!dir.exists()) {
			throw new Exception("Directory does not exist.");
		} else if (!dir.isDirectory()) {
			throw new Exception("Not a directory.");
		}
	}

	private static void validateFile(String filePath) throws Exception {
		validateFile(new File(filePath));
	}

	private static void validateDir(String dirPath) throws Exception {
		validateDir(new File(dirPath));
	}

	public static long getFileModifiedTimeStamp(String filePath) throws Exception {
		File file = new File(filePath);
		validateFile(file);
		return file.lastModified();
	}

	public static File getLatestFilefromDir(String dirPath) {
		File dir = new File(dirPath);
		File[] files = dir.listFiles();

		if (files == null || files.length == 0) {
			return null;
		}

		File lastModifiedFile = files[0];
		for (int i = 1; i < files.length; i++) {
			if (lastModifiedFile.lastModified() < files[i].lastModified()) {
				lastModifiedFile = files[i];
			}
		}
		return lastModifiedFile;
	}

	public static void deleteDirectory(String dirPath) throws Exception {
		File dir = new File(dirPath);
		validateDir(dir);
		FileUtils.deleteDirectory(dir);
	}

	public static void copyFile(File srcFile, File destFile) throws Exception {
		validateFile(srcFile);
		validateDir(destFile.getParent());
		FileUtils.copyFile(srcFile, destFile);
	}

	public static void copyFile(String srcFilePath, String destFilePath) throws Exception {
		copyFile(new File(srcFilePath), new File(destFilePath));
	}

	public static void copyFileToDirectory(File srcFile, File destDir) throws Exception {
		validateFile(srcFile);
		validateDir(destDir);
		FileUtils.copyFileToDirectory(srcFile, destDir);
	}

	public static void copyFileToDirectory(String srcFilePath, String destDirPath) throws Exception {
		copyFileToDirectory(new File(srcFilePath), new File(destDirPath));
	}

	public static File moveFiletoDir(File srcFile, String destDirPath) throws Exception {
		FileUtils.moveFileToDirectory(srcFile, new File(destDirPath), false);
		return new File(destDirPath + "/" + srcFile.getName());
	}

	public static File moveFileToDir(String srcFilePath, String destDirPath) throws Exception {
		File srcFile = new File(srcFilePath);
		return moveFiletoDir(srcFile, destDirPath);

	}

	public static File createEmptyFile(String path) throws Exception {
		File f = new File(path);
		FileUtils.touch(f);
		return f;
	}

	public static String getExtension(String fileName) {
		return FilenameUtils.getExtension(fileName);
	}
}
