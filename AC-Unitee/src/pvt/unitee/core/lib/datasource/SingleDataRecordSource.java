package pvt.unitee.core.lib.datasource;

import arjunasdk.ddauto.exceptions.DataSourceFinishedException;
import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.ddauto.lib.BaseDataSource;
import arjunasdk.ddauto.lib.ListDataRecord;
import arjunasdk.ddauto.lib.MapDataRecord;
import pvt.batteries.ddt.datarecord.BaseDataRecord;

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
