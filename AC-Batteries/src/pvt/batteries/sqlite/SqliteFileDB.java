package pvt.batteries.sqlite;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

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

	public ResultSet select(String sql) throws SQLException{
		PreparedStatement pstmt  = conn.prepareStatement(sql);
		ResultSet rs  = pstmt.executeQuery();
		return rs;
	}
				
	public void commit() throws SQLException{
		this.conn.commit();
	}
	
	public void close() throws SQLException{
		this.conn.close();
	}
			
}
