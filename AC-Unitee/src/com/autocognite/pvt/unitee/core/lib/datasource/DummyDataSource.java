package com.autocognite.pvt.unitee.core.lib.datasource;

import com.autocognite.batteries.databroker.DataRecord;
import com.autocognite.batteries.databroker.DataSource;
import com.autocognite.batteries.databroker.DataSourceFinishedException;
import com.autocognite.batteries.databroker.ReadOnlyDataRecord;

public class DummyDataSource implements DataSource{
	boolean done = false;
	static DataRecord record = new DataRecord();

	@Override
	public ReadOnlyDataRecord next() throws DataSourceFinishedException {
		if (done){
			throw new DataSourceFinishedException("Done");
		} else {
			done = true;
			return record;
		}
	}

}
