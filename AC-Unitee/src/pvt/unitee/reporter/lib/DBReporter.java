package pvt.unitee.reporter.lib;

import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Map;

import org.apache.poi.util.SystemOutLogger;

import arjunasdk.interfaces.Value;
import pvt.batteries.config.Batteries;
import pvt.batteries.hocon.HoconReader;
import pvt.batteries.hocon.HoconResourceReader;
import pvt.batteries.sqlite.SqliteFileDB;
import pvt.unitee.enums.ArjunaProperty;
import pvt.unitee.enums.RunDBSQLNames;
import pvt.unitee.testobject.lib.definitions.JavaTestClassDefinition;
import pvt.unitee.testobject.lib.definitions.JavaTestMethodDefinition;

import java.util.*;

public class DBReporter {
	
	private SqliteFileDB centralDB = null;
	private SqliteFileDB runDB = null;
	private int currentClassIndex = 0;
	private Map<String, Integer> classIndexMap = new HashMap<String, Integer>();
	private int currentMethodIndex = 0;
	
	private Map<String,Value> rsMap = null; 
	public DBReporter() throws Exception{
		runDB = new SqliteFileDB(Batteries.value(ArjunaProperty.PROJECT_CORE_DB_RUN_DBFILE).asString());
		HoconReader rsReader = new HoconResourceReader(this.getClass().getResourceAsStream("/com/testmile/pvt/text/rs.conf"));
		rsReader.process();
		rsMap = rsReader.getProperties();
	}

	public void registerMethodDefinition(JavaTestMethodDefinition tmd) throws SQLException, Exception {
		PreparedStatement stmt = runDB.prepare(this.rsMap.get(RunDBSQLNames.ADD_CREATOR.toString()).asString());
		stmt.setInt(1, this.classIndexMap.get(tmd.getClassDefinition().getTestVariables().object().qualifiedName()));
		stmt.setInt(2, ++currentMethodIndex);
		stmt.setString(3, tmd.getTestVariables().test().id());
		stmt.setString(4, tmd.getTestVariables().test().name());
		stmt.setString(5, tmd.getTestVariables().test().idea());
		stmt.setInt(6, tmd.getTestVariables().test().priority());
		stmt.setString(7, tmd.getQualifiedName());
		stmt.setString(8, tmd.getTestVariables().object().name());
		runDB.insert(stmt);
	}

	public void registerClassDefinition(JavaTestClassDefinition tcd) throws SQLException, Exception {
		PreparedStatement stmt = runDB.prepare(this.rsMap.get(RunDBSQLNames.ADD_CONTAINER.toString()).asString());
		stmt.setInt(1, ++currentClassIndex);
		stmt.setString(2, tcd.getTestVariables().test().id());
		stmt.setString(3, tcd.getTestVariables().test().name());
		stmt.setString(4, tcd.getTestVariables().test().idea());
		stmt.setString(5, tcd.getTestVariables().object().pkg());
		stmt.setInt(6, tcd.getTestVariables().test().priority());
		stmt.setString(7, tcd.getTestVariables().object().qualifiedName());
		stmt.setString(8, tcd.getName());
		runDB.insert(stmt);
		classIndexMap.put(tcd.getTestVariables().object().qualifiedName(), currentClassIndex);
	}
	
	public void addTestResult() throws SQLException, Exception {
		PreparedStatement stmt = runDB.prepare(this.rsMap.get(RunDBSQLNames.ADD_CONTAINER.toString()).asString());
		stmt.setInt(1, ++currentClassIndex);
		stmt.setString(2, tcd.getTestVariables().test().id());
		stmt.setString(3, tcd.getTestVariables().test().name());
		stmt.setString(4, tcd.getTestVariables().test().idea());
		stmt.setString(5, tcd.getTestVariables().object().pkg());
		stmt.setInt(6, tcd.getTestVariables().test().priority());
		stmt.setString(7, tcd.getTestVariables().object().qualifiedName());
		stmt.setString(8, tcd.getName());
		runDB.insert(stmt);
		classIndexMap.put(tcd.getTestVariables().object().qualifiedName(), currentClassIndex);
	}
	
	public void finalizeDefinitions() throws SQLException{
		runDB.commit();
	}

	public void tearDown() throws Exception {
		this.runDB.close();
	}

}
