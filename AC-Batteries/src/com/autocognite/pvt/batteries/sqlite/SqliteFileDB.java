package com.autocognite.pvt.batteries.sqlite;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class SqliteFileDB {
	Connection conn = null;
	
	public SqliteFileDB(String dbPathdb){
	    try {
	      Class.forName("org.sqlite.JDBC");
	      conn = DriverManager.getConnection(String.format("jdbc:sqlite:%s", dbPathdb));
	      conn.setAutoCommit(false);
	    } catch ( Exception e ) {
	      System.err.println( e.getClass().getName() + ": " + e.getMessage() );
	      System.exit(0);
	    }
	}
			
	public void dropTable(String tableName){
		// To Do
	}

	public void execute(String sql) throws SQLException{
		Statement stmt = conn.createStatement();
	      stmt.executeUpdate(sql);
	      stmt.close();
	}
				
	public void commit() throws SQLException{
		this.conn.commit();
	}
	
	public void close() throws SQLException{
		this.conn.close();
	}
			
}
