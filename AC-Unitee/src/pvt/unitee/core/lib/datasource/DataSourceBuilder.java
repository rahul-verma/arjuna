package pvt.unitee.core.lib.datasource;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import arjunasdk.console.Console;
import arjunasdk.ddauto.exceptions.DataSourceConstructionException;
import arjunasdk.ddauto.interfaces.DataSource;
import arjunasdk.sysauto.batteries.FileSystemBatteries;
import arjunasdk.sysauto.batteries.SystemBatteries;
import pvt.arjunapro.ArjunaInternal;
import pvt.arjunapro.annotations.DriveWithDataGenerator;
import pvt.arjunasdk.enums.BatteriesPropertyType;
import pvt.batteries.config.Batteries;
import pvt.batteries.databroker.DataSourceFactory;
import pvt.unitee.core.lib.annotate.None;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import unitee.annotations.Data;
import unitee.annotations.DriveWithData;
import unitee.annotations.DriveWithDataArray;
import unitee.annotations.DriveWithDataFile;
import unitee.annotations.DriveWithDataMethod;

// Purpose of this is to achieve thread safety for Data Sources by creating unique objects every time.
public class DataSourceBuilder {
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private JavaTestClassDefinition testClassDef = null;
	private DataSourceType dataSourceType = null;
	private Method testMethod = null;
	private boolean defProcessed = false;
	
	// For Drive With Data Annotation
	private String[] dataAnnRecord = null;
	private String[] dataAnnHeaders = null;
	
	// For Drive With Data Array Annotation
	private List<String[]> dataArrayRecords = null;
	private String[] dataArrayAnnHeaders = null;
	
	// For Drive With Data File Annotation
	private String location = null;
	private String delimiter = null;
	
	// For Drive With Data File Annotation
	private Method dataMethod = null;
	
	// For Drive With Data Generator Annotation
	private boolean chooseNamedDataGenerator = false;
	private String dataGeneratorName = null;
	private Class<? extends DataSource> dataGeneratorClass;
	
	public void testClassDef(JavaTestClassDefinition testClassDef){
		this.testClassDef = testClassDef;
	}
	
	public void dataSourceType(DataSourceType dataSourceType){
		this.dataSourceType = dataSourceType;
	}
	
	public void testMethod(Method testMethod){
		this.testMethod = testMethod;
	}
	
	private void processDriveWithDataAnnotation() throws Exception{
		Annotation annotation = testMethod.getAnnotation(DriveWithData.class);
		DriveWithData dataContainer = (DriveWithData) annotation;
		if (dataContainer.record().length == 0){
			if (dataContainer.value().length == 0){
				throw new Exception("You must specify either record or value attribute for @DriveWithData annotation with a string array of length > 0");
			} else {
				dataAnnRecord = dataContainer.value();
			}
		} else {
			dataAnnRecord = dataContainer.record();
		}

		dataAnnHeaders = dataContainer.headers();
		
		if ((dataAnnHeaders.length != 0) && (dataAnnHeaders.length != dataAnnRecord.length)){
			Console.displayError("Static Fatal Error: Problem with @DriveWithData annotation's [headers] attribute.");
			Console.displayError(String.format("Problem In: Test Method [%s.%s]", testClassDef.getQualifiedName(), testMethod.getName()));
			Console.displayError("Problem: The length of [headers] and [record] arrays does not match.");
			Console.displayError("Solution: Make [headers] and [record] array of same length. Or remove [headers] altogether and use List Data Record API.");
			//Console.displayExceptionBlock(e);
			SystemBatteries.exit();				
		}
	}
	
	private String[] getValuesFromDataAnnotation(Data annotation) throws Exception{
		String[] dataValues = annotation.value();
		if (dataValues.length == 0){
			throw new Exception("You should provide @Data annotation with a non-empty string array.");
		} else {
			return dataValues;
		}
	}
	
