package pvt.unitee.core.lib.datasource;

import java.util.Iterator;
import java.util.List;

import com.arjunapro.ddt.datarecord.ListDataRecordContainer;
import com.arjunapro.ddt.datarecord.MapDataRecordContainer;
import com.arjunapro.ddt.exceptions.DataSourceFinishedException;
import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.ddt.interfaces.DataRecordContainer;

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
