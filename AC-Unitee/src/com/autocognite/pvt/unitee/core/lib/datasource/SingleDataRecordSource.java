package com.autocognite.pvt.unitee.core.lib.datasource;

import com.autocognite.arjuna.exceptions.DataSourceFinishedException;
import com.autocognite.arjuna.interfaces.DataSource;
import com.autocognite.arjuna.utils.datarecord.DefaultDataRecord;

public class SingleDataRecordSource implements DataSource{
	private DefaultDataRecord record = null;
	private boolean done = false;
	
	public SingleDataRecordSource(String[] headers, String[] values) throws Exception{
		if (headers.length == 0){
			record = new DefaultDataRecord(values);
		} else {
			record = new DefaultDataRecord(headers, values);
		}
	}
	
	public void initialize(){
		// Do nothing
	}
	
	public DefaultDataRecord next() throws DataSourceFinishedException{
		if (done){
			throw new DataSourceFinishedException("Done");
		} else {
			done = true;
			return record;
		}
	}

}
