package com.autocognite.pvt.unitee.core.lib.datasource;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.autocognite.arjuna.annotations.Data;
import com.autocognite.arjuna.annotations.DriveWithData;
import com.autocognite.arjuna.annotations.DriveWithDataArray;
import com.autocognite.arjuna.annotations.DriveWithDataFile;
import com.autocognite.arjuna.annotations.DriveWithDataGenerator;
import com.autocognite.arjuna.annotations.DriveWithDataMethod;
import com.autocognite.batteries.config.RunConfig;
import com.autocognite.batteries.databroker.DataSource;
import com.autocognite.batteries.databroker.DataSourceFactory;
import com.autocognite.batteries.util.FileSystemBatteries;
import com.autocognite.pvt.ArjunaInternal;
import com.autocognite.pvt.batteries.enums.BatteriesPropertyType;
import com.autocognite.pvt.unitee.core.lib.annotate.None;
import com.autocognite.pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;

// Purpose of this is to achieve thread safety for Data Sources by creating unique objects every time.
public class DataSourceBuilder {
	private Logger logger = Logger.getLogger(RunConfig.getCentralLogName());
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
		
		dataArrayAnnHeaders = dataArrayContainer.headers();
		
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
			location = RunConfig.value(BatteriesPropertyType.DIRECTORY_DATA_SOURCES).asString() + "/" + location;
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
	
	public DataSource build() throws Exception{
		if (ArjunaInternal.displayDataMethodProcessingInfo){
			logger.debug("Building data source");
		}
		switch (this.dataSourceType){
		case DATA:
			return new SingleDataRecordSource(dataAnnHeaders, dataAnnRecord);
		case DATA_ARRAY:
			return new DataArrayDataSource(this.dataArrayAnnHeaders, this.dataArrayRecords);
		case DATA_FILE:
			return DataSourceFactory.getDataSource(this.location, this.delimiter);
		case DATA_METHOD:
			return new DataMethodDataSource(this.dataMethod);
		case DATA_GENERATOR:
			if (ArjunaInternal.displayDataMethodProcessingInfo){
				logger.debug("Choose Named Data Generator? " + this.chooseNamedDataGenerator);
			}
			if (this.chooseNamedDataGenerator){
				if (ArjunaInternal.displayDataMethodProcessingInfo){
					logger.debug("Fetching central data generator");
				}
				return ArjunaInternal.getDataSourceFromDataGenName(this.dataGeneratorName);
			} else {
				if (ArjunaInternal.displayDataMethodProcessingInfo){
					logger.debug("Creating specific data generator object");
				}
				return this.dataGeneratorClass.newInstance();
			}
		}
		
		throw new Exception(String.format("Unsupported Data Source Type supplied: %s", this.dataSourceType));
		
	}
	

}
