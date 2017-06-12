package pvt.unitee.core.lib.datasource;

import arjunasdk.ddauto.exceptions.DataSourceFinishedException;
import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.ddauto.lib.BaseDataSource;
import arjunasdk.ddauto.lib.MapDataRecord;
import pvt.batteries.ddt.datarecord.BaseDataRecord;

public class DummyDataSource extends BaseDataSource{
	boolean done = false;
	static BaseDataRecord record = new MapDataRecord();

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
