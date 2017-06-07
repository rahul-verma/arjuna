package arjunasdk.ddauto.interfaces;

public interface DataRecordContainer extends DataSource {

	void setHeaders(String[] names) throws Exception;

	void add(Object[] record) throws Exception;

	void addAll(Object[][] records) throws Exception;
	
	boolean hasNext();
}