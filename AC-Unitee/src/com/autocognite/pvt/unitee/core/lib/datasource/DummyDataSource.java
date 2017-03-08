package com.autocognite.pvt.unitee.core.lib.datasource;

import com.autocognite.arjuna.bases.DefaultDataRecord;
import com.autocognite.arjuna.exceptions.DataSourceFinishedException;
import com.autocognite.arjuna.interfaces.DataRecord;
import com.autocognite.arjuna.interfaces.DataSource;

public class DummyDataSource implements DataSource{
	boolean done = false;
	static DefaultDataRecord record = new DefaultDataRecord();

	@Override
	public DataRecord next() throws DataSourceFinishedException {
		if (done){
			throw new DataSourceFinishedException("Done");
		} else {
			done = true;
			return record;
		}
	}

}
