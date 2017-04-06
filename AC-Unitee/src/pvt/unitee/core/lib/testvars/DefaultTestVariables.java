package pvt.unitee.core.lib.testvars;

import java.util.HashMap;
import java.util.Map;

import com.arjunapro.ddt.datarecord.MapDataRecord;
import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.testauto.interfaces.TestObjectProperties;
import com.arjunapro.testauto.interfaces.TestProperties;
import com.google.gson.JsonObject;

import pvt.arjunapro.ddt.interfaces.DataReference;
import pvt.batteries.config.Batteries;
import pvt.batteries.value.DefaultStringKeyValueContainer;
import pvt.unitee.reporter.lib.reportable.TestVariablesSerializer;

public class DefaultTestVariables implements InternalTestVariables {
	private InternalTestObjectProperties objectProps = new DefaultTestObjectProperties();
	private InternalTestProperties testProps = new DefaultTestProperties();
	private DefaultStringKeyValueContainer customProps = new DefaultStringKeyValueContainer();
	private DefaultStringKeyValueContainer utvars = new DefaultStringKeyValueContainer();
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
	
	/* (non-Javadoc)
	 * @see com.autocognite.result.TestVariables#customProps()
	 */
	@Override
	public DefaultStringKeyValueContainer utp() throws Exception {
		return this.rawCustomProps();
	}
	
	/* (non-Javadoc)
	 * @see com.autocognite.result.TestVariables#utv()
	 */
	@Override
	public DefaultStringKeyValueContainer utv() throws Exception {
		return this.rawUtv();
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
	public DefaultStringKeyValueContainer rawCustomProps() throws Exception {
		return this.customProps;
	}

	@Override
	public DefaultStringKeyValueContainer rawUtv() throws Exception {
		return this.utvars;
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
	public void setCustomProps(DefaultStringKeyValueContainer props) throws Exception {
		this.customProps = props;
	}

	@Override
	public void setUtv(DefaultStringKeyValueContainer props) throws Exception {
		this.utvars = props;
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
