package com.autocognite.pvt.unitee.core.lib.datasource;

import java.util.Iterator;
import java.util.List;

import com.autocognite.batteries.databroker.DataRecord;
import com.autocognite.batteries.databroker.DataRecordContainer;
import com.autocognite.batteries.databroker.DataSource;
import com.autocognite.batteries.databroker.DataSourceFinishedException;
import com.autocognite.batteries.databroker.ReadOnlyDataRecord;

public class DataArrayDataSource implements DataSource{
	private DataRecordContainer container = null;
	private Iterator<ReadOnlyDataRecord> iter = null;

	public DataArrayDataSource(String[] headers, List<String[]> valuesArr) throws Exception {
		container = new DataRecordContainer();
		for (String[] rec: valuesArr){
			DataRecord record = null;
			if (headers.length == 0){
				record = new DataRecord(rec);
			} else {
				record = new DataRecord(headers, rec);
			}
			container.add(record);
		}
		this.initialize();
	}
	
	public void initialize(){
		iter = container.iterator();
	}
	
	public ReadOnlyDataRecord next() throws DataSourceFinishedException{
		if (iter.hasNext()){
			return iter.next();
		} else {
			throw new DataSourceFinishedException("Done");
		}
	}

}
