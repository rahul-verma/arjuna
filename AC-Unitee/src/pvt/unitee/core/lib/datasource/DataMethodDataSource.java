package pvt.unitee.core.lib.datasource;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.Iterator;

import com.arjunapro.ddt.datarecord.DefaultDataRecordContainer;
import com.arjunapro.ddt.interfaces.DataRecord;
import com.arjunapro.ddt.interfaces.DataRecordContainer;
import com.arjunapro.ddt.interfaces.DataSource;
import com.arjunapro.testauto.exceptions.DataSourceFinishedException;

public class DataMethodDataSource implements DataSource{
	private static Object[][] sampleArr = {};
	private Method dataMethod = null;
	DataRecordContainer recordContainer =  null;
	Iterator<DataRecord> iter = null;
	
	public DataMethodDataSource(Method dataMethod) throws Exception{
		if (Modifier.isStatic(dataMethod.getModifiers())){
			this.dataMethod = dataMethod;
		} else {
			throw new Exception(String.format("Data method must be static: %s.%s", dataMethod.getDeclaringClass().getName(),dataMethod.getName()));
		}
		this.init();
	}
	 
	public void init() throws Exception{
//			logger.debug("The method is invoked in static manner for class: " + targetMethod.getDeclaringClass().getName());
		if (dataMethod.getReturnType().isAssignableFrom(sampleArr.getClass())){
			recordContainer = new DefaultDataRecordContainer((Object[][]) dataMethod.invoke(null));
		} else {
			recordContainer = (DataRecordContainer) dataMethod.invoke(null);
		}	
		iter = recordContainer.iterator();
	}
	
	public DataRecord next() throws DataSourceFinishedException{
		if (iter.hasNext()){
			return iter.next();
		} else {
			throw new DataSourceFinishedException("Done");
		}
	}

}