	private void processDriveWithDataArrayAnnotation() throws Exception{
		Annotation annotation = this.testMethod.getAnnotation(DriveWithDataArray.class);
		DriveWithDataArray dataArrayContainer = (DriveWithDataArray) annotation;
		
		dataArrayRecords = new ArrayList<String[]>();
		Data[] annRecordContainers = null;
//		logger.debug(Arrays.toString(dataArrayContainer.records()));
		if (dataArrayContainer.records().length == 0){
			if (dataArrayContainer.value().length == 0){
				throw new Exception("You should provide either records or value attribute for @DriveWithDataArray with 1 or more @Data entries.");
			} else {
				annRecordContainers = dataArrayContainer.value();
			}
		} else {
			annRecordContainers = dataArrayContainer.records();
		}
		
		for (Data annRecordContainer: annRecordContainers){
			dataArrayRecords.add(getValuesFromDataAnnotation(annRecordContainer));
		}		
		
		int refLen = 0;
		boolean first = true;
		for (String[] dataArr: dataArrayRecords){
			if (first){
				refLen = dataArr.length;
				first = false;
				continue;
			}
			
			if (dataArr.length != refLen){
				Console.displayError("Static Fatal Error: Problem with @DriveWithDataArray annotation [records] attribute.");
				Console.displayError(String.format("Problem In: Test Method [%s.%s]", testClassDef.getQualifiedName(), testMethod.getName()));
				Console.displayError("Problem: The length of record entries in [records] array does not match.");
				Console.displayError("Solution: Make all record entries in [records] array of same length.");
				//Console.displayExceptionBlock(e);
				SystemBatteries.exit();						
			}
		}	
		
		dataArrayAnnHeaders = dataArrayContainer.headers();
		
		if ((dataArrayAnnHeaders.length != 0) && (dataArrayAnnHeaders.length != refLen)){
			Console.displayError("Static Fatal Error: Problem with @DriveWithDataArray headers attribute.");
			Console.displayError(String.format("Problem In: Test Method [%s.%s]", testClassDef.getQualifiedName(), testMethod.getName()));
			Console.displayError("Problem: The length of [headers] and record in [records] arrays does not match.");
			Console.displayError("Solution: Make [headers] and length of every record in [records] array of same length. Or remove [headers] altogether and use List Data Record API.");
			//Console.displayExceptionBlock(e);
			SystemBatteries.exit();				
		}
		
	}
	
	private void processDriveWithDataFileAnnotation() throws Exception{
		Annotation annotation = this.testMethod.getAnnotation(DriveWithDataFile.class);
		DriveWithDataFile dataFileAnnotation = (DriveWithDataFile) annotation;
		if (dataFileAnnotation.path().equals("NOT_SET")){
			if (dataFileAnnotation.value().equals("NOT_SET")){
				throw new Exception("Used DriveWithDataFile annotation by providing neither location nor value attribute.");
			} else {
				location = dataFileAnnotation.value();
			}
		} else {
			location = dataFileAnnotation.path();
		}
		
		if (!FileSystemBatteries.isFile(location)){
			location = Batteries.value(BatteriesPropertyType.DIRECTORY_PROJECT_DATA_SOURCES).asString() + "/" + location;
			if (!FileSystemBatteries.isFile(location)){
				throw new Exception(String.format("File path provided using DataFile annotation does not exist: %s", location));
			}
		}

		delimiter = dataFileAnnotation.delimiter();
	}

	private void processDriveWithDataMethodAnnotation() throws Exception{
		Annotation annotation = this.testMethod.getAnnotation(DriveWithDataMethod.class);
		DriveWithDataMethod dataMethodAnnotation = (DriveWithDataMethod) annotation;
		String targetDGMethodName = null;
		String methodContainer = dataMethodAnnotation.container();
		Class<?> containerClass = dataMethodAnnotation.containerClass(); 
		if (containerClass == None.class){
			if (methodContainer.equals("NOT_SET")){
				if (ArjunaInternal.displayDataMethodProcessingInfo){
					logger.debug("The data method is expected to be found in the test class: " + testClassDef.getQualifiedName());
				}
			} else {
				if (ArjunaInternal.displayDataMethodProcessingInfo){
					logger.debug("The data method is expected to be found outside of test");
				}
			}
		} else {
			if (ArjunaInternal.displayDataMethodProcessingInfo){
				logger.debug("The data method is expected to be found outside of test");
			}
		}
		
		if (dataMethodAnnotation.name().equals("NOT_SET")){			
			if (dataMethodAnnotation.value().equals("NOT_SET")){
				throw new Exception("Used DriveWithDataMethod annotation by providing none of the attributes: value/name/methodName.");
			} else {
				targetDGMethodName = dataMethodAnnotation.value();
			}
		} else {
			targetDGMethodName = dataMethodAnnotation.name();
		}
		
		if (containerClass == None.class){
			if (methodContainer.equals("NOT_SET")){
				dataMethod = this.testClassDef.getDataMethodsHandler().getMethod(targetDGMethodName);
			} else {
				dataMethod = ArjunaInternal.getDataGeneratorMethod(methodContainer, targetDGMethodName);
			}
		} else {
			dataMethod = ArjunaInternal.getDataGeneratorMethod(containerClass, targetDGMethodName);
		}
	}
	
