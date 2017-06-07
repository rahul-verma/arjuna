package pvt.unitee.core.lib.datasource;

import arjunasdk.ddauto.datarecord.MapDataRecord;
import arjunasdk.ddauto.exceptions.DataSourceFinishedException;
import arjunasdk.ddauto.interfaces.DataRecord;
import pvt.batteries.ddt.datarecord.BaseDataRecord;
import pvt.batteries.ddt.datarecord.BaseDataSource;

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
