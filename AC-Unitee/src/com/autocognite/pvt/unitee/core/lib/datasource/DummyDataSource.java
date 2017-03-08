package com.autocognite.pvt.unitee.core.lib.datasource;

import com.autocognite.arjuna.exceptions.DataSourceFinishedException;
import com.autocognite.arjuna.interfaces.DataSource;
import com.autocognite.arjuna.interfaces.ReadOnlyDataRecord;
import com.autocognite.pvt.batteries.databroker.DataRecord;

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
