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
package com.autocognite;

import java.time.LocalDate;

import arjunasdk.console.Console;
import arjunasdk.sysauto.batteries.SystemBatteries;
import pvt.arjunapro.ArjunaInternal;
import pvt.arjunapro.ArjunaTestEngine;
import pvt.unitee.cli.UniteeCliConfigurator;
import pvt.unitee.lib.engine.TestEngine;

public class Arjuna {

	public static void main(String[] args) throws Exception {
		Console.init();
		ArjunaInternal.setCliConfigurator(new UniteeCliConfigurator());
		ArjunaInternal.setEdition("AutoCognite Arjuna");
		ArjunaInternal.shouldInitUiAutomator(true);
		ArjunaInternal.init(args);
		TestEngine tee = createEngine(args);
		ArjunaInternal.execute(tee);
	}
	
	private static TestEngine createEngine(String[] args){
		TestEngine tee =  null;
		try{
			tee = new ArjunaTestEngine(args);
		} catch (java.lang.reflect.InvocationTargetException g) {
			if (Throwable.class.isAssignableFrom(g.getTargetException().getClass())){
				Console.displayExceptionBlock(g.getTargetException());
				SystemBatteries.exit();
			}
		} catch (Throwable e){
			Console.displayExceptionBlock(e);
			SystemBatteries.exit();
			System.exit(1);
		}		
		return tee;
	}
	
}
