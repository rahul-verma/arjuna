package com.autocognite.pvt.unitee.core.lib.testvars;

import java.util.HashMap;
import java.util.Map;

import com.autocognite.arjuna.interfaces.TestObjectProperties;
import com.autocognite.arjuna.interfaces.TestProperties;
import com.autocognite.batteries.config.RunConfig;
import com.autocognite.batteries.databroker.DataRecord;
import com.autocognite.batteries.databroker.DataReference;
import com.autocognite.batteries.databroker.ReadOnlyDataRecord;
import com.autocognite.batteries.value.StringKeyValueContainer;
import com.autocognite.pvt.unitee.reporter.lib.reportable.TestVariablesSerializer;
import com.google.gson.JsonObject;

public class DefaultTestVariables implements InternalTestVariables {
	private InternalTestObjectProperties objectProps = new DefaultTestObjectProperties();
	private InternalTestProperties testProps = new DefaultTestProperties();
	private StringKeyValueContainer customProps = new StringKeyValueContainer();
	private StringKeyValueContainer udvars = new StringKeyValueContainer();
	private ReadOnlyDataRecord dataRecord =  null;
	private Map<String,DataReference> dataRefMap = new HashMap<String,DataReference>();
	private static ReadOnlyDataRecord dr = new DataRecord();
	
	public DefaultTestVariables() throws Exception{
		this.dataRecord = dr;		
	}
	
	public void populateDefaults() throws Exception{
		this.objectProps.populateDefaults();
		this.testProps.populateDefaults();
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.result.TestVariables#autoProps()
	 */
	@Override
	public TestObjectProperties objectProps() throws Exception {
		return this.rawObjectProps();
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.result.TestVariables#testProps()
	 */
	@Override
	public TestProperties testProps() throws Exception {
		return this.rawTestProps();
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.result.TestVariables#customProps()
	 */
	@Override
	public StringKeyValueContainer customProps() throws Exception {
		return this.rawCustomProps();
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.result.TestVariables#udv()
	 */
	@Override
	public StringKeyValueContainer udv() throws Exception {
		return this.rawUdv();
	}

	@Override
	public InternalTestObjectProperties rawObjectProps() throws Exception {
		return this.objectProps;
	}

	@Override
	public InternalTestProperties rawTestProps() throws Exception {
		return this.testProps;
	}

	@Override
	public StringKeyValueContainer rawCustomProps() throws Exception {
		return this.customProps;
	}

	@Override
	public StringKeyValueContainer rawUdv() throws Exception {
		return this.udvars;
	}

	@Override
	public void setObjectProps(InternalTestObjectProperties props) throws Exception {
		this.objectProps = props;
	}

	@Override
	public void setTestProps(InternalTestProperties props) throws Exception {
		this.testProps = props;
	}

	@Override
	public void setCustomProps(StringKeyValueContainer props) throws Exception {
		this.customProps = props;
	}

	@Override
	public void setUdv(StringKeyValueContainer props) throws Exception {
		this.udvars = props;
	}
	
	public JsonObject asJsonObject() throws Exception{
		JsonObject obj =  new JsonObject();
		TestVariablesSerializer serializer = new TestVariablesSerializer();
		serializer.serializeTestVariables(obj, this);
		return obj;
	}

	@Override
	public void setDataRecord(ReadOnlyDataRecord dataRecord) {
		this.dataRecord = dataRecord;
	}
	
	@Override
	public ReadOnlyDataRecord dataRecord() {
		return this.dataRecord;
	}

	@Override
	public DataReference dataRef(String refName) throws Exception {
		String uName = refName.toUpperCase();
		if (this.dataRefMap.containsKey(uName)){
			return this.dataRefMap.get(uName);
		} else {
			try{
				return RunConfig.getDataReference(uName);
			} catch (Exception e){
				throw new Exception(
						String.format("No reference found with name \"%s\" for current test object or in central repository.",
								refName));
			}
		}
		
	}

	@Override
	public void addDataReference(String name, DataReference dataRef) {
		this.dataRefMap.put(name.toUpperCase(), dataRef);
	}

	@Override
	public Map<String,DataReference> getAllDataReferences() {
		return this.dataRefMap;
	}

	@Override
	public void addDataReferences(Map<String, DataReference> dataRefs) throws Exception {
		this.dataRefMap.putAll(dataRefs);
	}

}