	private void processDriveWithDataGenerator() throws Exception{
		Annotation annotation = this.testMethod.getAnnotation(DriveWithDataGenerator.class);
		DriveWithDataGenerator dataGenAnnotation = (DriveWithDataGenerator) annotation;
		String dataGenName = null;
		if (dataGenAnnotation.generatorClass() == None.class){
			if (dataGenAnnotation.name().equals("NOT_SET")){
				if (dataGenAnnotation.value().equals("NOT_SET")){
					throw new Exception("Used DriveWithDataGenerator annotation by providing neither name nor value attribute.");
				} else {
					dataGenName = dataGenAnnotation.value();
				}
			} else {
				dataGenName = dataGenAnnotation.name();
			}
			
			this.chooseNamedDataGenerator = true;
			this.dataGeneratorName = dataGenName;
		} else {
			this.dataGeneratorClass = dataGenAnnotation.generatorClass();
		}
	}
	
	public void process() throws Exception{
		switch (this.dataSourceType){
		case DATA:
			processDriveWithDataAnnotation();
			break;
		case DATA_ARRAY:
			processDriveWithDataArrayAnnotation();
			break;
		case DATA_FILE:
			processDriveWithDataFileAnnotation();
			break;
		case DATA_METHOD:
			processDriveWithDataMethodAnnotation();
			break;
		case DATA_GENERATOR:
			processDriveWithDataGenerator();
			break;
		}
	}
	
	private void throwConstructionException(String ann, String name, Throwable e) throws DataSourceConstructionException{
		String m = null;
		if (e.getMessage() != null){
			m = String.format(" : %s",e.getMessage());
		} else {
			m = ".";
		}
		
		throw new DataSourceConstructionException(
				String.format("Issues in creating Data Source for %s annotation%s", ann, m),
				name,
				e);		
	}
	
	public DataSource build() throws Exception{
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug("Building data source");
		}
		
		String name = null;
		DataSource ds = null;
		switch (this.dataSourceType){
		case DATA:
			try{
				name = String.format("@DriveWithData annotation for %s.%s",this.testClassDef.getQualifiedName(), this.testMethod.getName());
				ds = new SingleDataRecordSource(dataAnnHeaders, dataAnnRecord);
			} catch (Throwable e){
				throwConstructionException("@DriveWithData", name, e);
			}
			break;
		case DATA_ARRAY:
			try{
				name = String.format("@DriveWithDataArray annotation");
				ds = new DataArrayDataSource(this.dataArrayAnnHeaders, this.dataArrayRecords);
			} catch (Throwable e){
				throwConstructionException("@DriveWithDataArray", name, e);
			}
			break;
		case DATA_FILE:
			try{
				name = String.format("@DriveWithDataFile annotation");
				ds = DataSourceFactory.getDataSource(this.location, this.delimiter);
			} catch (Throwable e){
				throwConstructionException("@DriveWithDataFile", name, e);
			}
			break;
		case DATA_METHOD:
			try{
				name = String.format("[%s] data method used in @DriveWithDataMethod annotation",this.dataMethod.getName());
				ds = new DataMethodDataSource(this.dataMethod);
			} catch (Throwable e){
				throwConstructionException("@DriveWithDataMethod", name, e);
			}
			break;
		case DATA_GENERATOR:
			if (ArjunaInternal.displayDataMethodProcessingInfo){
				logger.debug("Choose Named Data Generator? " + this.chooseNamedDataGenerator);
			}
			if (this.chooseNamedDataGenerator){
				if (ArjunaInternal.displayDataMethodProcessingInfo){
					logger.debug("Fetching central data generator");
				}
				try{
					name = String.format("[%s] named generator used in @DriveWithDataGenerator annotation",this.dataGeneratorName);
					ds = ArjunaInternal.getDataSourceFromDataGenName(this.dataGeneratorName);
				} catch (Throwable e){
					throwConstructionException("@DriveWithDataGenerator", name, e);
				}
			} else {
				if (ArjunaInternal.displayDataMethodProcessingInfo){
					logger.debug("Creating specific data generator object");
				}
				try{
					name = String.format("[%s] class used as data generator in @DriveWithDataGenerator annotation",this.dataGeneratorClass.getName());
					ds = this.dataGeneratorClass.newInstance();
				} catch (Throwable e){
					throwConstructionException("@DriveWithDataGenerator", name, e);
				}
			}
			break;
		default:
			name = "Dummy Data Source";
			ds = new DummyDataSource();
		}	
		
		ds.setName(name);
		return ds;
	}
	

}
