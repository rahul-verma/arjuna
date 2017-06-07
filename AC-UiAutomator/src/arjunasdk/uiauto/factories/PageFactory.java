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
package arjunasdk.uiauto.factories;

import arjunasdk.uiauto.interfaces.Page;
import arjunasdk.uiauto.interfaces.PageMapper;
import arjunasdk.uiauto.interfaces.UiDriver;
import arjunasdk.uiauto.pageobject.BasePage;
import pvt.arjunapro.uiauto.factories.PageMapperFactory;

public class PageFactory {

//	public static Page getPage(String label, UiDriver uiDriver, PageMapper mapper) throws Exception{
//		Page page = new BasePage(label, uiDriver);
//		page.populate(mapper);
//		return page;
//	}

	private static Page getPage(UiDriver uiDriver, PageMapper mapper) throws Exception{
		Page page = new BasePage(uiDriver);
		page.populate(mapper);
		return page;
	}
	
//	public static App getSimpleApp(String name, UiDriver uiDriver, String appMapsRootDir) throws Exception{
//		App app = new BaseApp(name);
//		String consideredPath = appMapsRootDir;
//		if (!FileSystemBatteries.isDir(consideredPath)){
//			consideredPath = FileSystemBatteries.getCanonicalPath(Batteries.value(UiAutomatorPropertyType.DIRECTORY_UI_MAPS).asString() + "/" + consideredPath);
//			if (!FileSystemBatteries.isDir(consideredPath)){
//				throw new Problem(
//						"UI Automator", 
//						"Page Mapper", 
//						"getFileMapper", 
//						UiAutomator.problem.APP_MAP_DIR_NOT_A_DIR, 
//						Batteries.getProblemText(UiAutomator.problem.APP_MAP_DIR_NOT_A_DIR, consideredPath)
//					);				
//			} 
//		}
//		File d = new File(consideredPath);
//		for (File path: d.listFiles()){
//			app.registerPage(FilenameUtils.getBaseName(path.getAbsolutePath()), uiDriver,
//					path.getAbsolutePath());
//		}
//		return app;
//	}

	public static Page getPage(UiDriver uiDriver, String mapPath) throws Exception {
		return getPage(uiDriver, PageMapperFactory.getFileMapper(mapPath));
	}
}
