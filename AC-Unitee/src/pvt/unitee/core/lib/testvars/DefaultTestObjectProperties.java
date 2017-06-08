package pvt.unitee.core.lib.testvars;

import arjunasdk.console.Console;
import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.enums.ValueType;
import arjunasdk.interfaces.Value;
import pvt.batteries.container.EnumKeyValueContainer;
import pvt.batteries.ddt.datarecord.BaseDataRecord;
import pvt.batteries.value.DoubleValue;
import pvt.batteries.value.EnumValue;
import pvt.batteries.value.IntValue;
import pvt.batteries.value.LongValue;
import pvt.batteries.value.StringValue;
import pvt.unitee.arjuna.ArjunaInternal;
import unitee.enums.TestObjectAttribute;
import unitee.enums.TestObjectType;

public class DefaultTestObjectProperties 
				extends EnumKeyValueContainer<TestObjectAttribute>
				implements InternalTestObjectProperties{
		
	private String objectId = null;
	private DataRecord dataRecord = null;
	
	public DefaultTestObjectProperties(){

	}
	
	@Override
	public void populateDefaults() throws Exception{
		this.setParentQualifiedName(notSetValue);
		this.setPackage(notSetValue);
		this.setClass(notSetValue);
		this.setObjectType(notSetValue);
		this.setObjectTypeName(notSetValue);
		this.setClassInstanceNumber(naValue);
		this.setClassFragmentNumber(naValue);
		this.setMethod(naValue);
		this.setName(notSetValue);
		this.setMethodInstanceNumber(naValue);
		this.setSessionName(new StringValue("msession"));
		this.setTestNumber(naValue);	
		this.setThreadId(notSetValue);
		this.setSessionNodeName(notSetValue);
		this.setSessionNodeId(notSetValue);
		this.setSessionSubNodeId(notSetValue);
		this.setBeginTstamp(notSetValue);
		this.setEndTstamp(notSetValue);
		this.setTestTime(notSetValue);
	}

	public String objectId() throws Exception{
		return objectId;
	}
	
	public void setObjectId(String name) throws Exception{
		this.objectId = name;
	}
	
	public TestObjectType objectType() throws Exception {
		if (!this.value(TestObjectAttribute.OTYPE).isNull()){
			return this.value(TestObjectAttribute.OTYPE).asEnum(TestObjectType.class);
		} else {
			return null;
		}
	}
	
	public void setObjectType(Value value) throws Exception{
		this.add(TestObjectAttribute.OTYPE, value);
		if (!value.isNull()){
			this.setObjectTypeName(ArjunaInternal.getTestObjectTypeName(value.asEnum(TestObjectType.class).toString()));
		}
	}

	public void setObjectType(TestObjectType type) throws Exception {
		this.setObjectType(new EnumValue<TestObjectType>(type));
	}
	
	private void setObjectTypeName(Value value) throws Exception{
		this.add(TestObjectAttribute.ONAME, value);
	}

	private void setObjectTypeName(String name) throws Exception {
		this.setObjectTypeName(new StringValue(name));
	}
	
	public String qualifiedName() throws Exception{
		if (this.method().equals("NA")){
			return this.value(TestObjectAttribute.PNAME).asString() + "." + this.value(TestObjectAttribute.CNAME).asString();
		} else {
			return this.value(TestObjectAttribute.PNAME).asString() + "." + this.value(TestObjectAttribute.CNAME).asString() + "." + this.value(TestObjectAttribute.MNAME).asString();
		}
	}
	
	public String parentQualifiedName() throws Exception{
		return this.value(TestObjectAttribute.PQNAME).asString();
	}
	
	public void setParentQualifiedName(Value value) throws Exception{
		super.add(TestObjectAttribute.PQNAME, value);
	}
	
	public void setParentQualifiedName(String name) throws Exception{
		this.setParentQualifiedName(new StringValue(name));
	}
	
	public String pkg() throws Exception{
		return this.value(TestObjectAttribute.PNAME).asString();
	}
	
	public void setPackage(Value value) throws Exception{
		super.add(TestObjectAttribute.PNAME, value);
	}
	
	public void setPackage(String name) throws Exception{
		this.setPackage(new StringValue(name));
	}

	public String klass() throws Exception{
		return this.value(TestObjectAttribute.CNAME).asString();
	}
	
	public void setClass(Value value) throws Exception{
		super.add(TestObjectAttribute.CNAME, value);
	}
	
	public void setClass(String name) throws Exception{
		this.setClass(new StringValue(name));
	}
	public int classInstanceNumber() throws Exception{
		return this.value(TestObjectAttribute.CIN).asInt();
	}
	
	public void setClassInstanceNumber(Value value) throws Exception{
		super.add(TestObjectAttribute.CIN, value);
	}
	
	public void setClassInstanceNumber(int num) throws Exception{
		this.setClassInstanceNumber(new IntValue(num));
	}
	
	public int classFragmentNumber() throws Exception{
		return this.value(TestObjectAttribute.CFN).asInt();
	}
	
	public void setClassFragmentNumber(Value value) throws Exception{
		super.add(TestObjectAttribute.CFN, value);
	}
	
	public void setClassFragmentNumber(int num) throws Exception{
		this.setClassFragmentNumber(new IntValue(num));
	}
	
	public String method() throws Exception{
		return this.value(TestObjectAttribute.MNAME).asString();
	}
	
	public void setMethod(Value value) throws Exception{
		super.add(TestObjectAttribute.MNAME, value);
	}
	
	public void setMethod(String name) throws Exception{
		this.setMethod(new StringValue(name));
	}
	
	public String name() throws Exception{
		return this.value(TestObjectAttribute.MNAME).asString();
	}
	
	public void setName(Value value) throws Exception{
		super.add(TestObjectAttribute.NAME, value);
	}
	
	public void setName(String name) throws Exception{
		this.setName(new StringValue(name));
	}
	
	public int methodInstanceNumber() throws Exception{
		return this.value(TestObjectAttribute.MIN).asInt();
	}
	
	public void setMethodInstanceNumber(Value value) throws Exception{
		super.add(TestObjectAttribute.MIN, value);
	}
	
	public void setMethodInstanceNumber(int num) throws Exception{
		this.setMethodInstanceNumber(new IntValue(num));
	}
	
	public int testNumber() throws Exception{
		return this.value(TestObjectAttribute.TN).asInt();
	}

	public void setTestNumber(Value value) throws Exception{
		super.add(TestObjectAttribute.TN, value);
	}
	
	public void setTestNumber(int num) throws Exception{
		this.setTestNumber(new IntValue(num));
	}
	
	public String sessionName() throws Exception{
		return this.value(TestObjectAttribute.SN).asString();
	}
	
	public void setSessionName(Value value) throws Exception{
		super.add(TestObjectAttribute.SN, value);
	}
	
	public void setSessionName(String name) throws Exception{
		this.setSessionName(new StringValue(name));
	}
	
	public String group() throws Exception{
		return this.value(TestObjectAttribute.GN).asString();
	}
	
	public void setGroupName(Value value) throws Exception{
		super.add(TestObjectAttribute.GN, value);
	}
	
	public void setGroupName(String name) throws Exception{
		this.setGroupName(new StringValue(name));
	}
	
	
	public String threadId() throws Exception{
		return this.value(TestObjectAttribute.TID).asString();
	}
	
	public void setThreadId(Value value) throws Exception{
		super.add(TestObjectAttribute.TID, value);
	}
	
	public void setThreadId(String id) throws Exception{
		this.setThreadId(new StringValue(id));
	}
	
	public DataRecord dataRecord() throws Exception{
		return dataRecord;
	}
	
	public void setDataRecord(BaseDataRecord dataRecord) throws Exception{
		this.dataRecord = dataRecord;
	}
	
	public void setDataRecord(String id) throws Exception{
		this.setThreadId(new StringValue(id));
	}
	
	public String sessionNodeName() throws Exception{
		return this.value(TestObjectAttribute.NNAME).asString();
	}
	
	public void setSessionNodeName(Value value) throws Exception{
		super.add(TestObjectAttribute.NNAME, value);
	}
	
	public void setSessionNodeName(String name) throws Exception{
		this.setSessionNodeName(new StringValue(name));
	}
	
	public int sessionNodeId() throws Exception{
		return this.value(TestObjectAttribute.NID).asInt();
	}
	
	public void setSessionNodeId(Value value) throws Exception{
		super.add(TestObjectAttribute.NID, value);
	}
	
	public void setSessionNodeId(int id) throws Exception{
		this.setSessionNodeId(new IntValue(id));
	}
	
	public int sessionSubNodeId() throws Exception{
		return this.value(TestObjectAttribute.SNID).asInt();
	}
	
	public void setSessionSubNodeId(Value value) throws Exception{
		super.add(TestObjectAttribute.SNID, value);
	}
	
	public void setSessionSubNodeId(int id) throws Exception{
		this.setSessionSubNodeId(new IntValue(id));
	}
		
	private void setBeginTstamp(Value value) {
		super.add(TestObjectAttribute.BTSTAMP, value);
	}
		
	private void setEndTstamp(Value value) {
		super.add(TestObjectAttribute.ETSTAMP, value);
	}

	private void setTestTime(Value value) throws Exception {
		super.add(TestObjectAttribute.TTIME, value);
	}
	
	public long bTstamp() throws Exception{
		return this.value(TestObjectAttribute.BTSTAMP).asLong();
	}
	
	@Override
	public void setBeginTstamp() throws Exception {
		this.setBeginTstamp(new LongValue(System.currentTimeMillis()));
	}
	
	public long eTstamp() throws Exception{
		return this.value(TestObjectAttribute.ETSTAMP).asLong();
	}

	@Override
	public void setEndTstamp() throws Exception {
		this.setEndTstamp(new LongValue(System.currentTimeMillis()));
		double f = (new Double(eTstamp()) - bTstamp())/1000;
		this.setTestTime(new DoubleValue(f));
	}
	
	public Double time() throws Exception{
		return this.value(TestObjectAttribute.TTIME).asDouble();
	}

	@Override
	public ValueType valueType(TestObjectAttribute propType) {
		switch (propType){
		case PQNAME:
			return ValueType.STRING;
		case PNAME:
			return ValueType.STRING;
		case CNAME:
			return ValueType.STRING;
		case CIN:
			return ValueType.INTEGER;
		case CFN:
			return ValueType.INTEGER;
		case MNAME:
			return ValueType.STRING;
		case NAME:
			return ValueType.STRING;
		case MIN:
			return ValueType.INTEGER;
		case SN:
			return ValueType.STRING;
		case GN:
			return ValueType.STRING;
		case TN:
			return ValueType.INTEGER;
		case OTYPE:
			return ValueType.ENUM;
		case ONAME:
			return ValueType.STRING;
		case TID:
			return ValueType.STRING;	
		case NNAME:
			return ValueType.STRING;			
		case NID:
			return ValueType.INTEGER;		
		case SNID:
			return ValueType.INTEGER;
		case BTSTAMP:
			return ValueType.LONG;
		case ETSTAMP:
			return ValueType.LONG;
		case TTIME:
			return ValueType.DOUBLE;
		}
		return null;
	}

	@Override
	public ValueType valueType(String strKey) {
		return this.valueType(key(strKey));
	}

	@Override
	public TestObjectAttribute key(String strKey) {
		return TestObjectAttribute.valueOf(strKey.toUpperCase());
	}

	@Override
	public Class valueEnumType(String strKey) {
		TestObjectAttribute key = key(strKey);
		if (valueType(key) != ValueType.ENUM){
			return null;
		} else {
			switch (key){
			case OTYPE:
				return TestObjectType.class;		
			}
		}
		return null;
	}
	
	public DefaultTestObjectProperties clone(){
		DefaultTestObjectProperties map = new DefaultTestObjectProperties();
		try{
			map.cloneAdd(this.items());
		} catch (Exception e){
			Console.displayExceptionBlock(e);
		}
		return map;
	}
}
