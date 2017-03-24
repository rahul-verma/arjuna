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
package pvt.uiautomator.lib;

import com.arjunapro.sysauto.batteries.FileSystemBatteries;
import com.arjunapro.testauto.config.RunConfig;

import pvt.arjunapro.uiauto.interfaces.PageMapper;
import pvt.batteries.config.Batteries;
import pvt.batteries.exceptions.Problem;
import pvt.uiautomator.UiAutomator;

public abstract class BasePageMapper implements PageMapper{
	private String mapName = null;
	
	public abstract String getName();
	
	protected Object throwGenericUiMapperException(
			String action,
			String code,
			String message
			) throws Exception{
				throw new Problem(
						Batteries.getConfiguredName("COMPONENT_NAMES", "UI_AUTOMATOR"),
				this.getName(),
				action,
				code,
				message
				);		
	}
	
	public Object throwNotAFileException(String methodName, String filePath) throws Exception{
		return throwGenericUiMapperException(
				methodName,
				UiAutomator.problem.MAPFILE_NOTAFILE,
				Batteries.getProblemText(
						UiAutomator.problem.MAPFILE_NOTAFILE,
						FileSystemBatteries.getCanonicalPath(filePath)
				)
		);
	}
	
	public Object throwFileNotFoundException(String methodName, String filePath) throws Exception{
		return throwGenericUiMapperException(
				methodName,
				UiAutomator.problem.MAPFILE_NOT_FOUND,
				Batteries.getProblemText(
						UiAutomator.problem.MAPFILE_NOT_FOUND,
						FileSystemBatteries.getCanonicalPath(filePath)
				)
		);
	}
	
	public Object throwRelativePathException(String methodName, String filePath) throws Exception{
		return throwGenericUiMapperException(
				methodName,
				UiAutomator.problem.MAPFILE_RELATIVE_PATH,
				Batteries.getProblemText(
						UiAutomator.problem.MAPFILE_RELATIVE_PATH,
						filePath
				)
		);
	}
}
