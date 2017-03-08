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
package com.autocognite.pvt.batteries.lib;

import java.util.ArrayList;
import java.util.HashMap;

import com.autocognite.pvt.batteries.configurator.lib.strings.NamedString;
import com.autocognite.pvt.batteries.ds.MessagesContainer;
import com.autocognite.pvt.batteries.ds.NamesContainer;
import com.autocognite.pvt.batteries.exceptions.Problem;

public class StringsManager {
	HashMap<String, HashMap<String, String>> msgMap = new HashMap<String, HashMap<String, String>>();
	HashMap<String, HashMap<String, String>> nameMap = new HashMap<String, HashMap<String, String>>();
	HashMap<String, String> propMap = new HashMap<String, String>();
	HashMap<String, String> flattenedNames = new HashMap<String, String>();

	private static void populate(HashMap<String, String> map, String[][] codes) {
		for (int i = 0; i < codes.length; i++) {
			map.put(codes[i][0].toUpperCase().trim(), codes[i][1]);
		}
	}

	private static void populate(HashMap<String, String> map, HashMap<String, String> codes) {
		for (String key : codes.keySet()) {
			map.put(key.toUpperCase(), codes.get(key));
		}
	}

	private static void populate(HashMap<String, String> map, ArrayList<NamedString> namedStrings) {
		for (NamedString namedString : namedStrings) {
			map.put(namedString.getCode().toUpperCase(), namedString.getName());
		}
	}

	public void populateNames(ArrayList<NamesContainer> containers) {
		for (NamesContainer container : containers) {
			if (!nameMap.containsKey(container.getName())) {
				nameMap.put(container.getName(), new HashMap<String, String>());
			}
			populate(nameMap.get(container.getName()), container.getNamedStrings());
		}
	}

	public void populateMessages(ArrayList<MessagesContainer> containers) {
		for (MessagesContainer container : containers) {
			if (!msgMap.containsKey(container.getName())) {
				msgMap.put(container.getName(), new HashMap<String, String>());
			}
			populate(msgMap.get(container.getName()), container.getNamedStrings());
		}
	}

	public void populateFlattenedNames() throws Exception {
		for (String section : nameMap.keySet()) {
			for (String key : nameMap.get(section).keySet()) {
				flattenedNames.put(section + "::" + key, nameMap.get(section).get(key));
			}
		}
	}

	public HashMap<String, HashMap<String, String>> getAllNames() {
		return this.nameMap;
	}

	public HashMap<String, HashMap<String, String>> getAllMessages() {
		return this.msgMap;
	}

	public HashMap<String, String> getFlattnededNames() {
		return this.flattenedNames;
	}

	private boolean sectionExists(String section) {
		return this.msgMap.get(section) != null;
	}

	private boolean codeExists(String section, String code) {
		if (!sectionExists(section))
			return false;
		return this.msgMap.get(section).get(code) != null;
	}

	private void throwNotInitializedException(String context, String method) throws Problem {
		throw new Problem("autocognite", context, method, "LOCALIZER_NOT_INITIALIZED",
				"Strings Manager not initialized.");
	}

	private String getTextForCode(String section, String msgCode) throws Exception {
		if (this.msgMap == null) {
			throwNotInitializedException(section, "getTextForCode");
		} else if (!this.msgMap.containsKey(section)) {

		}
		String sectionCode = section.toUpperCase().trim();
		String code = msgCode.toUpperCase().trim();
		if (!codeExists(sectionCode, code))
			return code;
		return this.msgMap.get(sectionCode).get(code);
	}

	public String getInfoMessageText(String msgCode) throws Exception {
		return getTextForCode("INFO_MESSAGES", msgCode);
	}

	public String getProblemText(String msgCode) throws Exception {
		return getTextForCode("PROBLEM_MESSAGES", msgCode);
	}

	public String getWarningText(String msgCode) throws Exception {
		return getTextForCode("WARNING_MESSAGES", msgCode);
	}

	// public String getResultPropertyName(String property) throws Exception {
	// if (this.names == null){
	// throwNotInitializedException("RESULT_PROPERTIES",
	// "getResultPropertyName");
	// }
	// return
	// this.names.get("RESULT_PROPERTIES").get(property.toUpperCase().trim());
	// }

	public String getConfiguredName(String sectionName, String internalName) throws Exception {
		if (this.nameMap == null) {
			throwNotInitializedException(sectionName, "getConfiguredName");
		}
		return this.nameMap.get(sectionName.toUpperCase().trim()).get(internalName.toUpperCase().trim());
	}

	private static class problemCodes {

	}

	private static class infoCodes {

	}

	private static class errorCodes {

	}

	public void addPropertyName(String propCode, String propName) {
		propMap.put(propCode.toUpperCase(), propName);
	}

	public String getPropertyName(String propCode) {
		return propMap.get(propCode.toUpperCase());
	}
}
