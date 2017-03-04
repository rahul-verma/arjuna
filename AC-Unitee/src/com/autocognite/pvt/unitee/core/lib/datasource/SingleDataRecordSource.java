package com.autocognite.pvt.unitee.core.lib.datasource;

import com.autocognite.batteries.databroker.DataRecord;
import com.autocognite.batteries.databroker.DataSource;
import com.autocognite.batteries.databroker.DataSourceFinishedException;

public class SingleDataRecordSource implements DataSource{
	private DataRecord record = null;
	private boolean done = false;
	
	public SingleDataRecordSource(String[] headers, String[] values) throws Exception{
		if (headers.length == 0){
			record = new DataRecord(values);
		} else {
			record = new DataRecord(headers, values);
		}
	}
	
	public void initialize(){
		// Do nothing
	}
	
	public DataRecord next() throws DataSourceFinishedException{
		if (done){
			throw new DataSourceFinishedException("Done");
		} else {
			done = true;
			return record;
		}
	}

}
