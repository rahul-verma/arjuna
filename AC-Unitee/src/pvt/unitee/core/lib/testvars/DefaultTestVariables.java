package pvt.unitee.core.lib.testvars;

import java.util.HashMap;
import java.util.Map;

import com.google.gson.JsonObject;

import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.ddauto.interfaces.DataReference;
import arjunasdk.ddauto.lib.MapDataRecord;
import pvt.batteries.config.Batteries;
import pvt.batteries.value.DefaultStringKeyValueContainer;
import pvt.batteries.value.UserStringKeyValueContainer;
import pvt.unitee.reporter.lib.reportable.TestVariablesSerializer;
import unitee.interfaces.TestObjectProperties;
import unitee.interfaces.TestProperties;

public class DefaultTestVariables implements InternalTestVariables {
	private InternalTestObjectProperties objectProps = new DefaultTestObjectProperties();
	private InternalTestProperties testProps = new DefaultTestProperties();
	private UserStringKeyValueContainer attr = new UserStringKeyValueContainer();
	private UserStringKeyValueContainer execVars = new UserStringKeyValueContainer();
	private DataRecord dataRecord =  null;
	private Map<String,DataReference> dataRefMap = new HashMap<String,DataReference>();
	private static DataRecord dr = new MapDataRecord();
	
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
	public TestObjectProperties object() throws Exception {
		return this.rawObjectProps();
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.result.TestVariables#testProps()
	 */
	@Override
	public TestProperties test() throws Exception {
		return this.rawTestProps();
	}
	

	@Override
	public DefaultStringKeyValueContainer attr() throws Exception {
		return this.rawAttr();
	}
	
	@Override
	public DefaultStringKeyValueContainer execVars() throws Exception {
		return this.rawExecVars();
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
	public DefaultStringKeyValueContainer rawAttr() throws Exception {
		return this.attr;
	}

	@Override
	public UserStringKeyValueContainer rawExecVars() throws Exception {
		return this.execVars;
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
	public void setAttr(UserStringKeyValueContainer props) throws Exception {
		this.attr = props;
	}

	@Override
	public void setExecVars(UserStringKeyValueContainer props) throws Exception {
		this.execVars = props;
	}
	
	public JsonObject asJsonObject() throws Exception{
		JsonObject obj =  new JsonObject();
		TestVariablesSerializer serializer = new TestVariablesSerializer();
		serializer.serializeTestVariables(obj, this);
		return obj;
	}

	@Override
	public void setDataRecord(DataRecord dataRecord) {
		this.dataRecord = dataRecord;
	}
	
	@Override
	public DataRecord record() {
		return this.dataRecord;
	}

	@Override
	public DataReference refer(String refName) throws Exception {
		String uName = refName.toUpperCase();
		if (this.dataRefMap.containsKey(uName)){
			return this.dataRefMap.get(uName);
		} else {
			try{
				return Batteries.getDataReference(uName);
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
	public Map<String,DataReference> references() {
		return this.dataRefMap;
	}

	@Override
	public void addDataReferences(Map<String, DataReference> dataRefs) throws Exception {
		this.dataRefMap.putAll(dataRefs);
	}

}
