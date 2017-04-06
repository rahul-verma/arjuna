package pvt.unitee.core.lib.datasource;

import com.arjunapro.ddt.datarecord.ListDataRecord;
import com.arjunapro.ddt.datarecord.MapDataRecord;
import com.arjunapro.ddt.exceptions.DataSourceFinishedException;
import com.arjunapro.ddt.interfaces.DataRecord;

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
