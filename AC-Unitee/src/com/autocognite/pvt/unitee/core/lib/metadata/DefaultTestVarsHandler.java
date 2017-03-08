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
package com.autocognite.pvt.unitee.core.lib.metadata;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.config.RunConfig;
import com.autocognite.arjuna.enums.TestObjectType;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.unitee.core.lib.testvars.DefaultTestVariables;
import com.autocognite.pvt.unitee.core.lib.testvars.InternalTestVariables;
import com.autocognite.pvt.unitee.testobject.lib.interfaces.TestObject;

public class DefaultTestVarsHandler implements TestVarsHandler{
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
	private TestObject testObject = null;
	private TestObject parentTestObject = null;
	private InternalTestVariables testVars =  new DefaultTestVariables();
	
	public InternalTestVariables getTestVariables(){
		return this.testVars;
	}
	
	protected TestObject getTestObject(){
		return this.testObject;
	}
	
	protected TestObject getParentTestObject(){
		return this.parentTestObject;
	}
	
	public DefaultTestVarsHandler(TestObject testObject) throws Exception{
		this.testObject = testObject;
	}
	
	public DefaultTestVarsHandler(TestObject testObject, TestObject parentObject) throws Exception{
		this.testObject = testObject;
		this.parentTestObject = parentObject;
	}
	
	protected void populateObjectIdentification() throws Exception{
		this.testVars.rawObjectProps().setObjectId(testObject.getObjectId());
		this.testVars.rawObjectProps().setObjectType(testObject.getObjectType());
	}
	
	protected void populateFromParent() throws Exception{
		if (this.parentTestObject != null){
			if (ArjunaInternal.logPropInfo){
				logger.debug("Parent: " + this.getParentTestObject().getObjectType());
				logger.debug("Parent UDV: " + this.getParentTestObject().getTestVariables().udv().items());
				logger.debug("Parent Test Vars: " + this.getParentTestObject().getTestVariables().testProps().items());
				logger.debug("Parent Test Object Vars: " + this.getParentTestObject().getTestVariables().objectProps().items());
			}
			this.getTestVariables().rawObjectProps().cloneAdd(this.getParentTestObject().getTestVariables().objectProps().items());
			this.getTestVariables().rawTestProps().cloneAdd(this.getParentTestObject().getTestVariables().testProps().items());
			this.getTestVariables().rawCustomProps().cloneAdd(this.getParentTestObject().getTestVariables().customProps().items());
			this.getTestVariables().rawUdv().cloneAdd(this.getParentTestObject().getTestVariables().udv().items());
			this.getTestVariables().addDataReferences(this.getParentTestObject().getTestVariables().getAllDataReferences());
			if (testObject.getObjectType() == TestObjectType.TEST_METHOD){
				if (ArjunaInternal.logPropInfo){
					logger.debug(this.getTestVariables().rawObjectProps().objectType() );
					logger.debug(this.getParentTestObject().getTestVariables().objectProps().qualifiedName());
				}
				this.getTestVariables().rawObjectProps().setParentQualifiedName(this.getParentTestObject().getTestVariables().objectProps().qualifiedName());	
			}
		}
	}
	
	protected void populateFromSelf() throws Exception{
		if (ArjunaInternal.logPropInfo){
			logger.debug("Self Type: " + this.getTestObject().getObjectType());
			logger.debug("Self Definition UDV: " + this.getTestObject().getTestVariablesDefinition().udv().items());
			logger.debug("Self Definition Test Props: " + this.getTestObject().getTestVariablesDefinition().testProps().items());
			logger.debug("Self Definition Test Object Props: " + this.getTestObject().getTestVariablesDefinition().objectProps().items());
		}
		this.getTestVariables().rawObjectProps().cloneAdd(this.getTestObject().getTestVariablesDefinition().objectProps().items());
		this.getTestVariables().rawTestProps().cloneAdd(this.getTestObject().getTestVariablesDefinition().testProps().items());
		this.getTestVariables().rawCustomProps().cloneAdd(this.getTestObject().getTestVariablesDefinition().customProps().items());
		this.getTestVariables().rawUdv().cloneAdd(this.getTestObject().getTestVariablesDefinition().udv().items());
		this.getTestVariables().addDataReferences(this.getTestObject().getTestVariablesDefinition().getAllDataReferences());
	}
	
	public void populate() throws Exception{
		if (ArjunaInternal.logPropInfo){
			logger.debug(String.format("Now populating test variables for: %s", this.testObject.getObjectId()));
		}
		populateFromParent();
		populateFromSelf();
		populateObjectIdentification();
		
		if (ArjunaInternal.logPropInfo){
			logger.debug("-------------------");
			logger.debug("Self Type: " + this.getTestVariables().objectProps().objectType());
			logger.debug("Self UDV: " + this.getTestVariables().udv().items());
			logger.debug("Self Test Props: " + this.getTestVariables().testProps().items());
			logger.debug("Self Test Object Props: " + this.getTestVariables().objectProps().items());
			logger.debug("-------------------");
		}
	}

}


/*
subscriptions.put("LAYERS", new ArrayList<String>());
subscriptions.put("COMPONENTS", new ArrayList<String>());
subscriptions.put("MODULES", new ArrayList<String>());
subscriptions.put("VERSIONS", new ArrayList<String>());
subscriptions.put("TYPES", new ArrayList<String>());
subscriptions.put("LEVELS", new ArrayList<String>());
subscriptions.put("OS", new ArrayList<String>());
subscriptions.put("CATEGORIES", new ArrayList<String>());
subscriptions.put("BUGS", new ArrayList<String>());
subscriptions.put("AUTHORS", new ArrayList<String>());
subscriptions.put("CUSTOM_TAGS", new ArrayList<String>());
*/