package pvt.unitee.core.lib.datasource;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.Iterator;

import arjunasdk.ddauto.interfaces.DataRecord;
import arjunasdk.ddauto.interfaces.DataRecordContainer;
import arjunasdk.ddauto.interfaces.DataSource;
import arjunasdk.ddauto.lib.BaseDataSource;
import arjunasdk.ddauto.lib.ListDataRecordContainer;

public class DataMethodDataSource extends BaseDataSource{
	private static Object[][] sampleArr = {};
	private Method dataMethod = null;
	DataSource recordContainer =  null;
	Iterator<DataRecord> iter = null;
	
	public DataMethodDataSource(Method dataMethod) throws Exception{
		if (Modifier.isStatic(dataMethod.getModifiers())){
			this.dataMethod = dataMethod;
		} else {
			throw new Exception(String.format("Data method must be static: %s.%s", dataMethod.getDeclaringClass().getName(),dataMethod.getName()));
		}
		this.init();
		this.recordContainer.validate();
	}
	 
	public void init() throws Exception{
//			logger.debug("The method is invoked in static manner for class: " + targetMethod.getDeclaringClass().getName());
		if (dataMethod.getReturnType().isAssignableFrom(sampleArr.getClass())){
			DataRecordContainer container = new ListDataRecordContainer();
			container.addAll((Object[][]) dataMethod.invoke(null));
			recordContainer = container;
		} else {
			recordContainer = (DataSource) dataMethod.invoke(null);
		}	
	}
	
	public DataRecord next() throws Exception{
		return recordContainer.next();
	}
	
	public void terminate() {
		super.terminate();
		this.recordContainer.terminate();
	}

}
