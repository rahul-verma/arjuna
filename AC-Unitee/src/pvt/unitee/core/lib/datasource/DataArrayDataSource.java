package pvt.unitee.core.lib.datasource;

import java.util.Iterator;
import java.util.List;

import arjunasdk.ddauto.datarecord.ListDataRecordContainer;
import arjunasdk.ddauto.datarecord.MapDataRecordContainer;
import arjunasdk.ddauto.exceptions.DataSourceFinishedException;
import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.ddauto.interfaces.DataRecordContainer;
import pvt.batteries.ddt.datarecord.BaseDataSource;

public class DataArrayDataSource extends BaseDataSource{
	private DataRecordContainer container = null;
	private Iterator<DataRecord> iter = null;

	public DataArrayDataSource(String[] headers, List<String[]> valuesArr) throws Exception {
		if (headers.length == 0){
			container = new ListDataRecordContainer();
		} else {
			container = new MapDataRecordContainer();
			container.setHeaders(headers);
		}
		
		for (String[] rec: valuesArr){
			container.add(rec);
		}
	}
	
	public DataRecord next() throws Exception{
		if ((!isTerminated()) && (container.hasNext())){
			return container.next();
		} else {
			throw new DataSourceFinishedException("Done");
		}
	}

}
