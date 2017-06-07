package pvt.unitee.interfaces;

public interface InternlReportableObserver<T> {
	void initUpdate() throws Exception;
	void endUpdate() throws Exception;
	
	void setUp() throws Exception;
	void tearDown() throws Exception;
	
	void update(T reportable) throws Exception ;
}
