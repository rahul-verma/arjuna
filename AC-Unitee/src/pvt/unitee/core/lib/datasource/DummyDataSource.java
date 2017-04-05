package pvt.unitee.core.lib.datasource;

import com.arjunapro.ddt.datarecord.DefaultDataRecord;
import com.arjunapro.ddt.exceptions.DataSourceFinishedException;
import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.ddt.interfaces.DataSource;

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
