package com.autocognite.pvt.unitee.core.lib.datasource;

import com.autocognite.arjuna.exceptions.DataSourceFinishedException;
import com.autocognite.arjuna.interfaces.DataSource;
import com.autocognite.pvt.batteries.databroker.DataRecord;

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
