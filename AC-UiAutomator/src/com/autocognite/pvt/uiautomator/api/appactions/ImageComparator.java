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
package com.autocognite.pvt.uiautomator.api.appactions;

import java.io.File;

public interface ImageComparator {
	boolean areImagesSimilar(File leftImage, File rightImage, Double minScore) throws Exception;
	boolean areImagesSimilar(String leftImagePath, File rightImage)  throws Exception;
	boolean areImagesSimilar(String leftImagePath, File rightImage, Double minScore)  throws Exception;
	boolean areImagesSimilar(String leftImagePath, String rightImagePath)  throws Exception;
	boolean areImagesSimilar(File leftImage, File rightImage)  throws Exception;
}
