package com.autocognite.pvt.unitee.core.lib.datasource;

import java.util.Iterator;
import java.util.List;

import com.autocognite.arjuna.bases.DataRecordContainer;
import com.autocognite.arjuna.bases.DefaultDataRecord;
import com.autocognite.arjuna.exceptions.DataSourceFinishedException;
import com.autocognite.arjuna.interfaces.DataSource;
import com.autocognite.arjuna.interfaces.DataRecord;

public class DataArrayDataSource implements DataSource{
	private DataRecordContainer container = null;
	private Iterator<DataRecord> iter = null;

	public DataArrayDataSource(String[] headers, List<String[]> valuesArr) throws Exception {
		container = new DataRecordContainer();
		for (String[] rec: valuesArr){
			DefaultDataRecord record = null;
			if (headers.length == 0){
				record = new DefaultDataRecord(rec);
			} else {
				record = new DefaultDataRecord(headers, rec);
			}
			container.add(record);
		}
		this.initialize();
	}
	
	public void initialize(){
		iter = container.iterator();
	}
	
	public DataRecord next() throws DataSourceFinishedException{
		if (iter.hasNext()){
			return iter.next();
		} else {
			throw new DataSourceFinishedException("Done");
		}
	}

}
