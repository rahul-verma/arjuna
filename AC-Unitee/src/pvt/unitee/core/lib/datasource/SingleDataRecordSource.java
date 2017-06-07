package pvt.unitee.core.lib.datasource;

import arjunasdk.ddauto.datarecord.ListDataRecord;
import arjunasdk.ddauto.datarecord.MapDataRecord;
import arjunasdk.ddauto.exceptions.DataSourceFinishedException;
import arjunasdk.ddauto.interfaces.DataRecord;
import pvt.batteries.ddt.datarecord.BaseDataRecord;
import pvt.batteries.ddt.datarecord.BaseDataSource;

public class SingleDataRecordSource extends BaseDataSource{
	private BaseDataRecord record = null;
	private boolean done = false;
	
	public SingleDataRecordSource(String[] headers, String[] values) throws Exception{
		if (headers.length == 0){
			record = new ListDataRecord(values);
		} else {
			record = new MapDataRecord(headers, values);
		}
	}
	
	public void initialize(){
		// Do nothing
	}
	
	public DataRecord next() throws DataSourceFinishedException{
		if ((!isTerminated()) && (!done)){
			done = true;
			return record;
		} else {
			throw new DataSourceFinishedException("Done");
		}
	}

}
