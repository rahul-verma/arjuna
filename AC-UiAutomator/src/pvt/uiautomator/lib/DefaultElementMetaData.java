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

import java.util.ArrayList;
import java.util.HashMap;

import com.arjunapro.testauto.config.RunConfig;
import com.arjunapro.uiauto.enums.UiAutomationContext;
import com.arjunapro.uiauto.enums.UiElementType;

import pvt.batteries.config.Batteries;
import pvt.batteries.exceptions.Problem;
import pvt.uiauto.enums.IdentifyBy;
import pvt.uiautomator.UiAutomator;
import pvt.uiautomator.api.ElementMetaData;
import pvt.uiautomator.api.Identifier;

public class DefaultElementMetaData implements ElementMetaData {
	private HashMap<String, String> metaData = new HashMap<String, String>();
	ArrayList<Identifier> identifiers = new ArrayList<Identifier>();
	// private ArrayList<String> identificationOrder = new ArrayList<String>();
	private boolean relevant = false;
	//private boolean multiId = false;
	private UiAutomationContext identificationContext = null;
	
	public DefaultElementMetaData(HashMap<String, String> map) {
		for (String key: map.keySet()){
			set(key, map.get(key));
		}
	}
	
//	/* (non-Javadoc)
//	 * @see com.autocognite.uiautomator.base.metadata.IElementMetaData#getIdentificationOrder()
//	 */
//	@Override
//	public ArrayList<String> getIdentificationOrder(){
//		return this.identificationOrder;
//	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.uiautomator.base.metadata.IElementMetaData#isRelevantForEntity()
	 */
	@Override
	public boolean isRelevantForPage(){
		return relevant;
	}

	protected void setRelevance(boolean flag){
		this.relevant = flag;
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.uiautomator.base.metadata.IElementMetaData#set(java.lang.String, java.lang.String)
	 */
	@Override
	public void set(String propName, String value) {
		metaData.put(propName.toUpperCase(), value);
	}

	/* (non-Javadoc)
	 * @see com.autocognite.uiautomator.base.metadata.IElementMetaData#get(java.lang.String)
	 */
	@Override
	public String get(String propName) {
		return metaData.get(propName.toUpperCase());
	}

//	/* (non-Javadoc)
//	 * @see com.autocognite.uiautomator.base.metadata.IElementMetaData#keys()
//	 */
//	@Override
//	public Set<String> keys() {
//		return metaData.keySet();
//	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.uiautomator.base.metadata.IElementMetaData#getAllProperties()
	 */
	@Override
	public HashMap<String, String> getAllProperties() {
		return metaData;
	}
//	
//	/* (non-Javadoc)
//	 * @see com.autocognite.uiautomator.base.metadata.IElementMetaData#setMultiIdentification()
//	 */
//	@Override
//	public void setMultiIdentification(){
//		this.multiId = true;
//	}
	
//	/* (non-Javadoc)
//	 * @see com.autocognite.uiautomator.base.metadata.IElementMetaData#hasMultiIdentification()
//	 */
//	@Override
//	public boolean hasMultiIdentification(){
//		return multiId;
//	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.uiautomator.base.metadata.IElementMetaData#getAllowedIdentifiers()
	 */
	@Override
	public ArrayList<String> getAllowedIdentifiers() throws Exception{
		return UiAutomator.getAllowedIdentifiers(identificationContext);
	}
	
	public void process(UiAutomationContext identificationContext) throws Exception{
		this.identificationContext = identificationContext;
		for (String property: getAllProperties().keySet()){
			String upProperty = property.toUpperCase();
			String value = get(property);
			// Is it an identifier?
			if(getAllowedIdentifiers().contains(upProperty)){
				switch(IdentifyBy.valueOf(upProperty)){
				case ID: addIdentifier(upProperty, value);break;
				case NAME: addIdentifier(upProperty, value);break;
				case CLASS: addIdentifier(upProperty, value);break;
				case LINK_TEXT: addIdentifier(upProperty, value);break;
				case PARTIAL_LINK_TEXT: addIdentifier(upProperty, value);break;
				case XPATH: addIdentifier(upProperty, value);break;
				case CSS: addIdentifier(upProperty, value); break;
				case TAG: addIdentifier(upProperty, value);break;
				case IMAGE: addIdentifier(upProperty, value);break;
				case X_TEXT:
					addIdentifier("XPATH", String.format("//*[text()='%s']", value));
					break;
				case X_PARTIAL_TEXT: 
					addIdentifier("XPATH", String.format("//*[contains(text(),'%s')]", value));
					break;
				case X_VALUE:
					addIdentifier("XPATH", String.format("//*[@value='%s']", value));
					break;					
				case X_TITLE: 
					addIdentifier("XPATH", String.format("//*[@title='%s']", value));
					break;
				case X_IMAGE_SRC:
					addIdentifier("XPATH", String.format("//img[@src='%s']", value));
					break;
				case X_TYPE:
					String upValue = value.toUpperCase();
					if (UiAutomator.getAllAllowedUiElementTypes().contains(upValue)){
						UiElementType elementType = UiElementType.valueOf(upValue);
						switch(elementType){
						case TEXTBOX:
							addIdentifier("XPATH", String.format("//input[@type='text']", value));
							break;	
						case PASSWORD:
							addIdentifier("XPATH", String.format("//input[@type='password']", value));
							break;	
						case LINK: 
							addIdentifier("XPATH", String.format("//a", value));
							break;	
						case BUTTON: 
							addIdentifier("XPATH", String.format("//input[@type='button']", value));
							break;	
						case SUBMIT_BUTTON: 
							addIdentifier("XPATH", String.format("//input[@type='submit']", value));
							break;	
						case DROPDOWN: 
							addIdentifier("XPATH", String.format("//select", value));
							break;	
						case CHECKBOX: 
							addIdentifier("XPATH", String.format("//input[@type='checkbox']", value));
							break;	
						case RADIO: 
							addIdentifier("XPATH", String.format("//input[@type='radio']", value));
							break;
						case IMAGE: 
							addIdentifier("XPATH", String.format("//img", value));
							break;	
						}
					} else {
				// Do nothing. BECAUSE a single map is used across multiple automators.
					} 
				}
			}else {
				// Opportunity for meta properties.
			}
			
		}

	
		calculateRelevance();
	}
	
	public void processStrictly(UiAutomationContext context) throws Exception{
		this.process(context);
		if (!this.isRelevantForPage()){
			throw new Problem(
					Batteries.getComponentName("UI_AUTOMATOR"),
					"Element Meta Data",
					"processStrictly",
					UiAutomator.problem.UI_ELEMENT_INVALID_METADATA,
					Batteries.getProblemText(
							UiAutomator.problem.UI_ELEMENT_INVALID_METADATA, 
							UiAutomator.getAutomationContextName(context),
							metaData.toString())
							
				);
		}
	}

	protected void calculateRelevance(){
		if (identifiers.size() > 0){
			setRelevance(true);
		}		
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.uiautomator.base.metadata.IWebElementMetaData#getIdentifiers()
	 */
	@Override
	public ArrayList<Identifier> getIdentifiers(){
		return identifiers;
	}

	@Override
	public void addIdentifier(String key, String value) {
		identifiers.add(new Identifier(key, value));
	}
	
}

